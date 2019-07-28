# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import XiaoHuaItem


class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['www.xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/2014.html']

    def parse(self, response):
        infos = response.xpath('//div[@class="demo clearfix"]/div/div')
        item = XiaoHuaItem()
        for info in infos:
            title = info.xpath('.//div[@class="title"]/span/a/text()').extract()
            href = info.xpath('.//div[@class="title"]/span/a/@href').extract()

            item['title'] = title[0]
            item['href'] = href[0]

            yield item

