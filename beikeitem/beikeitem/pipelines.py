# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook
from pymysql import connect
import settings



class BeikeitemPipeline(object):
    def process_item(self, item, spider):
        return item

class BeikePipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['城市', '标题', '价格', '地址', '经纬度'])

    def process_item(self, item, spider):
        line = list(item.values())
        print(item)
        self.ws.append(line)
        self.wb.save('beike.xlsx')
        return item

class BeikeMysqlPipeline(object):

    def __init__(self):
        self.name = settings.MYSQL_DB
        self.host = settings.MYSQL_HOST
        self.user = settings.MSQL_USER
        self.password = settings.MYSQL_PASSWORD
        self.port = settings.MYSQL_PORT
        self.table = settings.MYSQL_TABLE
        self.db = connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.name)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = r'INSERT INTO %s (%s) VALUES (%s)' % (self.table, keys, values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
            print('插入成功!{}'.format(data['title']))
            return item
        except Exception as e:
            self.db.rollback()
            print('插入失败!', e.args)

    def close_spider(self, spider):
        self.db.close()