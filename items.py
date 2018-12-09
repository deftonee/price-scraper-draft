from scrapy.item import Item, Field


class Goods(Item):
    name = Field()
    price = Field()
