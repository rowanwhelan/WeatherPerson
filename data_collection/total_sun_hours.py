import math
from matplotlib import pyplot as plt
import numpy as np, datetime, ephem

#function to convert from year day to the ephem internal values
def date_to_ephem_date(year,day):
    return ephem.Date(36525.0 + ((-2000 + year) *365) + day + math.floor((-2000 + year) / 4) -0.5)

def collect_sunlight_hours(latitude, longitude, print_val, path):
    observer = ephem.Observer()
    observer.lat, observer.lon = latitude, longitude
    all_dates = np.array([])
    all_daylight_hours = np.array([])
    all_dates, all_daylight_hours = create_sunlight_table(observer, all_dates, all_daylight_hours)
    if print_val:
        plot_sunlight_table(all_dates, all_daylight_hours)
    zipped_array = np.vstack((all_dates, all_daylight_hours)).ravel(order='F')
    np.savetxt(path, zipped_array, delimiter=',')
    print('array successfully saved')

def create_sunlight_table(observer, all_dates, all_daylight_hours):
    for year in range(2000,2023):
        dates = np.array([])
        daylight_hours = np.array([])
        days = 366
        if(year%4 == 0):
            days = days+1
        for day in range(1,days):
            date = f'{year}-{day:03d}'
            observer.date = datetime.datetime.strptime(date, '%Y-%j')
            sunrise = observer.next_rising(ephem.Sun())
            sunset = observer.next_setting(ephem.Sun())
            #The sunset on the day happens in the morning before the sunrise, so we must update the day to compensate for this
            if sunset - sunrise < 0:
                #There is a fringe case where if the sunset happens very close to the changing of days, so this if statement catches that case and handles it by removing 24 hours from that calculation
                if sunset - date_to_ephem_date(year, day) < 0.007:
                    sunset = sunset + 1
                #Otherwise the algorithm continues as normal finding the next sunset
                else:
                    date = f'{year}-{day+1:03d}'
                    if day == days-1:
                        date = f'{year+1}-{1:03d}'
                    observer.date = datetime.datetime.strptime(date, '%Y-%j')
                    sunset = observer.next_setting(ephem.Sun())
            #Now that edge cases have been accounted for the algorithm computes the amount of sunlight and appends it to the return array   
            daylight_duration = sunset - sunrise
            daylight_hours = np.append(daylight_hours, daylight_duration * 24)
            dates = np.append(dates,int(date_to_ephem_date(year,day)))  
        all_dates = np.append(all_dates,dates)
        all_daylight_hours = np.append(all_daylight_hours,daylight_hours)
    return all_dates, all_daylight_hours

def plot_sunlight_table(all_dates, all_daylight_hours):
    plt.figure(figsize=(15, 8))
    plt.plot(all_dates, all_daylight_hours, label='Daylight')
    plt.title('Daylight Hours')
    plt.xlabel('Date')
    plt.ylabel('Daylight Hours')
    plt.show()
    
