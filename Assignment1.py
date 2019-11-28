# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:30:09 2019

@author: Kees 't Hooft`
"""

import numpy as np
import random



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
        self.DroneX[self.t+1] = np.min(np.where(np.cumsum(DroneQ[current_state,:])>=w)[0])+1
        self.t += 1
        
        
class Intruder:
    def __init__(self, name, IntX, Intt):
        self.name = name
        self.IntX = IntX
        self.Intt = Intt 
        
    def detSoTime(self):
        room = self.IntX[-1]
        SoTime = np.random.exponential(lambdas[int(self.IntX[-1])-1])
        return SoTime
    
    def newroom(self):
        w = random.random()
        current_state = int(self.IntX[-1]-1)
        room = np.where(np.cumsum(IntruderT[current_state,:]) >= w)[0][0]
        return room
    
    def updateX(self):
        SoTime = self.detSoTime()
        self.Intt.append(SoTime)
        newroom = self.newroom()
        self.IntX = np.append(self.IntX,[newroom])
        return self.IntX, self.Intt


DroneX = np.zeros([1])
DroneX[0] = 7
D1 = Drone('D1', DroneX, 0)

IntX = np.zeros([1])
IntX[0] = 9
I1 = Intruder('I1',IntX,[0])
