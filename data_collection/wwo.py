import sys
from wwo_hist import retrieve_hist_data
import csv
sys.path.append("../")
from CS_546.keys.wwokey import key
import os
os.chdir("..\CS_546\data")
import requests

def get_historical_weather(api_key, location, start_date, end_date):
    url = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"
    params = {
        "key": api_key,
        "q": location,
        "format": "json",
        "date": f"{start_date}",
        "enddate": f"{end_date}",
        'frequency': 24
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        daily_avg_humidity = {}
        for entry in data['data']['weather']:
            date = entry['date']
            hourly_humidity = [int(hour['humidity']) for hour in entry['hourly']]
            daily_avg_humidity[date] = sum(hourly_humidity) / len(hourly_humidity)
        return daily_avg_humidity
    else:
        print("Failed to fetch weather data:", response.status_code)
        return None

def write_table(table,location):
    output_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_folder, exist_ok=True)
    csv_file = os.path.join(output_folder, f"{location}_humidity_data.csv")
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Date', 'Humidity'])
        # Write data rows
        for date, humidity in table.items():
            writer.writerow([date, humidity])

def compile_wwo_table(location):
    total_dict = {}
    api_key = key
    for year in range(2009,2024):
        for month in range(1,13):
            start_date = f"{year}-{month}-01"
            if month == 2:
                end_date = f"{year}-{month}-28"
            elif month == 4 or month == 6 or month == 9 or month == 11:
                end_date = f"{year}-{month}-30"
            else:
                end_date = f"{year}-{month}-31"
            weather_data = get_historical_weather(api_key, location, start_date, end_date)
            total_dict.update(weather_data)
    if total_dict:
        write_table(total_dict,location)
    else:
        print("Failed to fetch weather data.")
        
compile_wwo_table("New York City, New York,US")
compile_wwo_table("Chicago, Illinois,US")
compile_wwo_table("Miami, Florida, US")
compile_wwo_table("Austin, Texas, US")