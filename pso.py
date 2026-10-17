# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import seaborn
import sympy
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.pyplot as plt
import random
from sympy import symbols, Eq, solve


'''
X=np.linspace(-5.12, 5.12, 100)
Y=np.linspace(-5.12,5.12, 100)   
'''
# Creating dataset
X = np.linspace(-5.12, 5.12, 100)
Y = np.linspace(-5.12, 5.12, 100)

X,Y = np.meshgrid(X, Y)
fig = plt.figure(figsize =(14, 9))
ax = plt.axes(projection ='3d')

x=np.array(X)
y=np.array(Y)

#Rastrigin 3D function
def rastrigin(X,Y):
    return  (X**2 - 10 * np.cos(2 * np.pi * X)) + (Y**2 - 10 * np.cos(2 * np.pi * Y)) + 20
rastrigin_vectorized = np.vectorize(rastrigin)
Z=rastrigin_vectorized(x,y)



# Set axes label
ax.set_xlabel('x', labelpad=20)
ax.set_ylabel('y', labelpad=20)
ax.set_zlabel('z', labelpad=20)




#plot rastrigin:
surf = ax.plot_surface(x, y, Z, cmap = plt.cm.cividis)
fig.colorbar(surf, shrink=0.5, aspect=8)
# Adding labels
ax.set_xlabel('X-axis')
ax.set_xlim(-5, 5)
ax.set_ylabel('Y-xis')
ax.set_ylim(-5, 5)
ax.set_zlabel('Z-axis')
ax.set_zlim(np.min(Z), np.max(Z))
ax.set_title('3D surface having 2D contour plot projections')
 
# show plot
plt.show()

#And now we gonna optimize it !
#1-declare constants:
W = 0.5
c1 = 0.8
c2 = 0.9 
n_iterations = int(input("Inform the number of iterations: "))
target_error = float(input("Inform the target error: "))
n_particles = int(input("Inform the number of particles: "))

#2-create swarm particle class:
class Particle:
    def __init__(self):
        self.position=np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])         # particle position
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([0,0])             
        
    def move(self):
        self.position = self.position + self.velocity 
#3-create the space search class:
class Space:
    def __init__(self,target, target_error, n_particles):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random()*50, random.random()*50])
    
    def fitness(self, particle):
        x=particle.position[0]
        y=particle.position[1]
        return (x**2 - 10 * math.cos(2 * math.pi * x)) + (y**2 - 10 * math.cos(2 * math.pi * y)) + 20
    
    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = self.fitness(particle)
            if(particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position
    
    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = self.fitness(particle)
            
            if(self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position
    
    def move_particles(self):
        for particle in self.particles:
            global W
            new_velocity = (W*particle.velocity) + (c1*random.random()) * (particle.pbest_position - particle.position) + \
                            (random.random()*c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()
            
search_space = Space(0, target_error, n_particles)
particles_vector = [Particle() for _ in range(search_space.n_particles)]
search_space.particles = particles_vector
#search_space.print_particles()
iteration = 0


while(iteration < n_iterations):
    search_space.set_pbest()    
    search_space.set_gbest()

    if(abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
        break

    search_space.move_particles()
    iteration =iteration+1 
print("The best solution is: ", search_space.gbest_position,"with value: ",search_space.gbest_value, " in n_iterations: ", iteration)   
