# use of previous sandbox : https://github.com/g0thier/iTunes-Store-Scrapy/blob/main/Script05.py

from itertools import count
import json
import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

# Intall for delay and rotation proxy
# pip install scrapy-user-agents
# pip install scrapy-rotating-proxies
# pip install rotating-free-proxies

booking_hostels = pd.read_json('src/booking_hostels.json')
booking_hostels = booking_hostels[booking_hostels['url_hostel'] != '']
booking_hostels = booking_hostels['url_hostel'].tolist()

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#  Import Class Function  #
#_________________________#
print("Import Class Function...")

class QuotesSpider(scrapy.Spider):
    counter = 1

    # Name of your spider
    name = "booking"
    
    # Url to start your spider from 
    start_urls = booking_hostels

    # Delay for don't be desallow 
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True, # limite pour ménager les serveur 
        'AUTOTHROTTLE_DEBUG': True, # affiche le debug
        'DOWNLOAD_DELAY': 0.2, # temps entre les requetes 
        'DEPTH_LIMIT': 1, # profondeur de recherche 
    }

    # Rotation de proxy 
    ROTATING_PROXY_LIST_PATH = 'src/proxies.txt' # Path that this library uses to store list of proxies
    NUMBER_OF_PROXIES_TO_FETCH = 5 # Controls how many proxies to use

    # paralelle
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        #'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        #'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        'rotating_free_proxies.middlewares.RotatingProxyMiddleware': 610,
        'rotating_free_proxies.middlewares.BanDetectionMiddleware': 620,
    }

    # Recherche Requête 
    def parse(self, response):

        print('HTTP status normal 200 :')
        print(response.status)

        # Requetes
        booking_page = response.url

        try:
            hotel_name = response.xpath('//*[@id="hp_hotel_name"]/h2/text()').get()
        except:
            hotel_name = ''

        try:
            adress = response.xpath('//*[@id="showMap2"]/span[1]/text()').get()
        except:
            adress = ''

        try:
            note = response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div/div[1]/text()').get()
        except:
            note = ''

        try: 
            describe = response.xpath('//*[@id="property_description_content"]').getall()
            describe = describe[0]
            describe = re.findall('<p>(.*?)</p>', describe)
            describe = ' '.join(describe)
        except:
            describe = ''

        print(f'{self.counter}/{len(booking_hostels)}')
        self.counter += 1

        yield {
                'booking_page' : booking_page, 'hotel_name' : hotel_name, 
                
                'adress': adress, 'note': note, 'describe' : describe
            }



print("...Import Class Function")
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
# Create Folder Directory #
#_________________________#
print("Create Folder Directory...")

try: 
    parent_dir = os.path.abspath(os.path.split(__file__)[0])
    folder_name = "src"
    print(parent_dir)

    path = os.path.join(parent_dir, folder_name)
    os.mkdir(path)
except:
    print("File probably exists")

print("...Create Folder Directory")
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#       Run Process       #
#_________________________#
print("Run Process...")

# Name of the file where the results will be saved
filename = "hostels_list.json"

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


## 'Chrome/97.0'
## 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
## 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
## 


# https://pypi.org/project/rotating-free-proxies/ 

# https://pypi.org/project/scrapy-rotating-proxies/ # <--- detect bannissement 

# https://docs.scrapy.org/en/latest/topics/autothrottle.html#autothrottle-algorithm

# https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings

# https://github.com/scrapy-plugins/scrapy-splash#why-not-use-the-splash-http-api-directly

# https://pypi.org/project/scrapy-rotating-proxies/