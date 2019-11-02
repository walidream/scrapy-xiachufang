# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json

from scrapy.exporters import JsonItemExporter

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class XiachufangPipeline(object):
    def process_item(self, item, spider):
        return item


class PostImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value['path']

        item['front_image_url'] = image_file_path
        return item

class JsonWithEncodingPipeline(object):
    #自定义
    def __init__(self):
        self.file = codecs.open('post.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipeline(object):
    #scrapy自带方法
    def __init__(self):
        self.file = open('postExport.json','wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    
    def process_item(self,item, spider):
        self.exporter.export_item(item)
        return item

class MysqlPipelin(object):
    
    def __init__(self):
        self.conn = MySQLdb.connect('47.101.151.61','wali','123456','scrapy',charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()
    
    def process_item(self,item,spider):
        insert_sql = """
            INSERT INTO post(`post_id`,`post_url`,`title`,`cover`,`front_image_url`,`author`,`avatar`,`score`,`cook`) 
            VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item['post_id'],item['post_url'],item['title'],item['cover'],item['front_image_url'],item['author'],item['avatar'],item['score'],item['cook']))
        self.conn.commit()


class MysqlTwistedPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        myparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DB'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASS'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", ** myparms)
        return cls(dbpool)
    
    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    #处理异常
    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
            INSERT INTO post(`post_id`,`post_url`,`title`,`cover`,`front_image_url`,`author`,`avatar`,`score`,`cook`) 
            VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)
        """
        cursor.execute(insert_sql,(item['post_id'],item['post_url'],item['title'],item['cover'],item['front_image_url'],item['author'],item['avatar'],item['score'],item['cook']))
        



















