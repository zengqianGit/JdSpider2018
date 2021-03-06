# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi


class JdspiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        a = item["item_id"]
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item):
        # 处理异步插入的异常
        print(item["item_id"])
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # print ("do_insert")
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
        print ("cursor.execute(insert_sql, {0})".format(params))


# class ElasticsearchPipeline(object):
#     #将数据写入到es中
#     def process_item(self, item, spider):
#         #将item转换为es的数据
#         item.save_to_es()
#         return item