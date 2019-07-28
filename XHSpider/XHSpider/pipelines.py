# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class XhspiderPipeline(object):
    def process_item(self, item, spider):
        return item



class XiaoHuaPipeline(object):
    def __init__(self):
        self.file = open('xiaohua.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        content = content + '\n'
        self.file.write(content)

        return item

    def close_file(self, item, spider):
        self.file.close()