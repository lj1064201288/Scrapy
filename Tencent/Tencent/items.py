# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from Tencent import settings

class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ItemTencent(scrapy.Item):
    collection = table = settings.MYSQL_TABLE
    PostId = scrapy.Field()
    RecruitPostId = scrapy.Field()
    RecruitPostName = scrapy.Field()
    CountryName = scrapy.Field()
    LocationName = scrapy.Field()
    BGName = scrapy.Field()
    ProductName = scrapy.Field()
    CategoryName = scrapy.Field()
    Responsibility = scrapy.Field()
    LastUpdateTime = scrapy.Field()
    PostURL = scrapy.Field()
    SourceID = scrapy.Field()
    IsCollect = scrapy.Field()
    IsValid = scrapy.Field()
