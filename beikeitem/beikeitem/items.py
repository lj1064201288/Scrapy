# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeikeitemItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BeikeItem(scrapy.Item):
    price = scrapy.Field()
    address = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    lngandlat = scrapy.Field()
