from datetime import datetime
import math
import sys
import time
import numpy as np
import pyowm
from pyowm.utils.config import get_config_from
sys.path.append("../")
from CS_546.keys.OpenWeather import key

def get_co_in_air(latitude, longitude, start_date, end_date):
    config_dict = pyowm.utils.config.get_default_config()
    owm = pyowm.OWM(key,config_dict)
    mgr = owm.airpollution_manager()
    co2_vals = np.array([])
    retry_count = 3
    retry_delay = 12 # seconds

    for _ in range(retry_count):
        try:
            list_of_historical_values = mgr.air_quality_history_at_coords(latitude, longitude, start=start_date, end=end_date)
            print(f"list is '{list_of_historical_values}'")
            # Each item in the list_of_historical_values is an Air  Status object 
            for air_status in list_of_historical_values:
                co2_vals = np.append(co2_vals,air_status.co)
                print("the air value is", air_status.co)
            break

        except pyowm.commons.exceptions.NotFoundError:
            print("Historical weather data not found for the specified location and date.")
            break
        except Exception as e:
            print("An error occurred:", e)
            print("Retrying...")
            time.sleep(retry_delay)
    else:
        print("Failed to retrieve historical weather data after multiple retries.")
    
    return co2_vals

def write_data(data, path):
    if len(data) == 0:
        print("Error")
        return
    try:
        # Save the data to the CSV file
        np.savetxt(path, data, delimiter=",")
        print(f"Data has been successfully written to '{path}'.")
    except Exception as e:
        print("An error occurred while writing to the CSV file:", e)
        
def collect_co2_data(latitude, longitude, path):
    complete_co2_table = np.array([])
    start = 1606223802-2087
    for i in range(0,365):
        leap_year =0
        if i%4 == 0: 
            leap_year = 1
        start_date = start + i*352 + math.floor(i / 4)
        # get the co2_table for the year and append it to the total table
        print(f"the year is '{i + 2015}'")
        complete_co2_table = np.append(complete_co2_table, get_co_in_air(latitude, longitude,start_date,end_date = start_date + 352 + leap_year))
    print(complete_co2_table)
    write_data(complete_co2_table, path)
    return
path = 'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data'
latitude = 40.7794
longitude = -73.9691
#collect_co2_data(latitude,longitude,path+'/Belvedere_Air_c02.csv')

def main():
    retry_count = 3
    retry_delay = 12 # seconds
    for _ in range(retry_count):
        try:
            start = datetime(2000,1,1)
            end = datetime(2023,12,31)
            sys.path.append("../")
            config_dict = pyowm.utils.config.get_default_config()
            owm = pyowm.OWM(key,config_dict) 
            mgr = owm.airpollution_manager()
            list_of_forecasts = mgr.air_quality_history_at_coords(40.7794, -73.9691, int(start.timestamp()), int(end.timestamp()))
            for air_status in list_of_forecasts:
                print(air_status.co)
            print(len(list_of_forecasts))
            break
        except pyowm.commons.exceptions.NotFoundError:
            print("Historical weather data not found for the specified location and date.")
            break
        except Exception as e:
            print("An error occurred:", e)
            print("Retrying...")
            time.sleep(retry_delay)
