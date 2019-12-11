import numpy as np
import random
from scipy.linalg import eig 
from matplotlib import pyplot as plt
import seaborn as sns

#Length of steps
T = 1000

#Transition matrix
IntruderT = np.array([[0,1.0,0,0,0,0,0,0,0,0],
                      [0.5,0,0.5,0,0,0,0,0,0,0],
                      [0,1/3,0,1/3,0,0,1/3,0,0,0],
                      [0,0,1/2,0,1/2,0,0,0,0,0],
                      [0,0,0,1/4,0,1/4,1/4,0,0,1/4],
                      [0,0,0,0,1/2,0,0,0,1/2,0],
                      [0,0,1/3,0,1/3,0,0,1/3,0,0],
                      [0,0,0,0,0,0,1/2,0,1/2,0],
                      [0,0,0,0,0,1/2,0,1/2,0,0],
                      [0,0,0,0,1,0,0,0,0,0]])

#%%Part Bi: find px4|x5,x2 of room 2 at x4 given that at x5 and x2 it is in room 3 and 4 respectively (simulation) (analyticalls via excel)
stepsBi = 4                 #amount of necessary steps
simulationsBi = 50000       #amount of simulations necessary
x13Bi = np.zeros(stepsBi)   #empty set of zeros with length of necessary steps
x13Bi[0] = 4                #start in room 4
occasionsBi = 0             #begin count when x5 = 3 and x2 = 4 is met
possibilitiesBi = 0         #begin count when all conditions met
probabilityBi = []          #empty list for appendicing the count
for i in range(simulationsBi):
    for j in range(stepsBi-1):
        w = random.random()
        current_position = int(x13Bi[j]-1)
        x13Bi[j+1] = np.min(np.where(np.cumsum(IntruderT[current_position,:])>=w)[0])+1 #random room following transition matrix
    if x13Bi[-1] == 3:          #look to see if x5 condition is met
        possibilitiesBi += 1    #add to count when condition is met
        if x13Bi[2] == 2:       #look to see if in room 2 at x4
            occasionsBi += 1    #add to count when condition is met
        probabilityBi.append(occasionsBi/possibilitiesBi)   #append probability of scenario happening

#plot probability graph
plt.style.use('seaborn-darkgrid')
plt.plot(probabilityBi[25:])            #ignore first few results for cleaner graph
plt.show()
print(np.mean(probabilityBi[25:]))      #print probability based on simulation

