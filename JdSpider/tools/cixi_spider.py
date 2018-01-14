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
            insert_sql = "insert proxy_ip(ip, port, proxy_type, speed) VALUES('{0}', '{1}', '{2}', {3})".format(
                        ip[0], ip[1], ip[2], ip[3])
            try:
                cursor.execute(insert_sql)
            except Exception as e:
                print ("primary key is exist")

            conn.commit()


class GetIP(object):

    def delete_ip(self, ip):
        delete_sql = "delete from proxy_ip where ip = '{0}'".format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        http_url = "https://item.jd.com/5143491.html"
        proxy_url = "https://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url
            }
            response = requests.get(http_url, proxies = proxy_dict)
            # print (response.text)
            return True
        except Exception as e:
            print ("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                return True
            else:
                print ("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        random_sql = "select ip, port from proxy_ip order by RAND() limit 1"
        result = cursor.execute(random_sql)
        for ip in cursor.fetchall():
            if self.judge_ip(ip[0], ip[1]):
                return "https://{0}:{1}".format(ip[0], ip[1])
            else:
                return self.get_random_ip()



# get_ip = GetIP()
# ip = get_ip.get_random_ip()
# print (ip)