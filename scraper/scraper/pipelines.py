# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ScraperPipeline(object):
    def process_item(self, item, spider):
        # dictitem = dict(item)
        # with open(f"fetched/{dictitem['manga']}/{dictitem['chapter']}.json", 'a+') as log:
            # line = json.dumps(dictitem) + "\n"
        with open(f"fetched/{item['manga']}/{item['chapter']}.json", 'a+') as log:
            # line = json.dumps(item) + "\n"
            # log.write(line)
            log.write(json.dumps(dict(item)) + "\n")
        return item
