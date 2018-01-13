# -*- coding: utf-8 -*-

# Scrapy settings for JdSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'JdSpider'

SPIDER_MODULES = ['JdSpider.spiders']
NEWSPIDER_MODULE = 'JdSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'JdSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'JdSpider.middlewares.JdspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'JdSpider.middlewares.JSPageMiddleware': 1,
   'JdSpider.middlewares.RandomUserAgentMiddlware': 500,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'JdSpider.pipelines.JdspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MYSQL_HOST = "localhost"
MYSQL_DBNAME = "jd_spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_PATH = "{0}/driver/chromedriver.exe".format(ROOT_PATH)

RANDOM_UA_TYPE = "random"

NOT_ALLOW_URL = [
   "bao.jd.com",
   "baitiao",
   "bk.jd.com",
   "coin.jd.com",
   "chat.jd.com",
   "credit.jd.com",
   "dang.jd.com",
   "dcrz.jd.com",
   "dq.jd.com",
   "dj.jd.com",
   "edu.jd.com",
   "fund.jd.com",
   "ft.jd.com",
   "gupiao.jd.com",
   "jc.jd.com",
   "jr.jd.com",
   "jrhelp.jd.com",
   "jincai.jd.com",
   "jimi.jd.com",
   "licai.jd.com",
   "licaishi.jd.com",
   "loan.jd.com",
   "nj.jd.com",
   "pingce.jd.com",
   "quant.jd.com",
   "rich.jd.com",
   "sale.jd.com",
   "z.jd.com",
   "zbbs.jd.com",
]