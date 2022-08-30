# use of previous sandbox : https://github.com/g0thier/iTunes-Store-Scrapy/blob/main/Script05.py

import json
import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

booking_mains_cities = pd.read_csv('src/booking_mains_cities.csv')

class QuotesSpider(scrapy.Spider):

    # Name of your spider
    name = "booking_index"
    
    # Url to start your spider from 
    start_urls = booking_mains_cities['main_url'].to_list()


    # Recherche Requête 
    def parse(self, response):

        print('HTTP status normal 200 :')
        print(response.status)

        quotes = response.xpath('//*[@id="right"]/div[1]/div/div/div')

        for quote in quotes:

            # Requete 
            main_url = response.url
            
            nb_place = quote.xpath('h1/text()').get()

            # fix str issue
            nb_place = re.search(r': (.*?) établissements', nb_place).group(1)
            nb_place = nb_place.replace(r'\D+', '')
            nb_place = nb_place.replace(' ', '')
            nb_place = int(nb_place)

            yield {
                'main_url' : main_url, 
                'nb_place': nb_place
                }

try: 
    parent_dir = os.path.abspath(os.path.split(__file__)[0])
    folder_name = 'src'
    path = os.path.join(parent_dir, folder_name)
    os.mkdir(path)
except:
    pass

# Name of the file where the results will be saved
filename = "booking_index.json"

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