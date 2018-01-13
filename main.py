# -*- coding: utf-8 -*-  
__author__ = 'qianzeng'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))) #将main所在的父级目录添加到path
execute(["scrapy", "crawl", "jd_spider"])