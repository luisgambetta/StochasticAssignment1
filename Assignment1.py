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

lambdas_inverse = np.array([1/22.00220022,
                    1/11.00110011,
                    1/7.333528894,
                    1/11.00110011,
                    1/5.500550055,
                    1/11.00110011,
                    1/7.333528894,
                    1/11.00110011,
                    1/11.00110011,
                    1/22.00220022])

lambdas_pronounced = np.array([1/587.6448667,
                    1/17.14124947,
                    1/5.275657607,
                    1/17.14124947,
                    1/2.927562934,
                    1/17.14124947,
                    1/5.275657607,
                    1/17.14124947,
                    1/17.14124947,
                    1/587.6448667])

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
lambda_array = lambdas

# Stay in room 10 for 180 mins
stay10 = False

# Run to room 10
run10 = False

# Stay in room 1 for 180 mins
stay1 = False

# Run to room 1
run1 = False

# SoJourn time always rounding up to nearest integer 
# roundup = False

# Make a histogram
makeplot = True

# Number of simulation runs
sims = 50000

# ----------------------------------------------------------------------------
# ------Establishing drone and intruder functions to be used in sim ----------
# ----------------------------------------------------------------------------

# returns the next room the drone will be in, given the time since entering house
# NOT USED 
def nextstate_drone(t):
    w = random.random()
    current_state = int(DroneX[i]-1)
    DroneX[i+1] = np.min(np.where(np.cumsum(DroneQ[current_state,:])>=w)[0])+1
    return DroneX

# making a class for the drone
class Drone:
    # attributes
    # DroneX = a list of the rooms visited by the drone
    # t = the time of the most recent addition to DroneX (the current timestep the drone is on)
    def __init__(self, name, DroneX, t):
        self.name = name
        self.DroneX = DroneX
        self.t = t
        
    # This fuctions updates the drone's position and time parameter.     
    def updateX(self):
        w = random.random()
        current_state = int(self.DroneX[self.t]-1)
        # determines the next room to enter, by giving neighboring rooms equal probability
        self.DroneX = np.append(self.DroneX, np.asarray([np.min(np.where(np.cumsum(DroneQ[current_state,:])>=w)[0])+1]))
        self.t += 1
        
    # simply returns the time of the most recent addition to the drone's path
    def getTime(self):
        time = self.t + 1
        return time
        
# Establish class for intruder
class Intruder:
    # attributes:
    # IntX = the list of the rooms the intruder visits
    # Intt = a list of the time spent in each of the rooms
    def __init__(self, name, IntX, Intt):
        self.name = name
        self.IntX = IntX
        self.Intt = Intt 
     
    # Determines Sojourn Time (time spent in room), dependant on which room intruder is in    
    def detSoTime(self):
        room = self.IntX[-1]
        SoTime = np.random.exponential(1/(lambda_array[int(self.IntX[-1])-1]))
        if roundup == True:
            SoTime = math.ceil(SoTime)
        return SoTime
    
    # Finds the next room the intruder should enter
    def newroom(self):
        w = random.random()
        current_state = int(self.IntX[-1]-1)   # index
        room = np.where(np.cumsum(IntruderT[current_state,:]) >= w)[0][0] + 1
        return room
    
    # Updates the intruders room (IntX) and time (Intt) attributes
    def updateX(self):
        SoTime = self.detSoTime()
        self.Intt.append(SoTime)
        newroom = self.newroom()
        self.IntX = np.append(self.IntX,[newroom])
        return self.IntX, self.Intt
    
    # Get's the time of the most recent addition to the intruders path
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
# Does this by checking the most recently updated path between the two agents
def Collision(Drone,Intruder):
    
    # If the drone was last to update, check whether the last movement of the drone 
    # forced it to find the intruder
    if DroneUpdate==True:
        Timelower = Drone.t
        Timeupper = Drone.t + 1
        RoomD = Drone.DroneX[-1]
        roomIdown = I1.IntX[np.where(np.cumsum(I1.Intt) >= Drone.t)[0][0]]
        
        # first check if the drone finds the intruder by moving into it's room
        if roomIdown == RoomD:
            return Timelower, RoomD
        else:
            return False
        
        TimeLimit = Timelower
        IndexLimit = np.where(np.cumsum(Intruder.Intt) >= Drone.t)[0][0]
        IndexLimit += 1    
        while len(Intruder.Intt) > IndexLimit:
            if Intruder.Intt[IndexLimit - 1] < Timeupper:
                if RoomD == Intruder.IntX[IndexLimit]:
                    return Intruder.Intt[IndexLimit - 1], RoomD
                else:
                    return False
            else:
                IndexLimit += 1
    # If the drone was updated last, check whether or not it's most recent movement
    # caused it to be found            
    if DroneUpdate==False:
        Timelower = sum(Intruder.Intt) - Intruder.Intt[-1]
        DroneTimelower = int(Timelower)
        if Intruder.IntX[-2] == Drone.DroneX[DroneTimelower]:
            return Timelower, Intruder.IntX[-2]
        else:
            return False
 
       

# ----------------------------------------------------------------------------
# ----------- Running simulation loop --------------
# ----------------------------------------------------------------------------
 
        
        
TimeToCollision = []
CollisionByRoom = [[],[],[],[],[], [],[],[],[],[]]   


for i in range(sims):
    if i%100==0:
        print(i)
    DroneX = np.zeros([1])
    DroneX[0] = 7
    D1 = Drone('D1', DroneX, 0)

    # determining the intruder's intial movements depending on which strategy is used
    if stay10==False and stay1==False and run10 == False and run1 == False:
        IntX = np.zeros([1])
        IntX[0] = 9
        I1 = Intruder('I1',IntX,[])
        I1.updateX()
     
    elif stay10 == True:        
        IntX = np.array([9,6,5,10,5])
        I1 = Intruder('I1',IntX,[0.01,0.01,0.01,180.1])
        I1.updateX()
        
    elif run10 == True:
        IntX = np.array([9,6,5,10])
        I1 = Intruder('I1',IntX,[0.1,0.1,0.1])
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

    
    while Collided == False:
        if nextToUpdate(D1,I1) ==True:
            DroneUpdate = True
            IntUpdate = False
            D1.updateX()
        else:
            DroneUpdate = False
            IntUpdate = True
            I1.updateX()
            
        if D1.t >= 180:
            TimeToCollision.append(180)
            Collided = True
            break
            
        if stay10 == False and stay1 == False:
            if Collision(D1,I1) != False:
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
            
        
# ----------------------------------------------------------------------------
# ----------- Makes histogram plot if requried --------------
# ----------------------------------------------------------------------------
 
if makeplot == True:
    asdf = plt.hist(TimeToCollision, color = 'blue', edgecolor = 'blue',
         bins = 600)

    plt.title('Distribution of time it takes for Drone to catch Intruder at room 10')
    plt.xlabel('Time taken (mins)')
    plt.ylabel('Occurances')
    plt.style.use('seaborn-darkgrid')
    axes = plt.gca()
    axes.set_xlim([0,40])
    #axes.set_ylim([0,100])    
    plt.savefig('asdf.png')
    
    
    
# print final results    
print("")
print(sum(TimeToCollision)/len(TimeToCollision))
