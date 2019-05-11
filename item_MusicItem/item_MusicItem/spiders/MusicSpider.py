import time
import scrapy
from urllib.parse import quote
from item_MusicItem.items import MusicItem

class MusicSpider(scrapy.Spider):

    name = 'music'
    allowed_domains = ['music.163.com']
    base_url = 'https://music.163.com/#/discover/toplist?id='

    def start_requests(self):
        ids = ['19723756', '3779629', '2884035', '3778678', '991319590',
           '2408901803', '1978921795', '71385702', '2462790889',
           '10520166', '3812895', '60131', '71384707', '180106', '60198',
           '27135204', '11641012', '120001', '2323534945', '745956260',
           '2023401535', '2006508653', '21845217', '112463',
           '112504', '64016', '10169002', '1899724']
        for id in ids:
            url = self.base_url + quote(id)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        title = response.xpath('./td/div/div/div/span/a/b/@title')
        print(title)