# -*- coding: utf-8 -*-  
__author__ = 'qianzeng'
import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root", db="jd_spider", charset="utf8")
cursor = conn.cursor();


def crawl_ips():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}

    for i in range(2000):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers = headers)

        selector = Selector(text=re.text)
        trs = selector.css("#ip_list tr")
        ip_list = []
        for tr in trs[1:]:
            tds = tr.css("td::text").extract()
            speed_str = tr.css("td").css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            ip_list.append((tds[0], tds[1], tds[5], speed))

        for ip in ip_list:
            cursor.execute("insert proxy_ip(ip, port, proxy_type, speed) VALUES('{0}', '{1}', '{2}', {3})".format(
                    ip[0], ip[1], ip[2], ip[3])
            )
            conn.commit()




crawl_ips()