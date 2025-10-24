# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LinkGraphItem(Item):
    pagina_origem = Field()
    links_destino = Field()

