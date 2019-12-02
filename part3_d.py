import numpy as np
import random
from scipy.linalg import eig 
from matplotlib import pyplot as plt

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


X = np.zeros(T)
#start matrix at room 9
X[0] = 9

#empty lists to append steps
difflist = []
difflist1 = []

intruder = np.array([])


#creating matrix with random path; run for 1000 runs
#append amount of time from room 9 to 10 for each run
for j in range(1000):
    for i in range(0,T-1):
        w = random.random()
        current_position = int(X[i]-1)
        X[i+1] = np.min(np.where(np.cumsum(IntruderT[current_position,:])>=w)[0])+1
    k = X.tolist().index(10)
    difflist.append(k)


#finding rolling average of time it took to get from room 9 to 10
for i in range(len(difflist)):
    difflist1.append(np.mean(difflist[:i]))


#plot the number of simulations vs the amount of steps it took for the intruder to get from room 9 to 10
difflist1 = difflist1[1:]
plt.plot(difflist1)
plt.xlabel('Simulations')
plt.ylabel('Average number of steps')
plt.show()


#Stationary Matrix
S, U = eig(IntruderT.T)
stationary = np.array(U[:, np.where(np.abs(S - 1.) < 1e-8)[0][0]].flat)
stationary = stationary / np.sum(stationary)


evals, evecs = np.linalg.eig(IntruderT.T)
evec1 = evecs[:,np.isclose(evals, 1)]

#Since np.isclose will return an array, we've indexed with an array
#so we still have our 2nd axis.  Get rid of it, since it's only size 1.
evec1 = evec1[:,0]

stationary1 = evec1 / evec1.sum()

#eigs finds complex eigenvalues and eigenvectors, so you'll want the real part.
stationary1 = stationary.real


