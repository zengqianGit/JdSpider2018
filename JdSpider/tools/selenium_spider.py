# -*- coding: utf-8 -*-  
__author__ = 'qianzeng'

import os
from selenium import webdriver
from JdSpider.settings import CHROME_DRIVER_PATH


browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
browser.get("http://openlaw.cn/search/judgement/type?causeId=270cfcd1df47453d9ff4b8d40901a587&selected=true")

print (browser.page_source)