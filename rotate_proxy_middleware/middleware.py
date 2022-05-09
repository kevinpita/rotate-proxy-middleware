import random
import time

import requests
import logging

log = logging.getLogger("scrapy.proxies")


class RotateProxyMiddleware:
    def __init__(self, settings):
        self.restart_url = settings.get("RESTART_URL")
        log.warning(self.restart_url)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_input(self, response, spider):
        proxy = response.meta["proxy"]
        if (
            response.status != 200
            and response.status != 301
            and response.status != 302
            and response.status != 404
        ):
            spider.crawler.stats.inc_value("restarted_proxies")
            log.warning("-*/" * 100)
            log.warning(response.status)
            log.warning("Proxy {} is dead, restarting it".format(proxy))
            log.warning("-*/" * 100)
            restarted = False
            while not restarted:
                log.debug(self.restart_url + proxy)
                request_response = requests.get(
                    self.restart_url + proxy.split("//")[1]
                ).json()
                if request_response["status"] == "true":
                    restarted = True
                elif request_response["msg"] == "reset_too_much":
                    restarted = True
            log.warning("-*/" * 100)
            log.warning("Proxy {} is now alive".format(proxy))
            log.warning("-*/" * 100)

    def process_spider_exception(self, response, exception, spider):
        log.debug("-*PROXY/" * 100)
        log.debug(exception.__class__.__name__)
        log.debug("-*PROXY/" * 100)
        if exception.__class__.__name__ == "TunnelError":
            spider.crawler.stats.inc_value("proxy_error")
            log.warning("-*/" * 100)
            log.warning("Proxy {} failed, restarting it".format(response.meta["proxy"]))
            time.sleep(5)
            log.warning("-*/" * 100)
        self.process_spider_input(response, spider)


class RandomProxy:
    def __init__(self, settings):
        self.proxy_list = settings.get("PROXY_LIST")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        proxy_address = random.choice(list(self.proxy_list))
        request.meta["proxy"] = proxy_address
