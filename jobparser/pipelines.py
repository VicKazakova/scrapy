# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            result_salary = self.process_salary(item.get('salary'))
        else:
            result_salary = 123  # smth
        item['salary_min'] = result_salary[0]
        item['salary_max'] = result_salary[1]
        item['currency'] = result_salary[2]
        # del item['salary']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        return [0, 1, 2]
