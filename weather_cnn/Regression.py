
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

#/
def gradientDescent(Theta0, learnrate, function, partial, epsilon):
    theta = Theta0
    t = 0 
    while True:
        t = t + 1
        thetaTemp = theta
        theta = theta - learnrate(partial(theta))
        if math.abs(function(theta) - function(thetaTemp)) < epsilon:
            break
    return theta
#/

class Regression:
    def __init__(self, iterations: int = 100, learning_rate: float = 1, dimension: int = 1):
        self.iterations = iterations
        self.alpha = learning_rate

        self.intercept = 0
        self.weight_vector = [0] * dimension

    def fit(self, x, y):    
        #initialize parameters 
        intercept = 0
        weight_vector = [ random.random() for col in range(len(x[0])) ]


        #begin fitting data
        iteration_number = 0 
        while iteration_number < self.iterations:
            iteration_number += 1
            intercept_gradient, weight_vector_gradient = self.compute_gradient(x, y, intercept, weight_vector)
            intercept, weight_vector = self.update(intercept, intercept_gradient, weight_vector, weight_vector_gradient)
        return intercept, weight_vector
        

    def compute_gradient(self, x,y,intercept, weight_vector):
        intercept_gradient, weight_vector_gradient = 0, [0] * len(x[0])
        for i in range(len(x)):
            #predict with your model then see how accurate your prediction is
            y_i_hat = intercept + sum((x[i][j] * weight_vector[j]) for j in range(len(x[0])))
            partial_error = 2 * (y[i] - y_i_hat)

            for j in range(len(x[0])):
                #update your values based on your predictions 
                weight_vector_gradient[j] += partial_error * (x[i][j]) / len(x)
                intercept_gradient += partial_error/ len(x)
        return intercept_gradient, weight_vector_gradient
    
    def update(self, intercept, intercept_gradient, weight_vector, weight_vector_gradient):
        intercept += intercept_gradient * self.alpha
        for j in range(len(weight_vector)):
            weight_vector[j] += weight_vector_gradient[j] * self.alpha
        return intercept, weight_vector

