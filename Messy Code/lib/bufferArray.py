# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:38:34 2015

@author: Damien
"""

import numpy as np

##############################################################################
# BUFFER ARRAY                                                               #
##############################################################################
def bufferArray(array,dims,scale,translate): # later add translate
    # buffer 3d array
    voxelsize = scale/dims 
    # buffer model
    model = np.zeros( (dims+2,dims+2,dims+2))    
    model[1:dims+1,1:dims+1,1:dims+1]=array
    # update dims    
    new_dims = dims+2
    # update scale
    new_scale = scale + 2*voxelsize
    # update translate 
    new_translate = [val-voxelsize for val in translate]
    return model,new_dims,new_scale,new_translate  # later add new_translate
    # as dict? 
    
"""    
a = np.array([[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
                [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
                [[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0]],
                [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
                [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]])
print a
print bufferArray(a,5,1.1,[0.0,0.0,0.0])[0]
"""