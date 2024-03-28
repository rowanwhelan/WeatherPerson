import csv
from datetime import datetime, timedelta
import numpy as np
import requests
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from keras.models import model_from_json
from meteostat import Point, Daily
from keys.OpenWeather import key
import pandas as pd
import sys
sys.path.append("../")
from CS_546.data_collection.Open_Weather_Data import get_co_in_air

def datetime_to_hours_float(dt):
    if isinstance(dt, timedelta):
        hours = dt.total_seconds() / 3600  # Convert timedelta to hours
    else:
        midnight = datetime(dt.year, dt.month, dt.day)
        delta = dt - midnight
        hours = delta.total_seconds() / 3600  # 3600 seconds in an hour
    return hours

def get_forecast(latitude, longitude, name):
    today = datetime.now()
    # Create a Point object with the coordinates
    location = Point(latitude, longitude)

    # Fetch forecast data from OpenWeatherMap API
    api_key = key
    if name == 'Belvedere':
        response = requests.get(f'http://pro.openweathermap.org/data/2.5/weather?q=New York City, New York&APPID={key}')
    elif name == 'Midway':
        response = requests.get(f'http://pro.openweathermap.org/data/2.5/weather?q=Chicago, Illinois&APPID={key}')
    elif name == 'Bergstrom':
        response = requests.get(f'http://pro.openweathermap.org/data/2.5/weather?q=Austin, Texas&APPID={key}')
    else:
        response = requests.get(f'http://pro.openweathermap.org/data/2.5/weather?q=Miami, FLorida&APPID={key}')
    openweather_data = response.json()
    
    meteo_data = Daily(location, today)
    meteo_data = meteo_data.normalize()
    meteo_data = meteo_data.fetch()
    
    #Temperature array
    today = pd.Timestamp.now().normalize()
    yesterday = today - pd.Timedelta(days=1)
    max_temp_yesterday = Daily(location, yesterday).normalize().fetch()[meteo_data.index == yesterday.strftime('%Y-%m-%d')]['tmax'].values[0]
    day_before_yesterday = yesterday - pd.Timedelta(days=1)
    max_temp_day_before = Daily(location, day_before_yesterday).normalize().fetch()[meteo_data.index == day_before_yesterday.strftime('%Y-%m-%d')]['tmax'].values[0]
    day_before_day_before_yesterday = day_before_yesterday - pd.Timedelta(days=1)
    max_temp_day_before_day_before = Daily(location, day_before_day_before_yesterday).normalize().fetch()[meteo_data.index == day_before_day_before_yesterday.strftime('%Y-%m-%d')]['tmax'].values[0]
    
    prev_temp = [max_temp_yesterday, max_temp_day_before, max_temp_day_before_day_before]
        
    #PRCP
    precipitation_rain = meteo_data[meteo_data.index == today.strftime('%Y-%m-%d')]['prcp'].fillna(0).values[0]
    precipitation_snow = meteo_data[meteo_data.index == today.strftime('%Y-%m-%d')]['snow'].fillna(0).values[0]
    precipitation = precipitation_snow + precipitation_rain
    
    #Humidity
    humidity = openweather_data['main']['humidity']
    
    #sunlight
    sunrise_timestamp = openweather_data['sys']['sunrise']
    sunrise_datetime = datetime.fromtimestamp(sunrise_timestamp)
    sunset_timestamp = openweather_data['sys']['sunset']
    sunset_datetime = datetime.fromtimestamp(sunset_timestamp)
    sunlight_duration_hours = datetime_to_hours_float(sunset_datetime - sunrise_datetime)
    
    #Wdir
    wind_direction_degrees = meteo_data[meteo_data.index == today.strftime('%Y-%m-%d')]['wdir'].fillna(0).values[0]
    
    #WPGT
    wind_speed = meteo_data[meteo_data.index == today.strftime('%Y-%m-%d')]['wspd'].fillna(0).values[0]
    
    #Pres
    pressure = meteo_data[meteo_data.index == today.strftime('%Y-%m-%d')]['pres'].fillna(0).values[0]
    
    #co2 in air 
    # the datetime objects here are midnight yesterday and midnight today
    co2_average = None
    co2_change = None
    if name != 'Bergstrom':
        air_quality_history = get_co_in_air(latitude, longitude, datetime.combine(yesterday, datetime.min.time()), datetime.combine(today, datetime.min.time()))
        co2_levels = [entry for entry in air_quality_history]
        co2_values = [co2_levels[0], co2_levels[8], co2_levels[16]]
        co2_average = sum(co2_values)/3
        co2_change = co2_values[2] - co2_values[0]
    
    # Print forecast data
    print("Forecast for today:")
    print(f"Previous Temperatures: {prev_temp}")
    print(f"Precipitation: {precipitation} mm")
    print(f"Wind Direction: {wind_direction_degrees}")
    print(f"Wind Peak Gust: {wind_speed} m/s")
    print(f"Pressure: {pressure}")
    print(f"Humidity: {humidity}")
    print(f"Sunlight Duration: {sunlight_duration_hours} hours")
    print(f"Average CO2: {co2_average} ppm")
    print(f"Change in CO2: {co2_change}")
    #Previous Temps, prcp, wdir, wpgt, pres, prcp, sunlight, humidity, co2 average, co2 slope
    # check        , check, check, check, check, check, check, check, 
    if name != 'Bergstrom':
        return np.array([prev_temp[0], prev_temp[1], prev_temp[2], precipitation, wind_direction_degrees, wind_speed, precipitation,co2_average, co2_change ])
    else:
        return np.array([prev_temp[0], prev_temp[1], prev_temp[2], precipitation, wind_direction_degrees, wind_speed, precipitation])

def generate_prediction( latitude, longitude, name, model):
    forecast = get_forecast(latitude, longitude)
    return model.predict(forecast)

def daily_protocol():
    #Belvedere
    latitude = 40.7794
    longitude = -73.9691
    forecast = get_forecast(latitude,longitude, 'Belvedere')

    #Midway
    latitude = 41.7868
    longitude = -87.7522
    forecast = get_forecast(latitude,longitude, 'Midway')

    #Bergstrom
    latitude = 30.1953
    longitude = -97.6667
    forecast = get_forecast(latitude,longitude, 'Bergstrom')

    #Miami
    latitude = 25.7951
    longitude = -80.2795
    forecast = get_forecast(latitude,longitude, 'Miami')


    
def main():
    daily_protocol()
main()