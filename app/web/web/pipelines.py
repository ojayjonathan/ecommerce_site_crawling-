# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import re
import MySQLdb
from scrapy.exceptions import NotConfigured

class WebPipeline:
    def process_item(self, item, spider):
        item['price'] = re.findall('\d+',re.sub(',','',item['price']))[0]
        item['prev_price']=re.findall('\d+',re.sub(',','',item['prev_price']))[0]
        item['rating']=re.findall('\d+',item['rating'])[0]
        item['reviews'] = re.findall('\d+',item['reviews'])[0]
        item['per_discount'] = re.findall('\d+',item['per_discount'])[0]
        item['category'] = re.sub('&' ,'and', item['category'])
        item['sub_category'] = re.sub('&', 'and', item['sub_category'])
        return item


class JsonWriterPipeline(object):
     def __init__(self):
         self.file = open('file.json','wb')
     def process_item(self, item,spider):
          line = json.dumps(dict(item))+'\n'
          self.file.write(line)
          return item

class DatabasePipeline(object):
    def __init__(self, db,user, password,host):
        self.user=user
        self.db = db
        self.password = password
        self.host = host

    @classmethod
    def from_crawler(cls,crawler):
        db_settings = crawler.settings.getdict('DB_SETTINGS')
        if not db_settings:
            raise NotConfigured
        return cls(db_settings['db'],db_settings['user'],db_settings['password'],
        db_settings['host'])
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(db=self.db,
                               user=self.user, passwd=self.password,
                               host=self.host,
                               charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self, item,spider):
        #self.cursor.excecute(table)
        sql = "INSERT INTO bestdeal (price,prev_price,item_link,image_src,description,\
            per_discount,reviews,rating,category,sub_category) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"    
        self.cursor.execute(sql,
                             (
                                 int(item.get('price')),
                                 int(item.get('prev_price')),
                                 item.get('item_link'),
                                 item.get('image_src'),
                                 item.get('description'),
                                 int(item.get('per_discount')),
                                 int(item.get('reviews')),
                                 int(item.get('rating')),
                                 item.get('category'),
                                 item.get('sub_category')
                             ))    
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.conn.close()         
