# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from JdSpider.models.es_types import JdSpiderType
import redis
from elasticsearch_dsl.connections import connections

es = connections.create_connection(JdSpiderType._doc_type.using)
redis_cli = redis.StrictRedis()


def handle_strip(value):
    return value.strip()


def price(value):
    # return float(value.replace("￥", ""))
    try:
        value = float(value)
    except:
        value = -1
    return value


def isJdBookStore(value):
    if len(value) == 0:
        return "京东自营"
    else:
        return value


def isJself(value):
    if value:
        return 1
    else:
        return 0

#
# def get_book_dianpu_name(self, response):
#     dianpu_name = response.xpath("//div[@class='seller-infor']/a/@title").extract()
#     if not dianpu_name:
#         dianpu_name.append("京东自营")
#     return dianpu_name
#
# def get_dianpu_name(self, response):
#     dianpu_name = response.xpath("//a[@clstag='shangpin|keycount|product|dianpuname1']/@title").extract()
#     if not dianpu_name:
#         dianpu_name.append("京东自营")
#     return dianpu_name
#
# def get_jself(self, response):
#     jself = response.css(".u-jd")
#     if jself:
#         return 1
#     else:
#         return 0
#
# def get_book_tag_list(self, response):
#     tag_list = response.css(".breadcrumb a::text").extract()
#     for i in range(4 - len(tag_list)):
#         tag_list.append("...")
#     return tag_list
#
# def get_tag_list(self, response):
#     tag_list = response.css("#crumb-wrap .crumb a::text").extract()
#     for i in range(4 - len(tag_list)):
#         tag_list.append("...")
#     return tag_list


class JDItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JdspiderItem(scrapy.Item):
    item_id = scrapy.Field()
    name = scrapy.Field()
    summary = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    price = scrapy.Field()
    tag_1 = scrapy.Field()
    tag_2 = scrapy.Field()
    tag_3 = scrapy.Field()
    tag_4 = scrapy.Field()
    dianpu_name = scrapy.Field(
        input_processor=MapCompose(isJdBookStore)
    )
    jself = scrapy.Field(
        input_processor=MapCompose(isJself)
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jd_item(item_id, name, summary, price, tag_1, tag_2, tag_3, tag_4, dianpu_name, jself, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE price=VALUES(price), crawl_time=VALUES(crawl_time)
        """

        params = (self["item_id"], self["name"], self["summary"], self["price"], self["tag_1"], self["tag_2"],
                  self["tag_3"], self["tag_4"], self["dianpu_name"], self["jself"], self["crawl_time"])

        print ("return insert_sql, params")
        return insert_sql, params

