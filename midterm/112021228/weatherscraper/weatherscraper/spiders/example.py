import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://weather.com/weather/tenday/l/51aa95c773902d7614fdbac99637315ed8f99a0a0ec624f9b5b493b53a4d8dbc?unit=m"]

    def parse(self, response):
        pass
