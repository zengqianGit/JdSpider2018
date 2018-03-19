# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from JdSpider.models.es_types import JdSpiderType


from elasticsearch_dsl.connections import connections
es = connections.create_connection(JdSpiderType._doc_type.using)

def handle_strip(value):
    return value.strip()


def price(value):
    return float(value.replace("￥", ""))


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

def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    return suggests
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
    price = scrapy.Field(
        input_processor=MapCompose(price)
    )
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

    def save_to_es(self):
        jd = JdSpiderType()
        jd.item_id = self["item_id"]
        jd.name = self["name"]
        jd.summary = self["summary"]
        jd.price = self["price"]
        jd.tag_1 = self["tag_1"]
        jd.tag_2 = self["tag_2"]
        jd.tag_3 = self["tag_3"]
        jd.tag_4 = self["tag_4"]
        jd.dianpu_name = self["dianpu_name"]
        jd.jself = self["jself"]
        jd.crawl_time = self["crawl_time"]

        jd.suggest = gen_suggests(JdSpiderType._doc_type.index, ((jd.name,10),(jd.summary, 7)))

        jd.save()
        #
        # redis_cli.incr("jobbole_count")

        return
