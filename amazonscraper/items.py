import scrapy


class AmazonItem(scrapy.Item):
    search_term= scrapy.Field()
    specific_brand = scrapy.Field()
    date = scrapy.Field()
    min_price = scrapy.Field()
    max_price = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    available = scrapy.Field()
    rating = scrapy.Field()
    num_reviews = scrapy.Field()
    url = scrapy.Field()