# use of previous sandbox : https://github.com/g0thier/iTunes-Store-Scrapy/blob/main/Script05.py

import json
import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest


booking_index = pd.read_json("src/booking_index.json")

booking_links = pd.DataFrame(columns=['urls'])

# Makes links 
for item in range(len(booking_index)):
    basic_page = booking_index['main_url'][item]
    max_result = booking_index['nb_place'][item]
    max_result = max_result//25 * 25

    # Composition urls
    for item in range(0, max_result, 25):
        new_link = f'{basic_page}&offset={item}'
        new_url = pd.DataFrame(columns= ['urls'], data= [[new_link]])
        booking_links = pd.concat([booking_links, new_url])

booking_links = booking_links['urls'].tolist()


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#   Scraping part.   #
#____________________#

class QuotesSpider(scrapy.Spider):

    # Name of your spider
    name = "booking_index"
    
    # Url to start your spider from 
    start_urls = booking_links


    # Recherche Requête 
    def parse(self, response):

        print('HTTP status normal 200 :')
        print(response.status)

        quotes = response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[7]/div')

        for quote in quotes:

            # Requete 
            main_url = response.url
            
            url_hostel = quote.xpath('div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/@href').getall()
            try:
                url_hostel = url_hostel[0]
            except:
                url_hostel = ''

            yield {
                'main_url' : main_url, 
                'url_hostel': url_hostel
                }

try: 
    parent_dir = os.path.abspath(os.path.split(__file__)[0])
    folder_name = 'src'
    path = os.path.join(parent_dir, folder_name)
    os.mkdir(path)
except:
    # adversiting cells without good formats. 
    pass

# Name of the file where the results will be saved
filename = "booking_hostels.json"

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