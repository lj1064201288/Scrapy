# -*- coding: utf-8 -*-
import scrapy, os, time
from scrapy import Request
from urllib.request import urlretrieve

class LrSpider(scrapy.Spider):
    name = 'lr'
    allowed_domains = ['www.lanrentuku.com']
    start_urls = []
    for page in range(1,4):
        start_urls.append('http://www.lanrentuku.com/tupian/p{}.html'.format(page))

    root_dir = r'C:\python\datas\images\tuku'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    def parse(self, response):
        dds = response.xpath('//div[@class="list-pic"]/dl/dd')
        for dd in dds:
           try:
                # 获取详情链接
                image_link = dd.xpath('./a/@href').extract()
                image_link = 'http://' + self.allowed_domains[0] + image_link[0]
                # 获取缩略图链接
                image_th = dd.xpath('./a/img/@src').extract()[0]
                # 获取标题
                img_alt = dd.xpath('./a/img/@alt').extract()[0]
                item = {
                    'image_th': image_th,
                    'img_alt': img_alt,
                    'chrome': False
                }
                yield Request(url=image_link, callback=self.Default_page, meta=item)
           except:
                pass

    def Default_page(self, response):
        print(response.url)
        # 获取详细页面的图片链接
        image = response.xpath('//div[@class="content-a content-tupian"]/p/img/@src').extract()[0]

        path = r'{}\{}.jpg'.format(self.root_dir, response.meta['img_alt'])
        urlretrieve(image, path)

