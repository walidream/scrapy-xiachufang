# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

from xiachufang.items import XiachufangItem,PostItemLoader
from xiachufang.utils.common import get_md5

from scrapy.loader import ItemLoader


class XcfSpider(scrapy.Spider):
    name = 'xcf'
    allowed_domains = ['xiachufang.com']
    start_urls = ['https://www.xiachufang.com/category/731/']

    def parse(self, response):
        #获取文章url
        post_urls = response.css('.ing-recipe .normal-recipe-list li>.recipe>a::attr(href)').getall()

        for post_url in post_urls:
            yield Request(url = parse.urljoin(response.url, post_url), callback= self.parse_detail)

        #判断是否有下一页
        next_url = response.css('.ing-recipe .pager a.next::attr(href)').get()
        if next_url:
            yield Request(url= parse.urljoin(response.url, next_url), callback= self.parse)

    def parse_detail(self,response):
        l = PostItemLoader(item= XiachufangItem(), response=response)
        l.add_value('post_url', response.url)
        l.add_css('post_id', get_md5(response.url))
        l.add_css('title', '.main-panel h1.page-title::text')
        l.add_css('cover', '.main-panel .cover img::attr(src)')
        l.add_css('author', '.main-panel .author span[itemprop="name"]::text')
        l.add_css('avatar', '.main-panel .author img::attr(src)')
        l.add_css('score', '.main-panel .score .number::text')
        l.add_css('cook', '.main-panel .cooked .number::text')
        
        l = l.load_item()
        yield l








