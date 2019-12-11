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

#%%Part Bii: Find the expectation of x3 given x1=7 (simulation) (analytically via excel)
stepsBii = 3                    #amount of necessary steps
simulationsBii = 500000         #amount of simulations
x13Bii = np.zeros(stepsBii)     #empty set of zeros with length of necessary steps
x13Bii[0] = 7                   #start in room 7
x3listBii = []                  #empty list to append final room in simulations

room2 = []                      #empty list to count occurances in room 2
room4 = []                      #empty list to count occurances in room 4
room6 = []                      #empty list to count occurances in room 6
room7 = []                      #empty list to count occurances in room 7
room9 = []                      #empty list to count occurances in room 9
room10 = []                     #empty list to count occurances in room 10

for i in range(simulationsBii):
    for j in range(stepsBii-1):
        w = random.random()
        current_position = int(x13Bii[j]-1)
        x13Bii[j+1] = np.min(np.where(np.cumsum(IntruderT[current_position,:])>=w)[0])+1 #random room following transition matrix 
    x3listBii.append(x13Bii[-1])            #append final room in one simulations

for rooms in range(len(x3listBii)):         #being counting and sorting where drone ends up
    if x3listBii[rooms] == 2:
        room2.append(x3listBii[rooms])      #append if in room 2
    if x3listBii[rooms] == 4:
        room4.append(x3listBii[rooms])      #append if in room 4
    if x3listBii[rooms] == 6:
        room6.append(x3listBii[rooms])      #append if in room 6
    if x3listBii[rooms] == 7:
        room7.append(x3listBii[rooms])      #append if in room 7
    if x3listBii[rooms] == 9:
        room9.append(x3listBii[rooms])      #append if in room 9
    if x3listBii[rooms] == 10:
        room10.append(x3listBii[rooms])     #append if in room 10
        
#print probability of drone ending up in rooms 2,4,6,7,9,10
print(round(len(room2)/simulationsBii,2), round(len(room4)/simulationsBii,2), round(len(room6)/simulationsBii,2), round(len(room7)/simulationsBii,2), round(len(room9)/simulationsBii,2), round(len(room10)/simulationsBii,2))


#%%Part C: Stationary Matrix
S, U = eig(IntruderT.T)
stationaryC = np.array(U[:, np.where(np.abs(S - 1.) < 1e-8)[0][0]].flat)
stationaryC = stationaryC / np.sum(stationaryC)


evals, evecs = np.linalg.eig(IntruderT.T)
evec1 = evecs[:,np.isclose(evals, 1)]

#Since np.isclose will return an array, we've indexed with an array
#so we still have our 2nd axis.  Get rid of it, since it's only size 1.
evec1 = evec1[:,0]

stationary1 = evec1 / evec1.sum()

#eigs finds complex eigenvalues and eigenvectors, so you'll want the real part.
stationary1 = stationaryC.real

#%%Part D: Expected time from room 9 to room 10
lambdas = np.array([0.447213595,                        #set up of intruder lambdas
                    0.547722558,
                    0.632455532,
                    0.707106781,
                    0.774596669,
                    0.836660027,
                    0.894427191,
                    0.948683298,
                    1.0,
                    1.048808848])
    
matrix = np.array([[-1,1.0,0,0,0,0,0,0,0,0],            #set up of matrix
                      [0.5,-1,0.5,0,0,0,0,0,0,0],
                      [0,1/3,-1,1/3,0,0,1/3,0,0,0],
                      [0,0,1/2,-1,1/2,0,0,0,0,0],
                      [0,0,0,1/4,-1,1/4,1/4,0,0,1/4],
                      [0,0,0,0,1/2,-1,0,0,1/2,0],
                      [0,0,1/3,0,1/3,0,-1,1/3,0,0],
                      [0,0,0,0,0,0,1/2,-1,1/2,0],
                      [0,0,0,0,0,1/2,0,1/2,-1,0],
                      [0,0,0,0,0,0,0,0,0,-1]])
ans = []
for i in range(10):                                     #gathering -1/lambda
    ans.append(-1/lambdas[i])
ans[-1] = 0                                             #setting last value of answer to 0
ans = np.array(ans)                                     #converting to numpy array
 
expectation = np.linalg.solve(matrix,ans)                    #calculation of expected time

#%%Part E: Finding the probability that X1 != X3 (simulation) (analytically via excel)
stepsE = 3                  #steps necessary for probability
x13E = np.zeros(stepsE)     #empty set of zeros with length necessary steps
notequalsE = 0              #set count at 0
neqlistE = []               #empty list to later append not equals count
for k in range(10000):
    for i in range(len(IntruderT)):
        x13E[0] = i+1                       #for each simulations ensure that you start in all rooms
        for j in range(stepsE-1):
            w = random.random()
            current_position = int(x13E[j]-1)
            x13E[j+1] = np.min(np.where(np.cumsum(IntruderT[current_position,:])>=w)[0])+1
        if x13E[0] != x13E[2]:              #find when room at x1 does not equal room at x3
            notequalsE += 1                 #add to count when this occurs
    neqlistE.append(notequalsE/((k+1)*10))  #append probability of x1 != x3 for every simulation run

plt.style.use('seaborn-darkgrid')
plt.plot(neqlistE[100:])                    #ignore first results to have a clearer graph
plt.xlabel('Simulations')
plt.ylabel('Probability')
plt.show()
print(np.mean(neqlistE[100:10000]))     #find the probability based on simulation

