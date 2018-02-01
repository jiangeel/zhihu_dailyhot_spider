# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re, time
from datetime import datetime
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuQuestionItem,ZhihuAnswerItem,ZhihuQuestionItemLoader
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class ZhihuSelSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/explore']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        # 在 middlewares 中随机取定
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    # custom_settings = {
    #     "COOKIES_ENABLED": True
    # }

    ## 不再适用: 由于标签页数量不多,每个标签都新建一个浏览器了, 而非共用一个了,在 middlewares.py 中
    def __init__(self):
        # self.browser = webdriver.PhantomJS(executable_path='/Users/eeljiang/phantomjs-2.1.1-macosx/bin/phantomjs')
        self.browser = webdriver.Chrome()
        super(ZhihuSelSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出的时候退出浏览器
        print("spider closed")
        self.browser.quit()


    def parse(self, response):

        # print("开始访问：{0}".format('https://www.zhihu.com/explore'))
        # self.browser.get('https://www.zhihu.com/explore')
        # time.sleep(3)
        #
        # print("开始滚动")
        # for i in range(2):
        #     self.browser.execute_script(
        #         "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        #     time.sleep(3)
        #
        # url = self.browser.current_url
        # body = self.browser.page_source
        # browser.quit()


        # browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.1.6087331e0UHPZn&id=562389491680&cm_id=140105335569ed55e27b&abbucket=9&skuId=3696699135152")
        # print(browser.page_source)
        # browser.quit()


        # self.browser.close()

        # all_urls = response.css("a::attr(href)").extract()
        # all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = response.css("div[data-type='daily'] .question_link::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]

        for url in all_urls:
            print(url)

        for url in all_urls:

            # if url == 'https://www.zhihu.com/question/265024635/answer/307551635':
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_question,
                                 cookies=response.request.cookies)
            # match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)

            # if match_obj:
            #     # 提取到 question 页面
            #     request_url = match_obj.group(1)
            #     question_id = match_obj.group(2)
            #     # print("print: ", request_url, question_id)
            #     yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            #     # break
            # else:
            #     # 不是 question 页面
            #     pass
            #     yield scrapy.Request(url, headers=self.headers, callback=self.parse)


    def parse_question(self, response):
        # 处理question页面， 从页面中提取出具体的question item
        match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
        if match_obj:
            question_id = int(match_obj.group(2))

        item_loader = ZhihuQuestionItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css("title", "h1.QuestionHeader-title::text")
        item_loader.add_css("content", ".QuestionHeader-detail")
        item_loader.add_value("url", response.url)
        item_loader.add_value("zhihu_id", question_id)
        item_loader.add_css("answer_num", ".QuestionMainAction::text")
        item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num", ".QuestionFollowStatus strong::text")
        item_loader.add_css("click_num", ".QuestionFollowStatus strong::text")
        item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
        item_loader.add_css("answerer_name", ".UserLink-link::text")
        item_loader.add_css("answerer_des", ".AuthorInfo-badgeText")
        item_loader.add_css("answer_text", ".RichContent-inner")
        item_loader.add_css("answer_like_num", ".Voters button::text")
        item_loader.add_value("crawl_time", datetime.now())


        question_item = item_loader.load_item()

        yield question_item

    def parse_answer(self, reponse):
        pass

    def start_requests(self):
        import pickle
        cookie_dict = {}
        # browser = webdriver.Chrome()

        # True:保存到文件 False: 从文件里读取
        if True:
            self.browser.get("https://www.zhihu.com/signin")
            time.sleep(3)
            self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                "15957112261")
            self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
                "g2D-Mdp-Lck-kFx")
            self.browser.find_element_by_css_selector(
                ".Button.SignFlow-submitButton").click()
            time.sleep(3)
            Cookies = self.browser.get_cookies()
            # self.browser.close()
            # print(Cookies)

            # with open('/Users/eeljiang/Desktop/zhihuCookies', 'wb') as f:
            for cookie in Cookies:
                cookie_dict[cookie['name']] = cookie['value']
                # pickle.dump(cookie_dict, f)
                # pickle.dump(Cookies, f)


        else:
            with open('/Users/eeljiang/Desktop/zhihuCookies', 'rb') as f:
                cookie_dict = pickle.load(f)

        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, headers=self.headers, cookies=cookie_dict)]
