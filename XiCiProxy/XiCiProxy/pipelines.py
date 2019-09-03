# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from XiCiProxy import settings
from pymysql import connect

class XiciproxyPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPieline(object):

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
        self.filtration_data(data['ipaddress'])
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = r'INSERT INTO %s (%s) VALUES (%s)'%(self.table, keys, values)
        try:
            decide = self.filtration_data(data['ipaddress'])
            if decide == True:
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
                print('插入成功!')
                return item
        except Exception as e:
            self.db.rollback()
            print('插入失败!', e.args)
    def filtration_data(self, ipaddress):
        sql = 'select * from {} where ipaddress="{}"'.format(self.table, ipaddress)
        result = self.cursor.execute(sql)
        print(ipaddress)
        if result:
            print('该地址已存在!插入失败！')
            return False
        else:
            return True


    def close_spider(self, spider):
        self.db.close()



