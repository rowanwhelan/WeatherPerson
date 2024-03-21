import sys
import requests
sys.path.append("../")
from CS_546.keys.Nasa import key

# Define NASA Earthdata credentials
username = 'rwhelan340'
password = key

# Define search parameters
keyword = 'sea surface temperature'
bounding_box = '-80,0,0,80'  # Atlantic Ocean
start_date = '2000-01-01'
end_date = '2000-01-31'

# Construct search URL
url = f'https://cmr.earthdata.nasa.gov/search/granules.json?short_name=SST&version=1&temporal[]={start_date},{end_date}&bounding_box={bounding_box}&keyword={keyword}'

# Perform authenticated request to NASA Earthdata
response = requests.get(url, auth=(username, password))

# Check if request was successful
if response.status_code == 200:
    # Extract URLs of data granules
    granules = response.json()['feed']['entry']
    for granule in granules:
        granule_url = granule['links'][0]['href']
        print(f"Downloading: {granule_url}")
        
        # Download data
        data_response = requests.get(granule_url, auth=(username, password))
        
        # Save data to file
        with open(granule_url.split('/')[-1], 'wb') as f:
            f.write(data_response.content)
else:
    print("Error:", response.status_code)
