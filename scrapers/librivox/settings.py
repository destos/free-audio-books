# -*- coding: utf-8 -*-

# Scrapy settings for librivox_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import sys

sys.path.append(
    os.path.abspath(os.path.dirname(__file__) + "../../../free_audio_books/"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

import configurations
configurations.setup()

BOT_NAME = 'librivox_scraper'

SPIDER_MODULES = ['librivox.spiders']
NEWSPIDER_MODULE = 'librivox.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'librivox_scraper (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 1,
    # Disable scrappy user agent
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

DEFAULT_REQUEST_HEADERS = {
    'X-Requested-With': 'XMLHttpRequest'
}

