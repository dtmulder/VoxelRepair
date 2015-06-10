# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 11:39:32 2015

@author: Damien
"""
import binvox_rw
import numpy as np

##############################################################################
# BINVOX 2 NP ARRAY                                                          #
##############################################################################

def binvoxToArray(binvoxfile):
    with open(binvoxfile,'rb') as f:
        array = binvox_rw.read_as_3d_array(f)
    return array
    
def bufferArray(array):
    # buffer 3d array
    olddims = array.dims # old dims before buffer
    oldscale = array.scale  # old scale before buffer
    oldtranslate = array.translate # old translate before buffer
    voxelsize = oldscale/olddims[0]
    # buffer model
    model = np.zeros( (olddims[0]+2,olddims[1]+2,olddims[2]+2))    
    model[1:olddims[0]+1,1:olddims[1]+1,1:olddims[2]+1]=array.data
    # update dims    
    dims = [x+2 for x in olddims]
    # update scale
    scale = oldscale + 2*voxelsize
    # update translate 
    translate = [x-voxelsize for x in oldtranslate]
    return model,dims,scale,translate,voxelsize
    # as dict? 