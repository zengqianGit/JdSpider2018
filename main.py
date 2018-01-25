# -*- coding: utf-8 -*-  
__author__ = 'qianzeng'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))) #将main所在的父级目录添加到path

# root_path = os.path.dirname(os.path.abspath(__file__))
# jdspider_path = "{0}/JdSpider/driver/chromedriver2_34.exe".format(root_path)
# sys.path.append(jdspider_path)


execute(["scrapy", "crawl", "jd_spider"])