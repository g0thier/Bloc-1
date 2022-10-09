# Bloc n°1 : Construction et alimentation d'une infrastructure de gestion de données. 
## Contact 

[voguant-cal0n@icloud.com](mailto:voguant-cal0n@icloud.com)

## Video explain

[Bloc n°1 : Construction et alimentation d'une infrastructure de gestion de données.](https://youtu.be/3zXOKyZjQvw "Bloc n°1")

## Goals

As the project has just started, your team doesn't have any data that can be used to create this application. Therefore, your job will be to: 

* Scrape data from destinations 
* Get weather data from each destination 
* Get hotels' info about each destination
* Store all the information above in a data lake
* Extract, transform and load cleaned data from your datalake to a data warehouse


## Informations about files:

1. cities_weather_info.ipynb create from a list of cities a dataframe with weather of this cities.
2. weather_code.py return a dataframe who associate code with a definition of this code.
3. booking_infos.ipynb return the first page of city result for current date.
4. booking_infos_pages.py return the numbers of results availables on firsts pages.
5. booking_hostels.py make a list of all hostels availables for previous list of firts pages.
6. hostels_list.py make a list of all hostels forms from hotels cities list.
7. hostels_list_located.ipynb add locations to this last dataset.

8. make_s3_dataset.ipynb reunion of all datas in s3_booking_weather_dataset.csv.
9. push_s3.ipynb send the dataframe on s3 bucket. 
10. pull_s3.ipynb import the dataframe drom the s3 bucket and show 20 best hostels in 5 best cities.