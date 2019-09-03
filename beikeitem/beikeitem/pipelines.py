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

    # 初始化MySQL的信息
    def __init__(self):
        self.name = settings.MYSQL_DB
        self.host = settings.MYSQL_HOST
        self.user = settings.MSQL_USER
        self.password = settings.MYSQL_PASSWORD
        self.port = settings.MYSQL_PORT
        self.table = settings.MYSQL_TABLE
        self.db = connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.name)
        self.cursor = self.db.cursor()

    # 对获得的数据进行保存处理
    def process_item(self, item, spider):
        # 将数据转为字典类型，方便存储
        data = dict(item)
        # 对字典中的键转化成列表，方便插入MySQL里面
        keys = ', '.join(data.keys())
        # 将值转化成格式化符，方便后续拼接存储
        values = ', '.join(['%s'] * len(data))
        sql = r'INSERT INTO %s (%s) VALUES (%s)' % (self.table, keys, values)
        try:
            # 执行sql语句插入操作
            self.cursor.execute(sql, tuple(data.values()))
            # 将插入的数据提交
            self.db.commit()
            print('插入成功!{}'.format(data['title']))
            return item
        except Exception as e:
            # 如果出现异常，回滚，然后打印异常信息
            self.db.rollback()
            print('插入失败!', e.args)
    # 关闭数据库
    def close_spider(self, spider):
        self.db.close()