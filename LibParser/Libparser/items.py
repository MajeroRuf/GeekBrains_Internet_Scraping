# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LibparserItem(scrapy.Item):

    name = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
    price_old = scrapy.Field()
    price_new = scrapy.Field()
    author = scrapy.Field()
    rate = scrapy.Field()