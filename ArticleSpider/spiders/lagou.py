# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItem, LagouJobItemLoader
from ArticleSpider.utils.common import get_md5
# from selenium import webdriver
import pickle
from datetime import datetime

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/','https://www.lagou.com/jobs/3699428.html']


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }

    rules = (
        # Rule(LinkExtractor(allow=r'gongsi/j\d+.html'),  callback='parse_job', follow=True),
        Rule(LinkExtractor(allow=r'zhaopin/.*'),process_request='request_tagPage', callback='parse_job', follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), process_request='request_tagPage', callback='parse_job', follow=True )

    )

    def request_tagPage(self, request):
        tagged = request.replace(headers=self.headers)
        tagged.meta.update(cookiejar=1)
        return tagged

    def start_requests(self):
        import pickle
        cookie_dict = {}
        # from selenium import webdriver
        # browser = webdriver.Chrome()
        # browser.get("https://passport.lagou.com/login/login.html")
        # browser.find_element_by_css_selector("div:nth-child(2) > form > div:nth-child(1) > input").send_keys(
        #     "15957112261")
        # browser.find_element_by_css_selector("div:nth-child(2) > form > div:nth-child(2) > input").send_keys(
        #     "EmFW.W}b2R7i")
        # browser.find_element_by_css_selector(
        #     "div:nth-child(2) > form > div.input_item.btn_group.clearfix > input").click()
        # import time
        # time.sleep(2)
        # Cookies = browser.get_cookies()
        # browser.quit()
        # print(Cookies)
        # cookie_dict = {}
        # print(Cookies)
        # with open('/Users/eeljiang/Desktop/lagouCookies', 'wb') as f:
        #     for cookie in Cookies:
        #         cookie_dict[cookie['name']] = cookie['value']
        #     pickle.dump(cookie_dict, f)

        with open('/Users/eeljiang/Desktop/lagouCookies', 'rb') as f:
            cookie_dict = pickle.load(f)

        return [scrapy.Request(url=self.start_urls[0], headers=self.headers, cookies=cookie_dict, callback=self.parse)]


    def parse_job(self, response):
        # 解析拉勾网的职位
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name span::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("tags", ".position-label li::text")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_css("company_name", "#job_company dt a div h2::text")
        item_loader.add_value("crawl_time", datetime.now())
        job_item = item_loader.load_item()

        yield job_item





