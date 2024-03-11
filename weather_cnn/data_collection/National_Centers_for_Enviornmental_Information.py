import requests,sys 
sys.path.append("../")
from weather_cnn.keys.NCEI import key

def collect_NCEI_data(latitude, longitude):
    start_date = '2022-01-01'
    end_date = '2022-01-31'
    location = str(latitude) + ',' + str(longitude)
    data_set = 'global-historical-climatology-network-daily'
    
    api_url = f'https://www.ncei.noaa.gov/access/services/data/v1'
    
    params = {
        'dataset': data_set,
        'startDate': start_date,
        'endDate': end_date,
        'location': location,
        'format': 'csv',
        'api-key': key
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.text
        print(data)
    else:
        print(f'Error: {response.status_code} - {response.text}')

collect_NCEI_data(40.7794,-73.9691)