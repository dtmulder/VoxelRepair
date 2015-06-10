# -*- coding: utf-8 -*-
"""
Created on Sun Apr 05 00:29:36 2015

@author: Damien
"""
import numpy as np

def reduce(array,dims):
    dims_new = dims/2
    b = np.zeros((dims_new,dims_new,dims_new))
    for k in range(0,dims,2):
        #print k
        for j in range(0,dims,2):
            for i in range(0,dims,2):
                temp = array[i:i+2,j:j+2,k:k+2]
                #print temp
                #print np.sum(temp)
                # FILTER WITH SUM? 
                # DIFFERENT FILTER? 
                if np.sum(temp) > 4:
                    b[i/2,j/2,k/2] = 1
                
    return b,dims_new
