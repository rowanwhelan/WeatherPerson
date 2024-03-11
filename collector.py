from data_collection.total_sun_hours import get_sunlight_hours
path = 'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS 546/data'
#Belvedere
latitude = '40.7794'
longitude = '-73.9691'
get_sunlight_hours(latitude, longitude, False, path+'/Belvedere_Sunlight.csv')
#Midway
latitude = '41.7868'
longitude = '87.7522'
get_sunlight_hours(latitude, longitude, False, path+'/Midway_Sunlight.csv')
#Bergstrom
latitude = '30.1953'
longitude = '97.6667'
get_sunlight_hours(latitude, longitude, False, path+'/Bergstrom_Sunlight.csv')
#Miami
latitude = '25.7951'
longitude = '80.2795'
get_sunlight_hours(latitude, longitude, False, path+'/Miami_Sunlight.csv')