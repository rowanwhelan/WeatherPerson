from datetime import datetime
from meteostat import Point, Daily
import numpy as np

def collect_air_stats(latitude, longitude, path):
    location = Point(latitude,longitude)
    data = Daily(location, start = datetime(2000,1,1,0,0), end= datetime(2023,12,31,0,0))
    data = data.fetch()
    data = data[['tmax', 'prcp', 'wdir', 'wpgt', 'pres']]
    data = data.fillna(-1)
            
    np.savetxt(path, data, delimiter=',')
    print('array successfully saved')
    
