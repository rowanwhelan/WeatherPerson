import requests,sys 
sys.path.append("../")

def collect_NWS_data():
    #Belvedere
    stationid = 'KW035'
    start = '1980-01-01T00:00:00+19:00'
    end = '2023-12-21T24:00:00+19:00'
    api_url = f'https://api.weather.gov/stations/{start, end, stationid}/observations'
    response = requests.get(api_url, headers= {'User-Agent': 'WeatherPredictorApp/1.0 contact rwhelan340@gmail.com', 'Accept': 'application/json'})

    
    # Check if request was successful
    if response.status_code == 200:
    # Parse the JSON response
        data = response.json()
    # Print the entire response for inspection
        print(data)
    else:
        print('Error:', response.status_code)
        print('Response Content:', response.text)  # Print response content for inspection

collect_NWS_data()