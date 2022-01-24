# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import unicodedata


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            self.process_hhru(item)
        elif spider.name == 'sjru':
            self.process_sjru(item)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_hhru(self, item):
        # item['_id'] = item['url'].split('/')[4]
        if 'до ' in item['salary']:
            item['salary_min'] = None
            salary_max = unicodedata.normalize('NFKD', str(item['salary'][1]))
            item['salary_max'] = int(salary_max.replace(' ', ''))
            item['currency'] = item['salary'][3]
        elif 'от ' in item['salary']:
            if ' до ' in item['salary']:
                salary_min = unicodedata.normalize('NFKD', str(item['salary'][1]))
                item['salary_min'] = int(salary_min.replace(' ', ''))
                salary_max = unicodedata.normalize('NFKD', str(item['salary'][3]))
                item['salary_max'] = int(salary_max.replace(' ', ''))
                item['currency'] = item['salary'][5]
            else:
                salary_min = unicodedata.normalize('NFKD', str(item['salary'][1]))
                item['salary_min'] = int(salary_min.replace(' ', ''))
                item['salary_max'] = None
                item['currency'] = item['salary'][3]
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['currency'] = None
        del item['salary']
        return item

    def process_sjru(self, item):
        item['_id'] = item['url'].split('-')[-1].replace('.html', '')
        if 'По договорённости' in item['salary']:
            item['salary_min'] = None
            item['salary_max'] = None
            item['currency'] = None
        elif 'от' in item['salary']:
            salary_min = unicodedata.normalize('NFKD', str(item['salary'][2]).replace('руб.', ''))
            item['salary_min'] = int(salary_min.replace(' ', ''))
            item['salary_max'] = None
            item['currency'] = item['salary'][2][-4:]
        elif 'до' in item['salary']:
            item['salary_min'] = None
            salary_max = unicodedata.normalize('NFKD', str(item['salary'][2]).replace('руб.', ''))
            item['salary_max'] = int(salary_max.replace(' ', ''))
            item['currency'] = item['salary'][2][-4:]
        else:
            salary_min = unicodedata.normalize('NFKD', str(item['salary'][0]).replace('руб.', ''))
            salary_max = unicodedata.normalize('NFKD', str(item['salary'][1]).replace('руб.', ''))
            item['salary_min'] = int(salary_min.replace(' ', ''))
            item['salary_max'] = int(salary_max.replace(' ', ''))
            item['currency'] = item['salary'][3]
        del item['salary']
        return item
