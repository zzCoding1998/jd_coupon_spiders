# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime

import pymysql as pymysql

from jd_coupon_spiders.items import jdCouponGoodsCategory, jdCoupon


class JdCouponSpidersPipeline:

    def __init__(self, host, port, user, password, database):
        self.db = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST', 'localhost'),
            port=crawler.settings.get('MYSQL_PORT', 3306),
            user=crawler.settings.get('MYSQL_USER', 'root'),
            password=crawler.settings.get('MYSQL_PASSWORD', '123456'),
            database=crawler.settings.get('MYSQL_DATABASE', 'jd_spider')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database)
        try:
            cursor = self.db.cursor()
            today = datetime.date.today()
            cursor.execute(f"delete from jd_coupons where crawl_date = '{today}'")
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            spider.logger.error('delete jd_coupons with today error!!!')
            spider.logger.error(e)

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        if isinstance(item, jdCouponGoodsCategory):
            try:
                cursor = self.db.cursor()
                sql = f'''
                    insert ignore into jd_coupon_category(cat_id,cat_name) values("{item['cat_id']}","{item['cat_name']}");
                '''

                # spider.logger.info(sql)
                cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                spider.logger.error('insert jd_coupon_category error!!!')
                spider.logger.error(e)
                spider.logger.error(item)
        elif isinstance(item, jdCoupon):
            try:
                cursor = self.db.cursor()
                sql = f'''
                    insert ignore into jd_coupons(crawl_date,batch_id,rule_key,jump_url,denomination,quota,limit_amount,
                    limit_str,need_pay_amount,discount_rate,discount_unit,cat_id) values("{item['crawl_date']}",
                    "{item['batch_id']}","{item['rule_key']}","{item['jump_url']}","{item['denomination']}",
                    "{item['quota']}","{item['limit_amount']}","{item['limit_str']}","{item['need_pay_amount']}",
                    "{item['discount_rate']}","{item['discount_unit']}","{item['cat_id']}");
                '''
                spider.logger.info(sql)
                cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                spider.logger.error('insert jd_coupons error!!!')
                spider.logger.error(e)
                spider.logger.error(item)
        return item
