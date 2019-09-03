# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaitemItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LianjiaItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 地址
    house_address = scrapy.Field()
    # 房屋来源
    house_source = scrapy.Field()
    # 详细链接
    house_href = scrapy.Field()
    # 房屋租赁方式
    house_typ = scrapy.Field()
    # 房间样式
    house_mode = scrapy.Field()
    # 面积
    house_area = scrapy.Field()
    # 朝向
    house_orient= scrapy.Field()
    # 上架时间
    putaway_time = scrapy.Field()
    # 房子编号
    house_id = scrapy.Field()
    # 价格
    house_price = scrapy.Field()
    # 附近内容
    aside_content = scrapy.Field()
    # 经纪人
    broker = scrapy.Field()
    # 发布
    issue = scrapy.Field()
    # 入住
    cheak = scrapy.Field()
    # 租期
    tenancy_term = scrapy.Field()
    # 看房
    look_house = scrapy.Field
    # 楼层
    floor = scrapy.Field()
    # 电梯
    elevator = scrapy.Field()
    # 车位
    stall = scrapy.Field()
    # 用水
    water = scrapy.Field()
    # 用电
    electro = scrapy.Field()
    # 燃气
    fuel_gas = scrapy.Field()
    # 房屋说明
    house_infos = scrapy.Field()

