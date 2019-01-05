from scrapy.item import Item, Field


class Good(Item):
    name = Field()
    price = Field()
    image_urls = Field()
    images = Field()
