# -*- coding: utf-8 -*-  
__author__ = 'qianzeng'
import re


NOT_ALLOW_URL = [
   "bao.jd.com",
   "baitiao.jd.com",
   "bk.jd.com",
   "coin.jd.com",
   "chat.jd.com",
   "dang.jd.com",
   "dcrz.jd.com",
   "fund.jd.com",
   "gupiao.jd.com",
   "jc.jd.com",
   "jr.jd.com",
   "jrhelp.jd.com",
   "jincai.jd.com",
   "jimi.jd.com",
   "licai.jd.com",
   "loan.jd.com",
   "nj.jd.com",
   "quant.jd.com",
   "rich.jd.com",
   "sale.jd.com",
   "z.jd.com",
   "zbbs.jd.com",
]

all_urls = ['https://m.jr.jd.com/helppage/downApp/jrAppPromote.html',
            'https://jrhelp.jd.com/',
            'https://chat.jd.com/jd/chat?entry=jd_jr',
            'https://jimi.jd.com/index.action?source=financing',
            'https://licai.jd.com',
            'https://www.jd.com', ]


def not_allow_url(all_urls):
    urls = list(all_urls)
    #
    # for i in range(len(all_urls)):
    #     urls[i] = all_urls[i]
    for i in range(len(all_urls)):
        url = all_urls[i]
        if abc(url):
            urls.remove(url)
    return urls


def abc(url):
    for nau in NOT_ALLOW_URL:
        match_obj = re.match("(.*{0}.*)".format(nau), url)
        if match_obj:
            return True
    return False

print (not_allow_url(all_urls))