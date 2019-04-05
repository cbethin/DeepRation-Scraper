# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ResourcesPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient('mongodb://general:enter1234@deeprationcluster-shard-00-00-vaiyq.mongodb.net:27017,deeprationcluster-shard-00-01-vaiyq.mongodb.net:27017,deeprationcluster-shard-00-02-vaiyq.mongodb.net:27017/test?ssl=true&replicaSet=DeepRationCluster-shard-0&authSource=admin&retryWrites=true')
        self.db = connection['resources']
        self.collection = self.db['items']

    def process_item(self, item, spider):
        self.collection.update_one(
            item,
            { '$set': item },
            upsert=True
        )