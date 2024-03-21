from data_collection.total_sun_hours import collect_sunlight_hours
from data_collection.pressure import collect_air_stats
from data_collection.Open_Weather_Data import collect_co2_data
from data_collection.National_Centers_for_Enviornmental_Information import collect_NCEI_data
path = 'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data'
#Belvedere
latitude = 40.7794
longitude = -73.9691
#collect_sunlight_hours(str(latitude), str(longitude), False, path+'/Belvedere_Sunlight.csv')
#collect_air_stats(latitude, longitude, path+'/Belvedere_Air_pressure.csv')
#collect_co2_data(latitude,longitude,path+'/Belvedere_Air_c02.csv')
#collect_NCEI_data('GHCND:USW00014732', 'GHCND', path+'/Belvedere_NCEI.csv')
#Midway
latitude = 41.7868
longitude = 87.7522
#collect_sunlight_hours(latitude, longitude, False, path+'/Midway_Sunlight.csv')
#collect_air_stats(latitude, longitude, path+'/Midway_Air_pressure.csv')
#collect_co2_data(latitude,longitude,path+'/Midway_Air_c02.csv')
#Bergstrom
latitude = 30.1953
longitude = 97.6667
#collect_sunlight_hours(latitude, longitude, False, path+'/Bergstrom_Sunlight.csv')
#collect_air_stats(latitude, longitude, path+'/Bergstrom_Air_pressure.csv')
#collect_co2_data(latitude,longitude,path+'/Bergstrom_Air_c02.csv')
#Miami
latitude = 25.7951
longitude = 80.2795
#collect_sunlight_hours(latitude, longitude, False, path+'/Miami_Sunlight.csv')
#collect_air_stats(latitude, longitude,  path+'/Miami_Air_pressure.csv')
#collect_co2_data(latitude,longitude,path+'/Miami_Air_c02.csv')