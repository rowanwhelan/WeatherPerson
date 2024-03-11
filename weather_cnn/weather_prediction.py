from Regression import Regression


reg = Regression(1000000,.0001,1)

belvedere_castle_tempartures = [61,41,47,55,67,58,49,52,54]
midway_international_airport_temperatures = [53,45,46,61,73,72,44,48,49]
bergstrom_temperatures = [70,49,69,82,79,84,90,83,75]
miami_temperatures = [79,81,79,79,82,84,82,80,86]

z = [ [data] for data in range(1,10)]

belv_int, belv_values = reg.fit(z,belvedere_castle_tempartures)
belv_prediction = belv_int + belv_values[0]*6
print("the model predicts:", belv_prediction, "for belvedere")

reg2 = Regression(1000000,0.0001,1)
mid_int, mid_values = reg2.fit(z,midway_international_airport_temperatures)
mid_predicition = mid_int + mid_values[0]*6
print("the model predicts:", mid_predicition, "for midway")

reg3 = Regression(1000000,0.0001,1)
berg_int, berg_values = reg3.fit(z,bergstrom_temperatures)
berg_prediction = berg_int + berg_values[0]*6
print("the model predicts:", berg_prediction, "for bergstrom")

reg4 = Regression(1000000,0.0001,1)
miami_int, miama_values = reg4.fit(z,miami_temperatures)
miami_prediction = miami_int + miama_values[0]*6
print("the model predicts:", miami_prediction, "for miami")