import csv
import numpy as np

def read_data(file_name):
    try:
        with open(file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
            
        if not data:
            raise ValueError("CSV file is empty")
        
         # Check if date in file
        if 'humidity' in file_name.lower():
            dates = [row[0] for row in data]
            humidity_values = [float(row[1]) for row in data]
            return np.hstack((   np.array(dates).reshape(-1,1), np.array(humidity_values).reshape(-1, 1) ))
        
        data = [[float(cell) for cell in row] for row in data]
        return np.array(data)
    
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An error occurred: {e}")
        
#CO2 data was taken every 8 hours, so I decided to have the algorithm learn based on the slope of the day and the average co2        
def co2_reshape(table):
    # Reshape the original table to have three columns
    reshaped_table = table.reshape(-1, 3)

    # Calculate the average of every three points
    averages = np.mean(reshaped_table, axis=1)

    # Calculate the slope between each pair of consecutive points
    slopes = np.diff(reshaped_table, axis=1)[:, 1] / 2  # Calculate the average of the differences as the slope

    # Stack the averages and slopes to create the final 8765 x 2 table
    final_table = np.column_stack((averages, slopes))
    return final_table
    print("Dimensions of the final table:", final_table.shape)

def compile_tables(name):
    filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_Air_Pressure.csv'
    meteo_array = read_data(filename)
    print(meteo_array.shape)
    filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_NCEI.csv'
    ncei_array = read_data(filename)
    print(ncei_array.shape)
    filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_Sunlight.csv'
    sun_array = read_data(filename)
    # sun array data is taken farther back, but I have decided to only use the last 23 years of data to match the other sources
    sun_array = sun_array[-8765:]
    print(sun_array.shape)
    filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_humidity.csv'
    #humidity data only goes back to 2009 so you need to add 
    humid_array = read_data(filename)
    padded_humid_array = np.pad(humid_array, ((3290, 0), (0, 0)), mode='constant', constant_values=0)
    print(padded_humid_array.shape)
    if name != 'Bergstrom':
        filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_Air_c02.csv'
        co2_table = read_data(filename)
        co2_table = co2_table[-26295:]
        co2_table = co2_reshape(co2_table)
        combined_array = np.hstack((padded_humid_array[:, 0], meteo_array[:, 0], meteo_array[:, 1], meteo_array[:, 2], meteo_array[:, 3], meteo_array[:, 4], ncei_array[:, 0], ncei_array[:, 1], sun_array[:, 0], padded_humid_array[:, 1], co2_table[:, 0], co2_table[:, 1]))
        combined_array = combined_array.reshape(8765, -1)

        return combined_array
    else:
        combined_array = np.hstack((padded_humid_array[:, 0], meteo_array[:, 0], meteo_array[:, 1], meteo_array[:, 2], meteo_array[:, 3], meteo_array[:, 4], ncei_array[:, 0], ncei_array[:, 1], sun_array[:, 0], padded_humid_array[:, 1]))
        combined_array = combined_array.reshape(8765, -1)

        return combined_array
        
        
def main():
    print(compile_tables('Belvedere'))
main()
    