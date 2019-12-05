# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:30:09 2019

@author: Kees 't Hooft`
"""

# Importing modules
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#-----------------------------------------------------------------------------
# ----------- Q-MATRIX, TRANSITION MATRIX, ECT. USED -------------------------
# ----------------------------------------------------------------------------

DroneQ = np.array([[0,1,0,0,0,0,0,0,0,0],   # 1
                   [0.5,0,0.5,0,0,0,0,0,0,0],   # 2
                   [0,1/3,0,1/3,0,0,1/3,0,0,0], #3
                   [0,0,0.5,0,0.5,0,0,0,0,0],  # 4
                   [0,0,0,0.25,0,0.25,0.25,0,0,0.25],   #5
                   [0,0,0,0,0.5,0,0,0,0.5,0],
                   [0,0,1/3,0,1/3,0,0,1/3,0,0], # 7
                   [0,0,0,0,0,0,0.5,0,0.5,0], # 8 
                   [0,0,0,0,0,0.5,0,0.5,0,0],    # 9 
                   [0,0,0,1,0,0,0,0,0,0]])

lambdas = np.array([0.447213595,
                    0.547722558,
                    0.632455532,
                    0.707106781,
                    0.774596669,
                    0.836660027,
                    0.894427191,
                    0.948683298,
                    1.0,
                    1.048808848])

lambdas_inverse = np.array([22.00220022,
                    11.00110011,
                    7.333528894,
                    11.00110011,
                    5.500550055,
                    11.00110011,
                    7.333528894,
                    11.00110011,
                    11.00110011,
                    22.00220022])

lambdas_pronounced = np.array([587.6448667,
                    17.14124947,
                    5.275657607,
                    17.14124947,
                    2.927562934,
                    17.14124947,
                    5.275657607,
                    17.14124947,
                    17.14124947,
                    587.6448667])

IntruderQ = np.array([[-lambdas[0],lambdas[0],0,0,0,0,0,0,0,0],
                      [0.5*lambdas[1],-lambdas[1],0.5*lambdas[1],0,0,0,0,0,0,0],
                      [0,lambdas[2]/3,-lambdas[2],lambdas[2]/3,0,0,lambdas[2]/3,0,0,0],
                      [0,0,lambdas[3]/2,-lambdas[3],lambdas[3]/2,0,0,0,0,0],
                      [0,0,0,lambdas[4]/4,-lambdas[4],lambdas[4]/4,lambdas[4]/4,0,0,lambdas[4]],
                      [0,0,0,0,lambdas[5]/2,-lambdas[5],0,0,lambdas[5]/2,0],
                      [0,0,lambdas[6]/3,0,lambdas[6]/3,0,-lambdas[6],lambdas[6]/3,0,0],
                      [0,0,0,0,0,0,lambdas[7]/2,-lambdas[7],lambdas[7]/2,0],
                      [0,0,0,0,0,lambdas[8]/2,0,lambdas[8]/2,-lambdas[8],0],
                      [0,0,0,0,lambdas[9],0,0,0,0,-lambdas[9]]])

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

# ----------------------------------------------------------------------------
# ----------- INPUT PARAMETERS TO DETERMINE INTRUDER'S STRATEGY --------------
# ----------------------------------------------------------------------------
# Change these if the user wants to alter the strategy of the intruder.

# Which lambda values to use:
# choose: lambdas (original values), lambdas_inverse (inverse of stationary matrix)...
# lambdas_pronounced (pronounced version of lambdas_inverse)
lambda_array = lambdas_pronounced 

# Stay in room 10 for 180 mins
stay10 = False

# Run to room 10
run10 = True

# Stay in room 1 for 180 mins
stay1 = False

# Run to room 1
run1 = False

# Make a histogram
makeplot = False

# Number of simulation runs
sims = 500000

# ----------------------------------------------------------------------------
# ----------- INPUT PARAMETERS TO DETERMINE INTRUDER'S STRATEGY --------------
# ----------------------------------------------------------------------------


def nextstate_drone(t):
    w = random.random()
    current_state = int(DroneX[i]-1)
    DroneX[i+1] = np.min(np.where(np.cumsum(DroneQ[current_state,:])>=w)[0])+1
    return DroneX


class Drone:
    def __init__(self, name, DroneX, t):
        self.name = name
        self.DroneX = DroneX
        self.t = t
        
    def updateX(self):
        w = random.random()
        current_state = int(self.DroneX[self.t]-1)
        #self.DroneX[self.t+1] = np.min(np.where(np.cumsum(DroneQ[current_state,:])>=w)[0])+1
        #self.DroneX.append(np.min(np.where(np.cumsum(DroneQ[current_state,:])>=w)[0])+1)
        self.DroneX = np.append(self.DroneX, np.asarray([np.min(np.where(np.cumsum(DroneQ[current_state,:])>=w)[0])+1]))
        self.t += 1
        
    def getTime(self):
        time = self.t + 1
        return time
        
class Intruder:
    def __init__(self, name, IntX, Intt):
        self.name = name
        self.IntX = IntX
        self.Intt = Intt 
        
    def detSoTime(self):
        room = self.IntX[-1]
        SoTime = np.random.exponential(lambda_array[int(self.IntX[-1])-1])
        return SoTime
    
    def newroom(self):
        w = random.random()
        current_state = int(self.IntX[-1]-1)   # index
        room = np.where(np.cumsum(IntruderT[current_state,:]) >= w)[0][0] + 1
        return room
    
    def updateX(self):
        SoTime = self.detSoTime()
        self.Intt.append(SoTime)
        newroom = self.newroom()
        self.IntX = np.append(self.IntX,[newroom])
        return self.IntX, self.Intt
    
    def getTime(self):
        time = sum(self.Intt)
        return time
    
# Returns True if we need to update the Drone's position
def nextToUpdate(Drone,Intruder):
    if Drone.getTime() < Intruder.getTime():
        return True
    else:
        return False


 
# Returns time of collision if there is collision, else returns False
def Collision(Drone,Intruder):
    #lower bound
    
    if DroneUpdate==True:
        Timelower = Drone.t
        Timeupper = Drone.t + 1
        RoomD = Drone.DroneX[-1]
        roomIdown = I1.IntX[np.where(np.cumsum(I1.Intt) >= Drone.t)[0][0]]
        if roomIdown == RoomD:
            return Timelower, RoomD
        
        # Checking if there are more Intruder movements which cause collision
        TimeLimit = Timelower
        IndexLimit = np.where(np.cumsum(Intruder.Intt) >= Drone.t)[0][0]
        IndexLimit += 1    
        while len(Intruder.Intt) > IndexLimit:
            if Intruder.Intt[IndexLimit - 1] < Timeupper:
                if RoomD == Intruder.IntX[IndexLimit]:
                    return Intruder.Intt[IndexLimit - 1], RoomD
            else:
                IndexLimit += 1
                
    if DroneUpdate==False:
        Timelower = sum(Intruder.Intt) - Intruder.Intt[-1]
        DroneTimelower = int(Timelower)
        if Intruder.IntX[-2] == Drone.DroneX[DroneTimelower]:
            return Timelower, Intruder.IntX[-2]
        
        

# ----------------------------------------------------------------------------
# ----------- INPUT PARAMETERS TO DETERMINE INTRUDER'S STRATEGY --------------
# ----------------------------------------------------------------------------
 
        
        
TimeToCollision = []
CollisionByRoom = [[],[],[],[],[], [],[],[],[],[]]   


for i in range(sims):
    if i%100==0:
        print(i)
    DroneX = np.zeros([1])
    DroneX[0] = 7
    D1 = Drone('D1', DroneX, 0)

    if stay10==False and stay1==False and run10 == False and run1 == False:
        IntX = np.zeros([1])
        IntX[0] = 9
        I1 = Intruder('I1',IntX,[])
        I1.updateX()
     
    elif stay10 == True:        
        IntX = np.array([9,6,5,10])
        I1 = Intruder('I1',IntX,[0.01,0.01,0.01])
        I1.updateX()
        
    elif run10 == True:
        IntX = np.array([9,6,5,10,5])
        I1 = Intruder('I1',IntX,[0.01,0.01,0.01,180.1])
        I1.updateX()
        
    elif stay1 == True:
        IntX = np.array([9,8,7,3,2,1])
        I1 = Intruder('I1',IntX,[0.01,0.01,0.01,0.01])
        I1.updateX()
        
    else:
        IntX = np.array([9,8,7,3,2,1,2])
        I1 = Intruder('I1',IntX,[0.01,0.01,0.01,0.01, 180.1])
        I1.updateX()
    
    Collided = False

    
    while Collided != True:
        if nextToUpdate(D1,I1) ==True:
            DroneUpdate = True
            IntUpdate = False
            D1.updateX()
        else:
            DroneUpdate = False
            IntUpdate = True
            I1.updateX()
            
        if stay10 == False and stay1 == False:
            if Collision(D1,I1) != None:
                #print(Collision(D1,I1))
                TimeToCollision.append(Collision(D1,I1)[0])
                CollisionByRoom[int(Collision(D1,I1)[1]) - 1].append(Collision(D1,I1)[0])
                Collided = True
                break
        
        if stay10 == True or stay1 == True:
            if D1.DroneX[-1]==10:
                TimeToCollision.append(D1.t)
                Collided = True
                break

# matplotlib histogram

            
#asdf = plt.hist(CollisionByRoom[9], color = 'blue', edgecolor = 'black',
     #    bins = 1000)
# Add labels
if makeplot == True:
    asdf = plt.hist(TimeToCollision, color = 'blue', edgecolor = 'black',
         bins = 80)
    plt.title('Distribution of time it takes for Drone to catch Intruder at room 10')
    plt.xlabel('Time taken (mins)')
    plt.ylabel('Occurances')
    axes = plt.gca()
    axes.set_xlim([0,50])
    #axes.set_ylim([0,100])    
    plt.savefig('asdf.png')
    
    
print("")
print(sum(TimeToCollision)/len(TimeToCollision))