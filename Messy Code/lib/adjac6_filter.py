# -*- coding: utf-8 -*-
"""
Created on Wed May 06 15:18:17 2015

@author: Damien
"""
import numpy as np
from evtk.hl import gridToVTK

#6adjacency filter
test = np.array([[[0, 0, 0 ,0 , 0], [0, 0, 0 ,0 , 0], [0, 0, 0 ,0 , 0],[0, 0, 0 ,0 , 0],[0, 0, 0 ,0 , 0]],
                 [[0, 0, 0 ,0 , 0], [0, 1, 0 ,0 , 0], [0, 1, 1 ,0 , 0],[0, 0, 0 ,0 , 0],[0, 0, 0 ,0 , 0]],
                 [[0, 0, 0 ,0 , 0], [0, 0, 0 ,0 , 0], [0, 1, 1 ,0 , 0],[0, 0, 0 ,0 , 0],[0, 0, 0 ,0 , 0]],
                 [[0, 0, 0 ,0 , 0], [0, 0, 0 ,0 , 0], [0, 0, 0 ,0 , 0],[0, 0, 0 ,0 , 0],[0, 0, 0 ,0 , 0]],
                 [[0, 0, 0 ,0 , 0], [0, 0, 0 ,0 , 0], [0, 0, 0 ,0 , 0],[0, 0, 0 ,0 , 0],[0, 0, 0 ,0 , 0]]])
                 
def COUNT(model,i,j,k):
    v5 =  model[i-0,j-1,k-0] # 6       18      26
    v11 = model[i-0,j-0,k-1] # 6       18      26
    v13 = model[i-1,j-0,k-0] # 6       18      26
    v15 = model[i+1,j-0,k-0] # 6       18      26
    v17 = model[i-0,j-0,k+1] # 6       18      26
    v23 = model[i-0,j+1,k-0] # 6       18      26
    ADJ6sum  = np.sum([v5,v11,v13,v15,v17,v23])
    return ADJ6sum 

def filter_1_6(array,dims):
    print "bla"
    new_array = np.zeros([dims,dims,dims],dtype=np.int)
    for k in range(1,dims -1): 
        for j in range(1,dims -1): # -1? back to 0? 
            for i in range(1,dims -1):     # was in range dims[0] -0? 
                if array[i,j,k] == 1:
                    #print 'check'
                    # SET FILTER HERE
                    # [0] for 6  [1] for 18 [2] for 26
                    # storing integers and settings threshold in 
                    #if COUNT(fullmodel,i,j,k)[0] < 6: 
                    if COUNT(array,i,j,k) > 1:
                        new_array[i,j,k] = 1
                    else:   
                        print "BLA"
                        new_array[i,j,k] = 0
                else:
                    new_array[i,j,k] = 0
    #print new_array
    return new_array 
    
#filter_1_6(test,5)

# testing needed? 
#vtkfilename = binvoxfile.replace(".binvox","full")
#NParray2VTK(fullmodel,dims,scale,vtkfilename)    
    



        

     
###############################################################################
# STEP 4 WRITE FULL & FILT MODEL TO VTK
###############################################################################
            
"""
def COUNT(model,i,j,k):
    if model[i,j,k] == 1:
        v1 =  model[i-1,j-1,k-1] #                 26 
        v2 =  model[i-0,j-1,k-1] #         18      26
        v3 =  model[i+1,j-1,k-1] #                 26
        v4 =  model[i-1,j-1,k-0] #         18      26
        v5 =  model[i-0,j-1,k-0] # 6       18      26
        v6 =  model[i+1,j-1,k-0] #         18      26 
        v7 =  model[i-1,j-1,k+1] #                 26 
        v8 =  model[i-0,j-1,k+1] #         18      26 
        v9 =  model[i+1,j-1,k+1] #                 26 
        v10 = model[i-1,j-0,k-1] #         18      26 
        v11 = model[i-0,j-0,k-1] # 6       18      26
        v12 = model[i+1,j-0,k-1] #         18      26 
        v13 = model[i-1,j-0,k-0] # 6       18      26
        #skip v14
        v15 = model[i+1,j-0,k-0] # 6       18      26
        v16 = model[i-1,j-0,k+1] #         18      26 
        v17 = model[i-0,j-0,k+1] # 6       18      26
        v18 = model[i+1,j-0,k+1] #         18      26 
        v19 = model[i-1,j+1,k-1] #                 26 
        v20 = model[i-0,j+1,k-1] #         18      26 
        v21 = model[i+1,j+1,k-1] #                 26 
        v22 = model[i-1,j+1,k-0] #         18      26 
        v23 = model[i-0,j+1,k-0] # 6       18      26
        v24 = model[i+1,j+1,k-0] #         18      26 
        v25 = model[i-1,j+1,k+1] #                 26
        v26 = model[i-0,j+1,k+1] #         18      26 
        v27 = model[i+1,j+1,k+1] #                 26
        ADJ6sum  = np.sum([v5,v11,v13,v15,v17,v23])
        ADJ18sum = np.sum([v2,v4,v5,v6,v8,v10,v11,v12,v13,v15,v16,v17,v18,v20,v22,v23,v24,v26])
        ADJ26sum = np.sum([v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v15,v16,v17,v18,v19,v20,v21,v22,v23,v24,v25,v26,v27])
        return ADJ6sum, ADJ18sum, ADJ26sum    
"""

def NParray2VTK(npmodel,dims,scale,vtkfilename):
    # Dimensions  
    # x, y & z Number of Voxels
    nx, ny, nz = dims[0], dims[1], dims[2]
    # x, y & z Length  
    lx , ly, lz = scale, scale, scale
    # x, y & z Voxel size 
    dx, dy, dz = lx/nx, ly/ny, lz/nz   # all equal
    # Coordinates - change to real pos later?
    # +0.1*dx used to get end value in arange 
    X = np.arange(0,lx+0.1*dx,dx, dtype='float64')  
    Y = np.arange(0,ly+0.1*dy,dy, dtype='float64')
    Z = np.arange(0,lz+0.1*dz,dz, dtype='float64')
    # x, y & z empty arrays
    x = np.zeros((nx + 1, ny + 1, nz + 1)) 
    y = np.zeros((nx + 1, ny + 1, nz + 1))
    z = np.zeros((nx + 1, ny + 1, nz + 1))  
    # Loop to fill position arrays
    for k in range(nz + 1): 
        for j in range(ny + 1):
            for i in range(nx + 1): 
                x[i,j,k] = X[i]  
                y[i,j,k] = Y[j] 
                z[i,j,k] = Z[k] 
    # write to VTK file
    vtkfilename = "./%s" % vtkfilename
    gridToVTK(vtkfilename, x, y, z, cellData = {vtkfilename : npmodel.astype(int)})  
