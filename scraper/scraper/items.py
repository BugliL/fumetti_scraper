# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MangaPage(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    json_path = scrapy.Field()
    manga = scrapy.Field()
    chapter = scrapy.Field()
    page = scrapy.Field()
    img = scrapy.Field()
