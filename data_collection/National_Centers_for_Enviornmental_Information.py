from datetime import datetime
import math
import numpy as np
import requests,sys 
sys.path.append("../")
from CS_546.keys.NCEI import key

def index_of_day(date_str):
    date_str = date_str[0:10]
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # Get the day of the year
        day_of_year = date_obj.timetuple().tm_yday
        year = int(date_str[0:4])
        day_of_year = day_of_year + ((-1980 + year)*365 + math.floor((-1980 + year) / 4))
        print(day_of_year)
        return day_of_year
    except ValueError:
        # Handle invalid date string
        print("Invalid date format. Please provide date in YYYY-MM-DD format.")

def tabulate_response(response,data,datatype):
    if response.status_code == 200:
        data = response.json()
        for observation in data['results']:
            date = observation['date']    
            value = observation['value']
                
            data[index_of_day(date),datatype] = value
        return data
    else:
        print(f'Error: {response.status_code} - {response.text}')

def collect_NCEI_data():
    data = np.array([[],[],[],[]])
    for i in range(1980, 2023):
        start_date = str(i)+'-01-01'
        end_date = str(i)+'-12-31'
        data_set = 'GHCND'

        api_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
        params = {
            'datasetid': data_set,
            'startdate': start_date,
            'enddate': end_date,
            'stationid': 'GHCND:USW00014732',
            'format': 'csv',
            'limit': '366',
            'datatypeid': ['ACMH']
        }
        headers = {'token': key}
        response = requests.get(api_url, params=params, headers=headers)
        data.append = tabulate_response(response, data, 1)
        params = {
            'datasetid': data_set,
            'startdate': start_date,
            'enddate': end_date,
            'stationid': 'GHCND:USW00014732',
            'format': 'csv',
            'limit': '366',
            'datatypeid': ['ACMH']
        }
        response = requests.get(api_url, params=params, headers=headers)
        tabulate_response(response, data, 2)
        params = {
            'datasetid': data_set,
            'startdate': start_date,
            'enddate': end_date,
            'stationid': 'GHCND:USW00014732',
            'format': 'csv',
            'limit': '366',
            'datatypeid': ['TMAX']
        }
        response = requests.get(api_url, params=params, headers=headers)
        tabulate_response(response, data, 2)
index_of_day('1986-12-04')
index_of_day('1980-01-04')