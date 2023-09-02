from amazonscraper.config import get_search_term, get_specific_brand, get_price_range
from scrapy.linkextractors import LinkExtractor
from amazonscraper.items import AmazonItem
from scrapy.spiders import Rule
from datetime import date
import scrapy


class AmazonSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["www.amazon.com"]
    scraped_date = date.today()

    search_term = get_search_term()
    specific_brand = get_specific_brand()
    min_price, max_price = get_price_range()
    custom_settings = {
        "ITEM_PIPELINES": {
            "amazonscraper.pipelines.AmazonItemPipeline": 100,
            "amazonscraper.pipelines.BrandCheckPipeline": 200,
            "amazonscraper.pipelines.PriceRangeCheckPipeline": 300,
            "amazonscraper.pipelines.DuplicateCheckPipeline": 500,
            "amazonscraper.pipelines.SaveToMySQLPipeline": 900
        }
    }    
    if input("Restrict mode? (y/n): ").lower().strip() == "y":
        custom_settings["ITEM_PIPELINES"]["amazonscraper.pipelines.ProductCheckPipeline"] = 400
    
    start_urls = [f'https://www.amazon.com/s?k={search_term.replace(" ", "+")}']
    rules = (
        Rule(LinkExtractor(allow=r'\/dp\/'), callback='parse_amazon_page', follow=True),
    )
    
    def parse(self, response):
        urls = response.css("h2 a::attr(href)").getall()
        for url in urls:
            relative_url = 'https://www.amazon.com' + url
            yield scrapy.Request(relative_url, callback=self.parse_product_page)

        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.amazon.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_product_page(self, response):
        item = AmazonItem()

        item['search_term'] = self.search_term
        item['specific_brand'] = self.specific_brand
        item['date'] = self.scraped_date
        item['min_price'] = self.min_price
        item['max_price'] = self.max_price
        
        # Extract the product name
        item['name'] = response.xpath("//span[@id='productTitle']/text()").get("")
        # Extract the product brand
        item['brand'] = self.parse_brand(response)
        # Extract the product price
        item['price'] = self.parse_price(response)
        # Extract the product rating
        item['rating'] = response.xpath("//div[@id='customerReviews']//span[@data-hook='rating-out-of-text']/text()").get("0")
        # Extract the product number of reviews
        item['num_reviews'] = response.xpath("//div[@id='customerReviews']//div[@data-hook='total-review-count']//span/text()").get("0")
        # Set the product availability to True by default
        item['available'] = True
        # Product url
        item['url'] = response.url

        yield item

    def parse_price(self, response):
        price = response.xpath("span[@class='a-price']//span[@aria-hidden='true']/text()[normalise-space()]").get("")
        if not price:
            price = response.css(".a-price .a-offscreen::text").get("0")
        return price

    def parse_brand(self, response):
        # Locate the 'Brand' span tag
        brand_span_xpath = '//div[@id="productOverview_feature_div"]//table//td[@class="a-span3"]//span/text()[normalize-space()="Brand"]'

        brand_span_text = response.xpath(brand_span_xpath).get(default="Unknow")
        if 'brand' in brand_span_text.lower():
            # Get the subsequent <span> tag after the 'Brand' span tag
            subsequent_span_xpath = f'{brand_span_xpath}/following::span[1]/text()[normalize-space()]'
            subsequent_span_text = response.xpath(subsequent_span_xpath).get()
            if subsequent_span_text:
                brand_name = subsequent_span_text
                return brand_name
        if brand_span_text == 'Unknow':
            bylineInfo_feature_div = response.xpath('//a[@id="bylineInfo"]/text()[normalize-space()]').get()
            return bylineInfo_feature_div
