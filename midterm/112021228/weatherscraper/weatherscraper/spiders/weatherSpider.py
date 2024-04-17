import scrapy
from dataclasses import dataclass
from pprint import pprint

@dataclass
class Weather:
    date:str
    high_temperature: int
    low_temperature: int
    weather_desc: str


class WeatherspiderSpider(scrapy.Spider):
    name = "weatherSpider"
    allowed_domains = ["weather.com"]
    start_urls = ["https://weather.com/weather/tenday/l/51aa95c773902d7614fdbac99637315ed8f99a0a0ec624f9b5b493b53a4d8dbc?unit=m"]


    def parse(self, response):
        # predicted = response.css('summary.Disclosure--Summary--3GiL4')
        summary_list=response.css('div[data-testid=DetailsSummary]')
        weather_list = []
        for idx, item in enumerate(summary_list):
            if(idx==0):
                continue
            weather_item = Weather(
                item.css('h3::text').get(),
                int(item.css('span[data-testid=TemperatureValue]::text').get()),
                int(item.css('span.DetailsSummary--lowTempValue--2tesQ::text').get()),
                item.css('div.DetailsSummary--condition--2JmHb').css('title::text').get()
            )
            weather_list.append(weather_item)

        pprint(weather_list)
        
            


