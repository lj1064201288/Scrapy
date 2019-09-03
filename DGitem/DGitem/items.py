# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DgitemItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DGItem(scrapy.Item):
    collection = table = 'dg'
    title = scrapy.Field()
    content = scrapy.Field()
    status = scrapy.Field()
    net_friend = scrapy.Field()
    date = scrapy.Field()
    number = scrapy.Field()
