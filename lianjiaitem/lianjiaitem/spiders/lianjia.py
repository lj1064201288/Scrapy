# -*- coding: utf-8 -*-
import re, os
import time
import random
import scrapy
from scrapy import Request
from ..settings import headers
from ..items import LianjiaItem
from urllib import request


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['www.lianjia.com']

    def start_requests(self):
        url = 'https://cd.lianjia.com/zufang/pg{}'
        start_urls = []
        for page in range(1,101):
            start_url = url.format(page)
            start_urls.append(start_url)
        for start_url in start_urls:
            yield Request(url=start_url, callback=self.parse, dont_filter=True, headers=headers, encoding='utf-8')
            # 爬取完一次后进行暂停
            rest = [0.5, 1, 1.5, 1.25, 1.75, 2]
            time.sleep(random.choice(rest))


    def parse(self, response):
        infos = response.xpath('//div[@class="content__list"]/div')
        for info in infos:
            # 获得房子的标题
            house_title = info.xpath('./div/p/a/text()').extract()[0]
            house_title = house_title.strip().replace(' ', '')
            # 获得房子的地址
            house_address = info.xpath('./div/p[@class="content__list--item--des"]/a/text()').extract()
            if house_address:
                house_address = '-'.join(house_address)
            else:
                house_address = '同创公寓'
            # 获取价格信息
            house_price = info.xpath('./div/span/em/text()').extract()[0]
            if house_price:
                house_price = house_price + '元/月'

            #获取房屋来源
            house_source = info.xpath('./div/p[3]/text()').extract()
            house_source = house_source[0].strip().replace(' ', '')
            # 获取房子的详细页面连接
            house_href = info.xpath('./div/p/a/@href').extract()[0]
            house_href = 'https://cd.lianjia.com/' + house_href

            meta = {
                'house_title': house_title,
                'house_address': house_address,
                'house_price': house_price,
                'house_source': house_source,
                'house_href': house_href
            }
            if meta['house_address'] != '同创公寓':
                yield Request(url=meta['house_href'], callback=self.parse_par, dont_filter=True, headers=headers, meta=meta)

    def parse_par(self, response):
        # 获取房屋发布时间
        putaway = response.xpath('//div[@class="content__subtitle"]/text()').extract()[1]
        putaway = re.findall(r'\d+-\d+-\d+', putaway)[0]
        # 获取房屋编号
        house_id = response.xpath('//div[@class="content__subtitle"]/i[2]/text()').extract()[0]
        house_id = re.findall(r'CD\d+', house_id)[0]
        # 附近设施
        aside_content = response.xpath('//div[@class="content__aside fr"]/p[2]/i/text()').extract()
        aside_content = '-'.join(aside_content)
        # 租赁方式
        house_typ = response.xpath('.//ul[@class="content__aside__list"]/p/span[1]/text()').extract()[0]
        # 房间样式
        house_mode = response.xpath('.//ul[@class="content__aside__list"]/p/span[2]/text()').extract()[0]
        # 房间面积
        house_area = response.xpath('.//ul[@class="content__aside__list"]/p/span[3]/text()').extract()[0]
        # 房间大小
        house_orient= response.xpath('.//ul[@class="content__aside__list"]/p/span[4]/text()').extract()[0]
        # 经纪人
        broker = response.xpath('//ul[@class="content__aside__list"]/li/div[@class="content__aside__list--title oneline"]/span/@title').extract()[0]
        # 发布
        issue = response.xpath('//div[@class="content__article__info"]/ul/li[2]/text()').extract()[0]
        # 入住
        cheak = response.xpath('//div[@class="content__article__info"]/ul/li[3]/text()').extract()[0]
        # 租期
        tenancy_trem = response.xpath('//div[@class="content__article__info"]/ul/li[5]/text()').extract()[0]
        # 看房
        look_house = response.xpath('//div[@class="content__article__info"]/ul/li[6]/text()').extract()[0]
        # 楼层
        floor = response.xpath('//div[@class="content__article__info"]/ul/li[8]/text()').extract()[0]
        # 电梯
        elevator = response.xpath('//div[@class="content__article__info"]/ul/li[9]/text()').extract()[0]
        # 车位
        stall = response.xpath('//div[@class="content__article__info"]/ul/li[11]/text()').extract()[0]
        # 用水
        water = response.xpath('//div[@class="content__article__info"]/ul/li[12]/text()').extract()[0]
        # 用电
        elector = response.xpath('//div[@class="content__article__info"]/ul/li[14]/text()').extract()[0]
        # 燃气
        fuel_gas = response.xpath('//div[@class="content__article__info"]/ul/li[15]/text()').extract()[0]
        # 房屋描述
        house_infos = response.xpath('//div[@class="content__article__info3"]/ul/li/p/@data-desc').extract()
        if house_infos:
            house_infos = house_infos[0].replace('<br />', '').strip().replace('', '')
        else:
            house_infos = '没有说明'
        # print(issue, cheak, tenancy_trem, look_house, floor, elevator, stall, water, elector, fuel_gas)
        item = LianjiaItem()
        item = {
            'title': response.meta['house_title'],
            'house_address': response.meta['house_address'],
            'house_source':response.meta['house_source'],
            'house_href': response.meta['house_href'],
            'house_typ': house_typ,
            'house_mode': house_mode,
            'house_area':house_area,
            'house_orient': house_orient,
            'putaway_time': putaway,
            'house_id': house_id,
            'house_price': response.meta['house_price'],
            'aside_content': aside_content,
            'broker': broker,
            'issue': issue,
            'cheak': cheak,
            'tenancy_term': tenancy_trem,
            'look_house': look_house,
            'floor': floor,
            'elevator': elevator,
            'stall': stall,
            'water': water,
            'electro': elector,
            'fuel_gas': fuel_gas,
            'house_infos': house_infos
        }

        yield item

        # print(house_id, putaway, aside_content, house_typ, house_area, house_mode, house_size)
        ''' images_url = response.xpath('//div[@class="content__article__slide"]/div/ul/li/img/@src').extract()
        file_path = 'C:\python\scrapy_win\lianjiaitem\lianjiaitem\images\{}'.format(response.meta['house_title'])
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for image_url in  images_url:
            flag = str(time.time()) + '.jpg'
            print(flag)
            request.urlretrieve(image_url, file_path + os.sep + flag)
        '''


