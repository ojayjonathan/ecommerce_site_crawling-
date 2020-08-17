# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class WebItem(scrapy.Item):
     category = scrapy.Field()
     sub_category = scrapy.Field()
     price = scrapy.Field()
     prev_price = scrapy.Field()
     item_link = scrapy.Field()
     image_src = scrapy.Field()
     per_discount = scrapy.Field()
     rating = scrapy.Field()
     reviews = scrapy.Field()
     description = scrapy.Field()



