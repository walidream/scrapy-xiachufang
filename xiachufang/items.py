# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst


def deal_title_strip(title):
    title = title.strip()
    return title

def score_conversion_type(score):
    score = score if score else 0
    return float(score)

def cook_converion_type(cook):
    cook = cook if cook else 0
    return int(cook)
    

class PostItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class XiachufangItem(scrapy.Item):  

    post_url = scrapy.Field()
    post_id = scrapy.Field()
    title = scrapy.Field(
        input_processor = MapCompose(deal_title_strip)
    )
    cover = scrapy.Field()
    front_image_url = scrapy.Field()
    author = scrapy.Field()
    avatar = scrapy.Field()
    score = scrapy.Field(
        input_processor = MapCompose(score_conversion_type)
    )
    cook = scrapy.Field(
        input_processor = MapCompose(cook_converion_type)
    )
