# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class jdCouponGoodsCategory(scrapy.Item):
    cat_id = scrapy.Field()
    cat_name = scrapy.Field()


class jdCoupon(scrapy.Item):
    crawl_date = scrapy.Field()
    batch_id = scrapy.Field()
    rule_key = scrapy.Field()
    jump_url = scrapy.Field()
    denomination = scrapy.Field()
    quota = scrapy.Field()
    limit_amount = scrapy.Field()
    limit_str = scrapy.Field()
    need_pay_amount = scrapy.Field()
    discount_rate = scrapy.Field()
    discount_unit = scrapy.Field()
    cat_id = scrapy.Field()
