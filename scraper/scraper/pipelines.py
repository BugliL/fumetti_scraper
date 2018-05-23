# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from json import dumps
from os.path import exists
from os import mkdir


class ScraperPipeline(object):
    # pages_list = []
    #
    # def open_spyder(self, item, spider):
    #     if not exists('fetched'):
    #         mkdir('fetched')
    #     print('+'*10, item)
    #
    # def close_spyder(self, item, spider):
    #     print('+'*10, len(self.pages_list))
    #     print('+'*10, item)

    def process_item(self, item, spider):
        # dictitem = dict(item)
        # with open(f"fetched/{dictitem['manga']}/{dictitem['chapter']}.json", 'a+') as log:
            # line = json.dumps(dictitem) + "\n"
        # with open(f"fetched/{item['manga']}/{item['chapter']}.json", 'a+') as log:
        # with open(f"fetched/{item['manga']}.json", 'a+') as log:
            # line = json.dumps(item) + "\n"
            # log.write(line)
            # log.write(dumps(dict(item)) + "\n")
            # self.pages_list.append(dict(item))
        with open(item['json_path'], 'a+') as log:
            log.write(dumps(dict((k, item[k]) for k in ['chapter', 'page', 'img'])) + "\n")
        return item
