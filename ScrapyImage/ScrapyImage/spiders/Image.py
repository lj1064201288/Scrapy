# -*- coding: utf-8 -*-
import scrapy
from ScrapyImage.items import ScrapyimageItem


class ImageSpider(scrapy.Spider):
    name = 'Image'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/archives/55.html']

    def parse(self, response):
        imgurls = response.css('.post-content p img::attr(src)').extract()
        item = ScrapyimageItem()
        item['imgurl'] = imgurls
        yield item
