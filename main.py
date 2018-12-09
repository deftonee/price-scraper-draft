# from urllib.parse import unquote
from scrapy.spiders import Spider

from items import Goods

items_path = './/div[contains(@class, "sel-product-tile-main")]'
name_path = 'div/div[@class="c-product-tile__description-wrapper"]/h4/@title'
price_path = 'div/div/div[@class="c-pdp-price__current"]/text()'
next_page_path = '//a[contains(@class, "c-pagination__next")]/@href'


class PricesSpider(Spider):
    name = "prices"
    allowed_domains = ['mvideo.ru']
    start_urls = [
        'https://www.mvideo.ru/komputernaya-tehnika/sistemnye-bloki-80/',
    ]

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)

        for item in response.xpath(items_path):

            goods = Goods()
            goods['name'] = item.xpath(name_path).extract_first()
            goods['price'] = item.xpath(price_path).extract_first()
            yield goods

        next_page = response.xpath(next_page_path).extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
