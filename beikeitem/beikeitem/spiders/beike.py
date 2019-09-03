# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import BeikeItem
import re
import time
import math

class BeikeSpider(CrawlSpider):
    name = 'beike'
    # allowed_domains = ['www.ke.com']
    start_urls = ['https://www.ke.com/city/']
    # 获得每个城市的新房链接
    citylink = LinkExtractor(allow=(r'//.*?ke.com$'))
   # louplink = LinkExtractor(allow=r'/loupan/p_\w+/')
    # 获得详细页面的链接
    #detaillinks = LinkExtractor(allow=(r'loupan/p_\w+/$'))
    # 获得每一页的链接
    # pagelinks = LinkExtractor(allow=(r'loupan/pg\d+/'))
    rules = (
        Rule(citylink, process_links='city_links', callback='parse_item'),
    )
    #rules = (
    #    Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    #)
    # 对获得的城市链接进行拼接
    def city_links(self, links):
        for link in links:
            urls = link.url.split('.')
            if 'fang' not in urls:
                urls.insert(1, 'fang')
            link.url = '.'.join(urls) + '/loupan/pg1'
        return links

    def parse_item(self, response):
        # 获取到该城市的楼盘数量
        number = response.xpath('//div[@class="resblock-have-find"]/span[@class="value"]/text()').extract()[0]
        # 每页10条信息，获取总页数
        max_page = math.ceil(int(number) / 10)
        # 解析出楼盘详细页面的地址节点
        lis = response.xpath('//div[@class="resblock-list-container clearfix"]/ul[@class="resblock-list-wrapper"]/li')
        # 由于解析出来的链接是slug的，所以需要获得该网址的域名，因为每个城市的域名又不一样，所以进行处理，然后拼接
        base_url = response.url.split('/')[:3]
        # 将域名进行拼接
        base_url = '/'.join(base_url)
        for li in lis:
            try:
                # 解析出详细页面的slug
                link = li.xpath('./a/@href').extract()[0]
                # 将URL进行拼接
                detail_link = base_url + link
                # 回调域名进行请求解析
                yield scrapy.Request(url=detail_link, callback=self.detail_parse, encoding='utf-8', dont_filter=False)
            except IndexError as e:
                print(response.url, e.args)
                break
        # 提取出当前页面的页数
        page = re.search('/pg(\d+)', response.url)
        # 对页面进行+1
        next_page = int(page.group(1)) + 1
        # 如果页数小于等于总页数,将执行递归操作
        if next_page <= max_page:
            # 对页数进行替换
            next_url = re.sub('pg(\d+)','pg'+str(next_page), response.url)
            yield scrapy.Request(url=next_url, callback=self.parse_item, encoding='utf-8', dont_filter=False)

    def detail_parse(self, response):
        items = BeikeItem()
        try:
            # 获得城市信息
            city = response.xpath('//a[@class="s-city"]/text()').extract()[0]
            # 获得价格
            price = response.xpath('//div[@class="price"]//span/text()').extract()
            price = ''.join(price).replace(' ', '')
            # 获得标题
            title = response.xpath('//div[@class="title-wrap"]/div/h2/text()').extract()[0]
            # 获得地址
            address = response.xpath('//div[@class="middle-info animation"]/ul/li/span[@class="content"]/text()').extract()[1].strip()
            if address:
                address = address.replace(' ', '')
            else:
                address = response.xpath('//div[@class="middle-info animation"]/ul/li/span[@class="content"]/text()').extract()[0].strip()
            # 获取经纬度
            lngandlat = re.findall('data-coord="(.*?)"', response.text)[0]
            if lngandlat == ',':
                lngandlat = '没有地图标记'
            items ['city'] = city
            items['title'] = title
            items['price'] = price
            items['address'] = address
            items['lngandlat'] = lngandlat
            time.sleep(0.5)
            yield items

        except Exception as e:
            print(e.args)

#        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
#        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
