# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from json import dumps


class ScraperPipeline(object):
    """
        Saves the fetched info into a json file
    """
    def process_item(self, item, spider):
        with open(item['json_path'], 'a+') as log:
            log.write(dumps(dict((k, item[k]) for k in ['chapter', 'page', 'img'])) + "\n")
        return item
