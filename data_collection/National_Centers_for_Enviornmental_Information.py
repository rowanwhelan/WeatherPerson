import numpy as np
import requests,sys 
sys.path.append("../")
from CS_546.keys.NCEI import key

def tabulate_response(response,data,value):
    if response.status_code == 200:
            data = response.json()
            for observation in data['results']:
                date = observation['date']    
                value = observation['value']
                
                data[index_of_day(date),] = value
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
            'limit': '365',
            'datatypeid': ['ACMH']
        }
        headers = {'token': key}
        response = requests.get(api_url, params=params, headers=headers)

        params = {
            'datasetid': data_set,
            'startdate': start_date,
            'enddate': end_date,
            'stationid': 'GHCND:USW00014732',
            'format': 'csv',
            'limit': '365',
            'datatypeid': ['ACMH']
        }
        
        response = requests.get(api_url, params=params, headers=headers)
        
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
            
        

collect_NCEI_data()