# from urllib.parse import unquote
from scrapy.spiders import Spider

from items import Good

items_path = './/div[contains(@class, "sel-product-tile-main")]'
name_path = 'div/div[@class="c-product-tile__description-wrapper"]/h4/@title'
price_path = 'div/div/div[@class="c-pdp-price__current"]/text()'
pic_path = 'div[@class="c-product-tile-picture"]/div/a/div/div/img/@data-original'
next_page_path = '//a[contains(@class, "c-pagination__next")]/@href'


class PricesSpider(Spider):
    name = "prices"
    allowed_domains = ['mvideo.ru']
    start_urls = [
        'https://www.mvideo.ru/komputernaya-tehnika/sistemnye-bloki-80/',
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy.pipelines.images.ImagesPipeline': 1
        },
        'IMAGES_STORE':  (
            '/Users/konstantin/PycharmProjects/priceScraper/downloads'
        ),
    }

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)

        for item in response.xpath(items_path):

            goods = Good()
            goods['name'] = item.xpath(name_path).extract_first()
            goods['price'] = item.xpath(price_path).extract_first()
            goods['image_urls'] = [
                f'http:{x}' for x in item.xpath(pic_path).extract()]
            yield goods

        next_page = response.xpath(next_page_path).extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
