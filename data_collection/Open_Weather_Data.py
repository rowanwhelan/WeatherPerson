from datetime import datetime
import sys
import time
import pyowm
from pyowm.utils.config import get_config_from
sys.path.append("../")
from CS_546.keys.OpenWeather import key

config_dict = get_config_from("keys\OWconfigs.json")
owm = pyowm.OWM(key)
mgr = owm.airpollution_manager()

def get_co_in_air(location, start_date, end_date):
    location = "New York mgr = owm.airpollution_manager()City, New York"

    retry_count = 3
    retry_delay = 5  # seconds

    for _ in range(retry_count):
        try:
            start = 1606223802  # November 24, 2020
            list_of_historical_values = mgr.air_quality_history_at_coords(51.507351, -0.127758, start)  # London, GB

            # ...or fetch history on a closed timeframe in the past
            end = 1613864065  # February 20, 2021
            list_of_historical_values = mgr.air_quality_history_at_coords(51.507351, -0.127758, start, end=end)  # London, GB

            # Each item in the list_of_historical_values is an AirStatus object 
            for air_status in list_of_historical_values:
                print(air_status.co)  # air quality index
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