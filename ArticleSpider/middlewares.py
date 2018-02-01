# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from ArticleSpider.tools.crawl_xici_ip import GetIP

class ArticlespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class RandomUserAgentMiddleware(object):
    # 随机更换 user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        ua = get_ua()
        request.headers.setdefault('User-Agent', ua)
        pass
        # request.meta["proxy"] = "http://122.245.58.221:8118"

class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        get_ip = GetIP()
        request.meta["proxy"] = get_ip.get_random_ip()


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.http import HtmlResponse
import time
from selenium.webdriver.common.keys import Keys
import pickle

class Use_seleniumMiddleware(object):

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler)

    # 处理第一条链接，用 browser 模拟登录并滚动滚轮
    #作为整个爬虫共享的浏览器, cookie 在最初登录时已经保存,无需再从文件中读取
    def process_request(self, request, spider):
        # # 所有 url 都走 browser
        # browser = webdriver.Chrome()
        # # 先启动浏览器才能添加 cookie
        # browser.get('http://localhost')
        #
        # # 从文件中读取 cookies
        # with open('/Users/eeljiang/Desktop/zhihuCookies', 'rb') as f:
        #     Cookies = pickle.load(f)
        #
        # for cookie in Cookies:
        #     browser.add_cookie(cookie)

        # print("开始访问：{0}".format(request.url))
        # browser.get(request.url)
        # time.sleep(5)


        # 首页需要滚动一下获取多组新闻,否则默认值只显示5条
        # 仅首页使用浏览器
        if request.url in spider.start_urls:
            # browser = webdriver.Chrome()
            print("开始访问：{0}".format(request.url))
            spider.browser.get(request.url)
            time.sleep(3)

            # 按一下 esc 关掉账号异常验证的框
            actions = ActionChains(spider.browser)
            actions.send_keys(Keys.ESCAPE)
            actions.perform()

            print("开始滚动")
            for i in range(3):
                spider.browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(3)

            url = spider.browser.current_url
            body = spider.browser.page_source
            # browser.quit()

            return HtmlResponse(url=url, body=body, encoding="utf-8", request=request)
