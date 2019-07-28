# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymysql import connect


class TencentPipeline(object):
    def process_item(self, item, spider):
        return item


class MySqlPipeline(object):
    def __init__(self, db, user, host, port, password):
        self.db = db
        self.host = host
        self.user = user
        self.port = port
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db=crawler.settings.get('MYSQL_DB'),
            user=crawler.settings.get('MYSQL_USER'),
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_POST'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        self.database = connect(host=self.host, user=self.user, db=self.db, password=self.password, port=self.port, charset='utf8')
        self.cursor = self.database.cursor()

    def close_spider(self, spider):
        self.database.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.database.commit()
            print('插入成功!!!')
            return item
        except Exception as e:
            print(e.args)
            self.database.rollback()