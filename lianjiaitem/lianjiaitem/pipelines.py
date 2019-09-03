# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from openpyxl import Workbook
from pymysql import connect
from lianjiaitem import settings


class LianjiaitemPipeline(object):
    def process_item(self, item, spider):
        return item

# 保存至Json格式
class LianjiaJsonPipeline(object):
    def __init__(self):
        self.file = open(r'.lianjia.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        content = content + '\n'
        self.file.write(content)
        return item

    def close_file(self, item, spider):
        self.file.close()
# 保存excel表格方式
class LianjiaExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['标题', '房屋地址', '房屋来源', '房屋链接', '租房方式', '房屋模型', '房屋面积', '房屋朝向', '发布时间', '房屋id', '房屋价格', '周围设施', '经纪人', '发布', '入住', '租期', '看房', '楼层', '电梯', '车位', '用水', '用电', '燃气', '描述'])

    def process_item(self, item, spider):
        line = list(item.values())
        self.ws.append(line)
        self.wb.save('lianjia.xlsx')

        return item

class LianjiaMysqlPipeline(object):

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
