import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from fortekz.items import Article
import requests
import json


class fortekzSpider(scrapy.Spider):
    name = 'fortekz'
    start_urls = ['https://forte.kz/news']

    def parse(self, response):
        json_response = json.loads(requests.get("https://forte.kz/page-data/news/page-data.json").text)
        articles = json_response["result"]["pageContext"]["posts1"]["nodes"]
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article['title']
            date = article['created_at'][:10]
            content = article['content']

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()
