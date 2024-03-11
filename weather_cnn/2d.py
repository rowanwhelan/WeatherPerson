
# TESTER CODE TO GRAPH THE PLANE
from random import random
from matplotlib import pyplot as plt
import numpy as np
from Regression import Regression


reg = Regression(50000,0.01,2)
xy_points =  [ [random.random()*5, random.random()*5] for i in range(10) ]
z_points =  [ random.random()*5 for i in range(10) ]
intercept, weight_vector = reg.fit(xy_points, z_points)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = np.array( x * weight_vector[0] + y * weight_vector[1] + intercept)

surf = ax.plot_surface(x, y, z, cmap='viridis')
x_points = [xy_points[i][0] for i in range(len(xy_points))]
y_points = [xy_points[i][1] for i in range(len(xy_points))]

ax.scatter(x_points, y_points, z_points, color='red', s=50 , label='Specific Points')
# Add labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('3D Plot')

# Add a color bar
fig.colorbar(surf)

# Show the plot
plt.show()

