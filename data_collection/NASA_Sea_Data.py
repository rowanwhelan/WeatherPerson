import sys
import requests
sys.path.append("../")
import noaapy as noaa
from CS_546.keys.Nasa import key, passkey

def collect_nasa_data(dataset_id):
    # Construct the request URL with your API key
    url = 'https://cmr.earthdata.nasa.gov/collections.json'
    params = {
        'short_name': dataset_id,
        'bounding_box': '-180,-90,180,90',  # Global coverage
        'temporal': '2023   -01-01T00:00:00Z,2023-12-31T23:59:59Z',  # Temporal range
        'page_size': 10  # Number of results per page
    }

    # Make the request
    response = requests.get(url,params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response data
        try:
            data = response.json()
            granules = data.get('feed', {}).get('entry', [])
            print("Dataset ID:", dataset_id)
            print("Number of granules found:", len(granules))
        except KeyError as e:
                print(f"Error: Unable to extract dataset IDs. KeyError: {e}")
                print("Response Content:")
                print(response.content)
                return []
    else:
        # Handle the error
        print(f'Error: {response.status_code} - {response.text}')
dataset_id = 'C1588876556-EUMETSAT'
collect_nasa_data(dataset_id)