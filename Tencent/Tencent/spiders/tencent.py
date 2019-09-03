# -*- coding: utf-8 -*-
import scrapy
import json
from Tencent.items import ItemTencent

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['www.tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1559572126675&pageIndex=1&pageSize=4000']

    def parse(self, response):
        # 获取需要的数据
        datas = json.loads(response.text, encoding='utf-8').get('Data').get('Posts')
        item = ItemTencent()
        # 获取到的数据是一个列表，进行遍历
        for data in datas:
            # 删除第一个元素
            del data['Id']
            # 对获取的字典进行遍历传入item
            for k, v in data.items():
                item[k] = v

            yield item