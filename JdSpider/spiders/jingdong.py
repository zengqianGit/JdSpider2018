# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class JingdongSpider(CrawlSpider):
    name = 'jingdong'
    allowed_domains = ['jd.com']
    # start_urls = ['https://www.jd.com/']
    start_urls = ['https://item.jd.com/3779751.html']
    rules = (
        # 提取匹配 'jd.com/'的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=(r'.*jd.com/.*',)), ),

        # 提取匹配 'item.jd.com/' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=(r'.*item.jd.com/\d+.html.*',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
