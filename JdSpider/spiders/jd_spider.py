# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
from urllib import parse
import re
from JdSpider.items import JDItemLoader, JdspiderItem
import datetime
from selenium import webdriver
from JdSpider.settings import CHROME_DRIVER_PATH
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class JdSpiderSpider(RedisSpider):
    name = 'jd_spider'
    redis_key = 'jd_spider:start_urls'
    allowed_domains = ['jd.com']

    def __init__(self, **kwargs):
        # 初始化selenium加载页面用的browser
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_opt.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_opt)
        # self.browser = webdriver.Chrome(executable_path=r"E:\Workspaces\OldSpider\JdSpider\JdSpider\driver\chromedriver2_34.exe", chrome_options=chrome_opt)
        super(JdSpiderSpider, self).__init__()
        dispatcher.connect(self.spider_close, signals.spider_closed)

        self.first = True
        self.yieldNum = 0
        self.yieldPNum = 0

    def spider_close(self):
        # 当爬虫退出的时候关闭chrome
        self.browser.close()

    def parse(self, response):
        """
        1. 提取出html页面中的所有url，并跟踪这些url进行异步爬取
        2. 如果提取的url中格式为/item.jd.com/xxx 直接进入解析函数
        """
        index_obj = re.match("(.*www.jd.com.*)", response.url)
        if index_obj and self.first:
            self.first = False
            all_urls = response.css(".cate_menu a::attr(href)").extract()
            all_urls = [parse.urljoin(response.url, url) for url in all_urls]
            for url in all_urls:
                self.yieldNum += 1
                yield scrapy.Request(url)
        else:
            all_urls = response.css("a::attr(href)").extract()
            all_urls = [parse.urljoin(response.url, url) for url in all_urls]
            new_urls = []
            for url in all_urls:
                m = re.match(".*javascript.*", url)
                if not m:
                    new_urls.append(url)
            for url in new_urls:
                match_obj = re.match("(.*item.jd.com/(\d+).html.*)", url)
                if match_obj:
                    # 如果提取到item相关的页面则下载后交由parse_item进行提取
                    request_url = match_obj.group(1)
                    item_id = match_obj.group(2)
                    # 通过yield返回给scrapy的下载器，另外一定要用request
                    self.yieldPNum += 1
                    yield scrapy.Request(request_url, meta={"item_id": item_id}, callback=self.parse_item, priority=1)
                elif re.match("(.*list.jd.com/.*)", url):
                    if not re.match(".*&ev=.*", url):
                        yield scrapy.Request(url)

        # 对单个网站测试
        # match_obj = re.match("(.*item.jd.com/(\d+).html.*)", response.url)
        # item_id = match_obj.group(2)
        # yield scrapy.Request(response.url, meta={"item_id": item_id}, callback=self.parse_item, priority=1)

    def parse_item(self, response):

        item_loader = JDItemLoader(item=JdspiderItem(), response=response)
        item_id = response.meta.get("item_id", "")
        e = False
        if item_id:
            if (response.css(".breadcrumb")):
                # 图书类
                if not response.css(".m-itemover"):
                    # 是否下架
                    tag_list = self.get_book_tag_list(response=response)
                    item_loader.add_value("item_id", item_id)
                    item_loader.add_css("name", "#name h1::text")
                    item_loader.add_value("summary", self.get_summary(response=response))  # js加载
                    item_loader.add_value("price", self.get_a_price(response=response)) # js加载
                    item_loader.add_value("tag_1", tag_list[0])
                    item_loader.add_value("tag_2", tag_list[1])
                    item_loader.add_value("tag_3", tag_list[2])
                    item_loader.add_value("tag_4", tag_list[3])
                    item_loader.add_value("dianpu_name", self.get_book_dianpu_name(response=response))
                    item_loader.add_value("jself", self.get_jself(response=response))
                    item_loader.add_value("crawl_time", datetime.datetime.now())
                    e = True
            elif(response.css("#crumb-wrap")):
                # 非图书类，且没有被重定向到首页
                if not response.css(".itemover"):
                    # 是否下架
                    tag_list = self.get_tag_list(response=response)
                    item_loader.add_value("item_id", item_id)
                    item_loader.add_css("name", ".ellipsis::attr(title)")
                    item_loader.add_css("summary", ".sku-name::text")
                    # item_loader.add_css("price", ".summary-price-wrap .price::text")
                    item_loader.add_value("price", self.get_b_price(response=response))
                    item_loader.add_value("tag_1", tag_list[0])
                    item_loader.add_value("tag_2", tag_list[1])
                    item_loader.add_value("tag_3", tag_list[2])
                    item_loader.add_value("tag_4", tag_list[3])
                    item_loader.add_value("dianpu_name", self.get_dianpu_name(response=response))
                    item_loader.add_value("jself", self.get_jself(response=response))
                    item_loader.add_value("crawl_time", datetime.datetime.now())
                    e = True
            if e:
                jd_item = item_loader.load_item()
                print("return jd_item")
                return jd_item

    def get_a_price(self, response):
        price = response.css("#jd-price::text").extract()[0]
        if "￥" in price:
            price = price.replace("￥", "")
        try:
            price = float(price)
        except:
            price = 0
        return price

    def get_b_price(self, response):
        itemId = response.meta.get("item_id", "")
        price = response.css(".J-p-{0}::text".format(itemId)).extract()[0]
        if "￥" in price:
            price = price.replace("￥", "")
        try:
            price = float(price)
        except:
            price = 0
        return price

    def get_book_dianpu_name(self, response):
        dianpu_name = response.xpath("//div[@class='seller-infor']/a/@title").extract()
        if not dianpu_name:
            dianpu_name.append("京东自营")
        return dianpu_name

    def get_dianpu_name(self, response):
        dianpu_name = response.xpath("//a[@clstag='shangpin|keycount|product|dianpuname1']/@title").extract()
        if not dianpu_name:
            dianpu_name.append("京东自营")
        return dianpu_name

    def get_jself(self, response):
        jself = response.css(".u-jd")
        if jself:
            return 1
        else:
            return 0

    def get_book_tag_list(self, response):
        tag_list = response.css(".breadcrumb a::text").extract()
        for i in range(4 - len(tag_list)):
            tag_list.append("...")
        return tag_list

    def get_tag_list(self, response):
        tag_list = response.css("#crumb-wrap .crumb a::text").extract()
        for i in range(4 - len(tag_list)):
            tag_list.append("...")
        return tag_list

    def get_summary(self, response):
        summary = "作者：" + response.css("#p-author a::text").extract_first("") + "；" \
                  + response.css("#p-ad::text").extract_first("")
        return summary


