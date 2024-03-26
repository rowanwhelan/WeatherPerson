import csv
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from keras.models import model_from_json

class ClimateNN(nn.Module):
        def __init__(self):
            super(ClimateNN, self).__init__()
            self.fc1 = nn.Linear(12, 128)  # Input layer
            self.fc2 = nn.Linear(128,64)
            self.fc3 = nn.Linear(64, 32)   # Hidden layer
            self.fc4 = nn.Linear(32, 1)    # Output layer

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            x = torch.relu(self.fc3(x))
            x = self.fc4(x)
            return x

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
        
# CO2 data was taken every 8 hours, so I decided to have the algorithm learn based on the slope of the day and the average co2        
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

# returns tables in the format Tmax, prcp, wdir, wpgt, pres, prcp, sunlight, humidity, co2 average, co2 slope
def compile_tables(name,prev_temp):
    filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_Air_Pressure.csv'
    meteo_array = read_data(filename)
    filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_NCEI.csv'
    ncei_array = read_data(filename)
    filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_Sunlight.csv'
    sun_array = read_data(filename)
    # sun array data is taken farther back, but I have decided to only use the last 23 years of data to match the other sources
    sun_array = sun_array[-8765:]
    filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_humidity.csv'
    #humidity data only goes back to 2009 so you need to add 
    humid_array = read_data(filename)
    humid_array = humid_array[:,1]
    padded_humid_array = np.pad(humid_array, ((3290), (0)), mode='constant', constant_values=0)
    
    temps = meteo_array[:,0]
    hist_temp = create_previous_temparatures(temps, prev_temp)

    
    if name != 'Bergstrom':
        filename = f'C:/Users/rwhel/OneDrive/Desktop/Notes/College/CS_546/data/{name}_Air_c02.csv'
        co2_table = read_data(filename)
        co2_table = co2_table[-26295:]
        co2_table = co2_reshape(co2_table)
        combined_array = np.column_stack((meteo_array[:, 1], hist_temp[:,0], hist_temp[:,1], hist_temp[:,2], meteo_array[:, 1], meteo_array[:, 2], meteo_array[:, 3], meteo_array[:, 4], ncei_array[:, 1], sun_array[:, 0], padded_humid_array, co2_table[:, 0], co2_table[:, 1]))
        return combined_array
    else:
        combined_array = np.column_stack((meteo_array[:, 1], hist_temp[:,0], hist_temp[:,1], hist_temp[:,2], meteo_array[:, 1], meteo_array[:, 2], meteo_array[:, 3], meteo_array[:, 4], ncei_array[:, 1], sun_array[:, 0], padded_humid_array))
        return combined_array

# pass in a n x 1 np array and three manually inputted temperatures get back a n x 3 np array
def create_previous_temparatures(data, temps):
    second = np.array([temps[1], temps[2], data[0]])
    third = np.array([temps[2], data[0],data[1]])
    final = np.row_stack([temps,second,third])
    for i in range(3,len(data)):
        slice = np.array([data[i-3], data[i-2], data[i-1]])
        final = np.row_stack([final, slice])
    return final
# Assuming you have your dataset in X (input features) and y (target labels)
# X should be a numpy array of shape (8765, 10)

def NN(data,labels):
    # Convert numpy arrays to PyTorch tensors
    X = torch.tensor(data, dtype=torch.float32)
    y = torch.tensor(labels, dtype=torch.float32)


    # Initialize the model, loss function, and optimizer
    model = ClimateNN()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0005)

    # Training the model
    epochs = 500
    batch_size = 32
    for epoch in range(epochs):
        for i in range(0, len(X), batch_size):
            inputs = X[i:i+batch_size]
            batch_labels = y[i:i+batch_size].view(-1,1)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, batch_labels)
            loss.backward()
            optimizer.step()

        if epoch % 100 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
    print('Finished Training')
    return model
    
def test_model(model, test_data, test_labels, threshold=0.4):
    # Convert test data to PyTorch tensor
    X_test = torch.tensor(test_data, dtype=torch.float32)
    y_test = torch.tensor(test_labels, dtype=torch.float32).view(-1,1)

    # Set the model to evaluation mode
    model.eval()

    # Pass test data through the model
    with torch.no_grad():
        outputs = model(X_test)

    # Calculate loss (optional, depending on your requirements)
    criterion = nn.MSELoss()
    test_loss = criterion(outputs, y_test).item()
    print(f'Test Loss: {test_loss:.4f}')

    # Evaluate performance
    num_correct = 0
    for pred, true_label in zip(outputs, y_test):
        if torch.abs(pred - true_label) <= threshold:
            num_correct += 1

    accuracy = num_correct / len(test_labels) * 100
    print(f'Percentage of Correctly Labeled Test Data: {accuracy:.2f}%')

    return accuracy

def format_data(data):
    labels = (data[:,0].astype(float) * 1.8) + 32
    testing_labels = labels[-100:]
    labels = labels[0:len(labels)-100]
    data = data[:,1::]
    testing_data = data[-100:]
    data = data[0:len(data)-100]
    return testing_labels, testing_data, labels, data

def complete_NN(name, prev):
    print(f'Training a model for {name}')
    data = compile_tables(name, prev)
    testing_labels, testing_data, data_labels, data = format_data(data)
    accuracy = 0
    while accuracy < 80:
        model = NN(data.astype(float), data_labels.astype(float))
        accuracy = test_model(model,testing_data.astype(float),testing_labels.astype(float))
    return model
            
def save_model(model,name):
    torch.save(model.state_dict(), f'models/{name}_model')
    
def load_model(model,name):
    model = ClimateNN()
    model.load_state_dict(torch.load(f'models/{name}_model'))

def model_instantiation():
    #Belvedere
    prev_temp = [36,50,43]
    name = 'Belvedere'
    #bel_model = complete_NN(name, prev_temp)
    #save_model(bel_model,name)  
    #Miami
    prev_temp = [71,75,79]
    name = 'Miami'
    #mia_model = complete_NN(name,prev_temp)
    #save_model(mia_model,name)
    #Midway
    prev_temp = [48,41,41]
    name = 'Midway'
    mid_model = complete_NN(name,prev_temp)
    save_model(mid_model,name)
    #Bergstrom
    prev_temp = (79,81,72)
    name = 'Bergstrom'
    #ber_model = complete_NN(name,prev_temp)
    #save_model(ber_model,name)

def main():
    model_instantiation()
    
main()