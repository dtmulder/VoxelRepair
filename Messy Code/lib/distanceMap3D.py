# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 17:06:56 2015

@author: Damien
"""
import numpy as np

def distanceMap3D(array):                
    # initialize distance map
    shape = array.shape
    dims = shape[0]
    b = np.copy(array)
    maxval = 99999999
    b[b==0] = maxval
    b[b==1] = 0
    # K TOP DOWN SCAN
    for k in range(1,dims): #1,2,3,4
        # J TOP DOWN SCAN
        for j in range(1,dims):
            # check below    
            for i in range(0,dims): # 0,1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k,j-1,i] + 1)])
            # check left         
            for i in range(1,dims): #     1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k,j,i-1] + 1)])
            # check right
            for i in range(dims-2,-1,-1):  # 3,2,1,0
                b[k,j,i] = min([(b[k,j,i]),(b[k,j,i+1] + 1)])

        # J BOTTOM UP SCAN
        for j in range(dims-2,-1,-1):
            # check above 
            for i in range(0,dims): # 0,1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k,j+1,i] + 1)])
            # check to the left    
            for i in range(1,dims): # 1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k,j,i-1] + 1)])
            # check tot he right    
            for i in range(dims-2,-1,-1): # 3,2,1,0
                b[k,j,i] = min([(b[k,j,i]),(b[k,j,i+1] + 1)])
        # K CHECK    
        for j in range(0,dims):
            #check below 
            for i in range(0,dims):
                b[k,j,i] = min([(b[k,j,i]),(b[k-1,j,i] +1)])     

   # K BOTTOM UP SCAN
    for k in range(dims-2,-1,-1): # 3,2,1,0
        for j in range(1,dims):
            # check below    
            for i in range(0,dims): # 0,1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k,j-1,i] + 1)])
            # check to the left         
            for i in range(1,dims): #     1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k,j,i-1] + 1)])
            # check to the right
            for i in range(dims-2,-1,-1):  # 3,2,1,0
                b[k,j,i] = min([(b[k,j,i]),(b[k,j,i+1] + 1)])
    # J BOTTOM UP SCAN
        for j in range(dims-2,-1,-1):
            # check above 
            for i in range(0,dims): # 0,1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k,j+1,i] + 1)])
            # check to the left    
            for i in range(1,dims): # 1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k,j,i-1] + 1)])
            # check tot he right    
            for i in range(dims-2,-1,-1): # 3,2,1,0
                b[k,j,i] = min([(b[k,j,i]),(b[k,j,i+1] + 1)])
        # K CHECK    
        for j in range(0,dims): # 0,1,2,3,4
            for i in range(0,dims): # 0,1,2,3,4
                b[k,j,i] = min([(b[k,j,i]),(b[k+1,j,i] +1)])

    return b
