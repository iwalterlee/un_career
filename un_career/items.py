# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy4Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    level = scrapy.Field()
    job_network = scrapy.Field()
    job_family = scrapy.Field()
    department = scrapy.Field()
    location = scrapy.Field()
    deadline = scrapy.Field()
    pass
