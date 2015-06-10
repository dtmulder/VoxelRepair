# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:13:05 2015

@author: Damien
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 17:05:58 2015

@author: Damien
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:51:43 2015

@author: Damien
"""

import numpy as np

##############################################################################
# 2D EXAMPLE                                                                 #
##############################################################################
array = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0]])
print array

def distanceMap2D(array):
    # initialize distance map
    shape = array.shape
    dims = shape[0]
    b = np.copy(array)
    maxval = 99999999
    b[b==0] = maxval
    b[b==1] = 0
    #print b
    # TOP DOWN SCAN
    for j in range(1,dims):
        # check below    
        for i in range(0,dims): # 0,1,2,3,4
            b[i,j] = min([(b[i,j]),(b[i,j-1] + 1)])
        
        # check to the left         
        for i in range(1,dims): #     1,2,3,4
            b[i,j] = min([(b[i,j]),(b[i-1,j] + 1)])
        
        # check to the right
        for i in range(dims-2,-1,-1):  # 3,2,1,0
            b[i,j] = min([(b[i,j]),(b[i+1,j] + 1)])  
    # BOTTOM UP SCAN
    for j in range(dims-2,-1,-1):
        # check above 
        for i in range(0,dims): # 0,1,2,3,4
            b[i,j] = min([(b[i,j]),(b[i,j+1] + 1)])
    
        # check to the left    
        for i in range(1,dims): # 1,2,3,4
            b[i,j] = min([(b[i,j]),(b[i-1,j] + 1)])
    
        # check tot he right    
        for i in range(dims-2,-1,-1): # 3,2,1,0
            b[i,j] = min([(b[i,j]),(b[i+1,j] + 1)])
    return b
print distanceMap2D(array)
