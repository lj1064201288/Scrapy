# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiciproxyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class XcproxyItem(scrapy.Item):
    country = scrapy.Field()
    ipaddress = scrapy.Field()
    port = scrapy.Field()
    serveraddr = scrapy.Field()
    isanonymous = scrapy.Field()
    type = scrapy.Field()
    alivetime = scrapy.Field()
    verifictiontime = scrapy.Field()
