# Usuals imports
import datetime
import numpy as np
import pandas as pd 
import re
import requests
import urllib.parse

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#  Constantes  #
#______________#

cities_weather_infos = pd.read_csv('src/cities_weather_infos.csv')

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

# Creating urls params
checkin = today.strftime("%Y-%m-%d")
checkout = tomorrow.strftime("%Y-%m-%d")
ac_langcode = 'fr'
dest_type = 'city'


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#   booking first link city page    #
#___________________________________#

booking_mains_cities = pd.DataFrame(columns= ['city', 'main_url'])

for item in range(len(cities_weather_infos)):

    city = cities_weather_infos['city'][item]

    # Composition urls
    url = 'https://www.booking.com/searchresults.fr.html?'
    params = {'ss': city, 
              'ac_langcode': ac_langcode,
              'dest_type': dest_type,
              'checkin': checkin,
              'checkout': checkout
              }

    main_url = url + urllib.parse.urlencode(params)

    new_url = pd.DataFrame(columns= ['city', 'main_url'], 
                              data= [[ city, main_url]])

    booking_mains_cities = pd.concat([booking_mains_cities, new_url])

# reset index due to concat
booking_mains_cities.reset_index(inplace= True)
booking_mains_cities.drop(columns=['index'], inplace= True)


#¨¨¨¨¨¨¨¨¨¨¨¨¨#
#   Export    #
#_____________#

booking_mains_cities.to_csv(r'src/booking_mains_cities.csv', index=False)