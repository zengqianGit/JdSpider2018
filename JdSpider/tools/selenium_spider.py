# -*- coding: utf-8 -*-  
__author__ = 'qianzeng'

import os
from selenium import webdriver
from JdSpider.settings import CHROME_DRIVER_PATH


browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)


list = ['20171726097','21331832370','21122485290','12650024297','19014277925','15929548767','10194606329',
        '10434991885','10333566878','201543','5512855','10329947407']

for i in range(len(list)):
    browser.get("https://item.jd.com/{0}.html".format(list[i]))
    try:
        b = browser.find_element_by_id("jd-price").text
    except:
        b = browser.find_element_by_css_selector(".p-price .price").text
    finally:
        print (b)
browser.close()