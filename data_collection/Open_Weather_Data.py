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
    retry_count = 5
    retry_delay = 2 # seconds

    for _ in range(retry_count):
        try:
            list_of_historical_values = mgr.air_quality_history_at_coords(latitude, longitude, start=start_date, end=end_date)
            print(list_of_historical_values)
            # Each item in the list_of_historical_values is an Air  Status object 
            for air_status in list_of_historical_values:
                co2_vals = np.append(co2_vals,air_status.co)
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
    start = datetime(2000,1,1)
    end = datetime(2023,12,31)
    complete_co2_table = np.append(complete_co2_table, get_co_in_air(latitude, longitude,start,end_date = end))
    print(len(complete_co2_table))
    #write_data(complete_co2_table, path)
    return

path = 'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data'
latitude = 29.7604
longitude = -95.3698
collect_co2_data(latitude,longitude,path+'/Bergstrom_Air_c02.csv')
