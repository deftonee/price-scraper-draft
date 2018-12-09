# from urllib.parse import unquote
from scrapy.spiders import Spider, Request


items_path = './/div[contains(@class, "sel-product-tile-main")]'
name_path = 'div/div[@class="c-product-tile__description-wrapper"]/h4/@title'
price_path = 'div/div/div[@class="c-pdp-price__current"]/text()'
next_page_path = '//a[contains(@class, "c-pagination__next")]/@href'


class PrintReceiver:
    buffer = ''

    def write(self, *strings):
        self.buffer += ''.join(strings)

    def get_result(self):
        return self.buffer


def convert(string):
    converter = PrintReceiver()
    print(string, sep='', end='', file=converter)
    return converter.get_result()


class PricesSpider(Spider):
    name = "prices"
    allowed_domains = ['mvideo.ru']

    def start_requests(self):
        url_template = 'https://www.mvideo.ru/komputernaya-tehnika/sistemnye-bloki-80//f/page=%s'
        for i in range(1, 22):
            yield Request(url=url_template % i, callback=self.parse)

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)

        for item in response.xpath(items_path):
            result = {}
            result['name'] = convert(item.xpath(name_path).extract_first())
            result['price'] = convert(item.xpath(price_path).extract_first())
            yield result

        next_page = response.xpath(next_page_path).extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
