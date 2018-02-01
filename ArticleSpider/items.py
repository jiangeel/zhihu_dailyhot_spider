# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime
import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from ArticleSpider.utils.common import extract_nums
from ArticleSpider.settings import SQL_DATE_FORMAT,SQL_DATETIME_FORMAT
from w3lib.html import remove_tags


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    value = value.replace('·', '').strip()
    try:
        create_date = datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.now().now()
    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comma(value):
    return value.replace(',', '')


def return_value(value):
    return value



class TakeLast(object):
    def __call__(self, values):
        return values[-1]


def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


class ArticleItemloader(ItemLoader):
    # 自定义 itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field(
        output_processor=(remove_comment_tags)
    )
    tags = scrapy.Field(
        output_processor=Join(',')
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    vote_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    url_object_id = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into articles(title, url, create_date, fav_nums)
                VALUEs (%s, %s, %s, %s)
                """
        params = (self['title'], self['url'], self['create_date'], self['fav_nums'])

        return insert_sql, params


class ZhihuQuestionItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field(
        input_processor=MapCompose(remove_tags),
    )
    answer_num = scrapy.Field(

        input_processor=MapCompose(remove_comma, get_nums)
    )
    comments_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    watch_user_num = scrapy.Field(
        input_processor=MapCompose(remove_comma)

    )
    click_num = scrapy.Field(
        input_processor=MapCompose(remove_comma),
        output_processor=TakeLast()

    )
    crawl_time = scrapy.Field()
    answerer_name = scrapy.Field()
    answerer_des = scrapy.Field(
        input_processor=MapCompose(remove_tags),
    )
    answer_text = scrapy.Field(
        input_processor=MapCompose(remove_tags),

    )
    answer_like_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )

    def get_insert_sql(self):
        # 插入知乎 question 表的 sql 语句
        insert_sql = """ 
                insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num,
              watch_user_num, click_num, crawl_time,answerer_name,answerer_des,answer_text,answer_like_num
              ) 
                VALUES (%s, %s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)
                ON DUPLICATE KEY UPDATE content=VALUES(content), 
                                        comments_num=VALUES(comments_num),
                                        crawl_time=VALUES(crawl_time)
                """

        params = (self["zhihu_id"], self["topics"], self["url"], self["title"], self["content"], self["answer_num"], self["comments_num"],
        self["watch_user_num"], self["click_num"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT), self["answerer_name"],self["answerer_des"],self["answer_text"],self["answer_like_num"])

        return insert_sql, params

class ZhihuAnswerItem(scrapy.Item):
    #知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()


def remove_splash(value):
    # 去掉工作城市的斜线
    return value.replace('/', '')


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)

class LagouJobItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(',')
    )
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field(
        input_processor=MapCompose(handle_jobaddr),
    )
    company_url = scrapy.Field()
    crawl_time = scrapy.Field(
        # input_processor=MapCompose(''.join),
    )
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(title, url, url_object_id,salary, job_city, work_years, degree_need,
                        job_type, publish_time, job_advantage, job_desc, job_addr, company_name,
                        company_url, tags, crawl_time) VALUES(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE salary=VALUES(salary), 
                                        job_desc=VALUES(job_desc)
                                       
        """

        params = (self["title"], self["url"],self["url_object_id"], self["salary"], self["job_city"], self["work_years"],
                  self["degree_need"], self["job_type"], self["publish_time"], self["job_advantage"],
                  self["job_desc"], self["job_addr"], self["company_name"], self["company_url"],
                  self["tags"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
                  )

        return insert_sql, params