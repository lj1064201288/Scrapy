# -*- coding: utf-8 -*-
import scrapy
import re, time, random
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from DGitem.items import DGItem


class DgSpider(CrawlSpider):
    name = 'DG'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/html/top/report.shtml']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    # 获取页面的链接
    pagelinks = LinkExtractor(allow=(r'report?'))
    # 获取详细页面的链接
    detaillinks = LinkExtractor(allow=r'question/\d+/\d+.shtml')

    rules = (
        Rule(pagelinks, follow=True),
        Rule(detaillinks, callback='parse_item', follow=True),
    )


    def parse_item(self, response):
        print(response.text)
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()

        item = DGItem()

        title = response.xpath('//td/span[@class="niae2_top"]/text()').extract_first().replace('提问：', '')
        number = response.xpath('//td[@valign="middle"]/span[2]/text()').extract_first().strip().replace('编号:', '')
        content = response.xpath('//td[@class="txt16_3"]/text()').extract()
        try:
            content = ''.join(content).replace(' ', '').strip()
        except:
            content = 'None'
        status = response.xpath('//div[@class="wzy3_1"]/span/text()').extract_first()
        netfriendanddate = response.xpath('//div[@class="wzy3_2"]/span[1]/text()').extract_first()
        net_friend = re.findall(r'网友：(.*?) ', netfriendanddate)[0]
        date = re.findall(r'发言时间：(.*)', netfriendanddate)[0]

        item['title'] = title
        item['number'] = number
        item['content'] = content
        item['status'] = status
        item['net_friend'] = net_friend
        item['date'] = date
        yield item

        time.sleep(random.choice[0.1, 0.2, 0.25, 0.15, 0.75])
