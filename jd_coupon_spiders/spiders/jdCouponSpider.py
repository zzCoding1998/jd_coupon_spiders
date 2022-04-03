import datetime
import re

import scrapy

from jd_coupon_spiders.items import jdCouponGoodsCategory, jdCoupon


class JdcouponspiderSpider(scrapy.Spider):
    name = 'jdCouponSpider'
    allowed_domains = ['jd.com']
    start_urls = ['https://a.jd.com/']

    def parse(self, response):
        cat_items = response.xpath('//a[contains(@class,"cate-item")]')

        for cat in cat_items:
            cat_id = cat.xpath('./@data-cateid').get()
            cat_name = cat.xpath('./text()').get()
            yield jdCouponGoodsCategory(cat_id=cat_id, cat_name=cat_name)
            url = "https://a.jd.com/?cateId=" + str(cat_id)
            yield scrapy.Request(url, callback=self.parse_coupons, meta={'cat_id': cat_id})

    def parse_coupons(self, response):
        coupon_items = response.xpath('//div[contains(@class, "quan-item")]')
        for coupon_item in coupon_items:
            jd_coupon = jdCoupon()
            jd_coupon['crawl_date'] = datetime.date.today()
            jd_coupon['cat_id'] = response.request.meta['cat_id']
            jd_coupon['jump_url'] = coupon_item.xpath(
                './div[contains(@class, "q-ops-jump")]/div[contains(@class, "q-opbtns")]/a/@href').get()
            jd_coupon['batch_id'] = jd_coupon['jump_url'].split("=")[-1]
            jd_coupon['rule_key'] = coupon_item.xpath(
                './div[contains(@class, "q-ops-box")]//div[contains(@class, "q-opbtns")]/a/@rel').get()
            jd_coupon['denomination'] = float(coupon_item.xpath(
                './div[contains(@class, "q-type")]//div[contains(@class, "q-price")]/strong/text()').get())
            discount_unit_str = coupon_item.xpath(
                './div[contains(@class, "q-type")]//div[contains(@class, "q-price")]/span[@class="zh-txt"]/text()').get()
            jd_coupon['discount_unit'] = 2 if discount_unit_str is not None and '折' in discount_unit_str else 1
            jd_coupon['quota'] = coupon_item.xpath(
                './div[contains(@class, "q-type")]//div[contains(@class, "q-range")]/span[@title]/text()').get()
            jd_coupon['limit_str'] = coupon_item.xpath(
                './div[contains(@class, "q-type")]//div[contains(@class, "q-price")]/span[@data-tips]/text()').get()
            jd_coupon['limit_amount'] = float(re.findall(r'([0-9]*\.?[0-9]+)', jd_coupon['limit_str'])[0])
            if jd_coupon['discount_unit'] == 2:
                jd_coupon['need_pay_amount'] = round(jd_coupon['limit_amount'] * jd_coupon['denomination'] / 10, 4)
                jd_coupon['discount_rate'] = jd_coupon['denomination']
            else:
                jd_coupon['need_pay_amount'] = jd_coupon['limit_amount'] - jd_coupon['denomination']
                jd_coupon['discount_rate'] = round(jd_coupon['need_pay_amount'] / jd_coupon['limit_amount'], 4)
            yield jd_coupon
