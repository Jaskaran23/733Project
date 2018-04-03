# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WikipediaEventItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    day_of_week = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    news_header = scrapy.Field()
    # news_sub_header = scrapy.Field()
    # source -> [(source_name, source_url), (...), ...]
    source = scrapy.Field()
