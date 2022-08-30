# use of previous sandbox : https://github.com/g0thier/iTunes-Store-Scrapy/blob/main/Script05.py

import json
import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):

    # Name of your spider
    name = "weatherbit"
    
    # Url to start your spider from 
    start_urls = ['https://www.weatherbit.io/api/codes']


    # Recherche Requête 
    def parse(self, response):

        print('HTTP status normal 200 :')
        print(response.status)

        quotes = response.xpath("/html/body/div/div/div/table/tbody/tr")

        for quote in quotes:
            
            code = quote.xpath('td[1]/text()').get()
            description = quote.xpath('td[2]/text()').get()

            # fix str issue 
            weather_code = int(code.replace(r'\D+', ''))

            yield {
                'weather_code' : weather_code, 
                'description': description
                }

try: 
    parent_dir = os.path.abspath(os.path.split(__file__)[0])
    folder_name = 'src'
    path = os.path.join(parent_dir, folder_name)
    os.mkdir(path)
except:
    pass

# Name of the file where the results will be saved
filename = "weather_code_description.json"

# Settings Crawler 
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'LOG_LEVEL': logging.ERROR,
    "FEEDS": {
        path + '/' + filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(QuotesSpider)
process.start()

print("...Run Process")