# -*- coding: utf-8 -*-
import scrapy
from XiCiProxy.items import XcproxyItem


def judge(info):
    try:
        info = info[0].replace(' ', '')
    except:
        info = '未知'

    return info

class XcspiderSpider(scrapy.Spider):
    name = 'Xcspider'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    def parse(self, response):
        items_1 = response.xpath("//tr[@class='odd']")
        items_2 = response.xpath("//tr[@class='']")
        items = items_1 + items_2
        infos = XcproxyItem()
        for item in items:
            # 获取国家图片链接
            country = item.xpath('./td[@class="country"]/img/@src').extract()
            country = judge(country)
            # 获取ipaddress
            ipadderss = item.xpath('./td[2]/text()').extract()
            ipadderss = judge(ipadderss)
            # 获取端口号
            port = item.xpath('./td[3]/text()').extract()
            port = judge(port)
            # 获取服务器地址
            serveraddr = item.xpath('./td[4]/text()').extract()
            serveraddr = judge(serveraddr)
            # 是否匿名
            isanonymous = item.xpath('./td[5]/text()').extract()
            isanonymous = judge(isanonymous)
            # 协议类型
            type = item.xpath('./td[6]/text()').extract()
            type = judge(type)
            # 获取存活时间alivetime
            alivetime = item.xpath('./td[7]/text()').extract()
            alivetime = judge(alivetime)
            # 获取验证时间
            verifictiontime = item.xpath('./td[8]/text()').extract()
            verifictiontime = judge(verifictiontime)

            infos['country'] = country
            infos['ipaddress'] = ipadderss
            infos['port'] = port
            infos['serveraddr'] = serveraddr
            infos['isanonymous'] = isanonymous
            infos['type'] = type
            infos['alivetime'] = alivetime
            infos['verifictiontime'] = verifictiontime

            yield infos


