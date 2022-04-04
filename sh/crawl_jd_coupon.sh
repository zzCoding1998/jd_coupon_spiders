#!/usr/bin/env bash
LOCK_FILE=/tmp/crawl_jd_coupon2.lock
exec 99>"$LOCK_FILE"
flock -n 99
if [ "$?" != 0 ]; then
    echo "$0 already running"
    exit 1
fi
cd /app && scrapy crawl jdCouponSpider
