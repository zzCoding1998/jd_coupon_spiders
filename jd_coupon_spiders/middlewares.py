# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import queue
import threading
import time

import requests
from scrapy import signals

# useful for handling different item types with a single interface
from scrapy.http import HtmlResponse
from scrapy.spidermiddlewares.httperror import HttpError

from utils.ChromeDriverHelper import ChromeDriverHelper
from utils.ProxyHelper import ProxyHelper


class JdCouponSpidersSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        spider.logger.info('through spider input!!!')
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.

        spider.logger.info('save item soon!!!')
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class JdCouponSpidersCouponHomeDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, concurrent_requests):
        self.queue = queue.Queue(concurrent_requests)
        self.flag = False
        for i in range(concurrent_requests):
            proxy = ProxyHelper.get_single_proxy()
            driver = ChromeDriverHelper.get_driver(proxy)
            self.queue.put(driver)
        logging.getLogger(__name__).info(__name__ + ":init drivers success. size: %d" % self.queue.qsize())

    def _get_driver(self):
        while not self.flag:
            self.flag = True
            if self.queue.qsize() == 0:
                proxy = ProxyHelper.get_single_proxy()
                driver = ChromeDriverHelper.get_driver(proxy)
                self.queue.put(driver)
            driver = self.queue.get(True, 50)
            self.flag = False
            return driver


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings['CONCURRENT_REQUESTS'])
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        driver = self._get_driver()
        try:
            driver.get(request.url)
            if 'cateId=' in request.url:
                # 将滚动条移动到页面的底部
                all_window_height = []  # 创建一个列表，用于记录每一次拖动滚动条后页面的最大高度
                all_window_height.append(
                    driver.execute_script("return document.body.scrollHeight;"))  # 当前页面的最大高度加入列表
                while True:
                    driver.execute_script("scroll(0,100000)")  # 执行拖动滚动条操作
                    time.sleep(3)
                    check_height = driver.execute_script("return document.body.scrollHeight;")
                    if check_height == all_window_height[-1]:  # 判断拖动滚动条后的最大高度与上一次的最大高度的大小，相等表明到了最底部
                        spider.logger.info("我已下拉完毕")
                        break
                    else:
                        all_window_height.append(check_height)  # 如果不想等，将当前页面最大高度加入列表。
                        spider.logger.info("我正在下拉")
            # 判断响应码
            body = driver.page_source
            self.queue.put(driver, True, 60)
            return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)
        except:
            driver.close()
            return HtmlResponse(request.url, body='', encoding='utf-8', request=request, status=500)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def close_spider(self, spider):
        while not self.queue.empty():
            self.queue.get().close()
        spider.logger.info('JdCouponSpidersCouponHomeDownloaderMiddleware: close drivers done!')


class ProxyMiddleware:
    def process_request(self, request, spider):
        proxy = ProxyHelper.get_single_proxy()
        if proxy != '':
            request.meta['proxy'] = proxy
        else:
            spider.logger.error('get single proxy failed!!!  please check!!!')
            request.meta['dont_filter'] = True
            return request

    def process_response(self, request, response, spider):
        if response.status != 200:
            spider.logger.error(f'status code error: {response.status}, url: {request.url}')
            raise HttpError(response)

        return response

    def process_exception(self, request, exception, spider):
        request.meta['dont_filter'] = True
        spider.logger.error(exception)
        return request
