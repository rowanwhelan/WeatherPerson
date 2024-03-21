from datetime import datetime
import math
import time
import numpy as np
import requests,sys 
sys.path.append("../")
from CS_546.keys.NCEI import key

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

def index_of_day(date_str):
    date_str = date_str[0:10]
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # Get the day of the year
        day_of_year = date_obj.timetuple().tm_yday
        year = int(date_str[0:4])
        day_of_year = day_of_year + ((-1980 + year)*365 + math.floor((-1980 + year) / 4))
        return day_of_year
    except ValueError:
        # Handle invalid date string
        print("Invalid date format. Please provide date in YYYY-MM-DD format.")

def tabulate_response(response,table):
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data == {}:
            return table
        for observation in data['results']:
            date = observation['date']    
            value = observation['value']
            table[index_of_day(date)-1][1] = value
    else:
        print(f'Error: {response.status_code} - {response.text}')
    return table

def collect_NCEI_data(station,data_set,path):
    retry_delay = 1
    table = np.array([[1,0]])
    for num in range (1,16070):
        table = np.vstack((table,[[num+1,0]]))
    for i in range(2000, 2023):
        time.sleep(retry_delay)
        start_date = str(i)+'-01-01'
        end_date = str(i)+'-12-31'
        api_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
        params = {
            'datasetid': data_set,
            'startdate': start_date,
            'enddate': end_date,
            'stationid': station,
            'format': 'json',
            'limit': '1000',
            'datatypeid': ['PRCP']
        }
        headers = {'token': key}
        response = requests.get(api_url, params=params, headers=headers)
        table = tabulate_response(response, table)
    write_data(table,path)
    return table

path = 'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data'
#collect_NCEI_data('USW00014732', 'GHCND', path+'/Belvedere_NCEI.csv')
#collect_NCEI_data('US1ILCK0012', 'GHCND', path+'/Midway_NCEI.csv')
collect_NCEI_data('USW00093987', 'GHCND', path+'/Bergstrom_NCEI.csv')
#collect_NCEI_data('GHCND:USW00092811', 'GHCND', path+'/Miami_NCEI.csv')
