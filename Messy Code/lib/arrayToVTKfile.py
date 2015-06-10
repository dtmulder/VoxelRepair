# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 11:47:56 2015

@author: Damien
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 02 12:11:55 2015

@author: Damien
"""

# BINVOX to VTK 
import numpy as np
#import binvox_rw
from evtk.hl import gridToVTK


##############################################################################
# BINVOX TO VTK FILE                                                         #
##############################################################################
def arrayToVTKfile(vtkfilename,array,dims,scale,translate,voxelsize):
#def main(binvoxfile):
    # OPEN BINVOX FILE AS NP ARRAY
    
    
    # buffer 3d array
    #olddims = tempmodel.dims # old dims before buffer
    #oldscale = tempmodel.scale  # old scale before buffer
    #oldtranslate = tempmodel.translate # old translate before buffer
    #voxelsize = oldscale/olddims[0]
    #print "voxelsize = %s "  % (voxelsize)
    # BUFFER THE ARRAY 
    #model = np.zeros( (olddims[0]+2,olddims[1]+2,olddims[2]+2))    
    #model[1:olddims[0]+1,1:olddims[1]+1,1:olddims[2]+1]=tempmodel.data
    #dims = [x+2 for x in olddims]
    #print dims
    #scale = oldscale + 2*voxelsize
    #translate = [x-voxelsize for x in oldtranslate]
    
    # WRITE TO VTK 
    
    #dims = dims[0]
    #vtkfilename = binvoxfile.replace(".binvox","")
    # Dimensions  
    # x, y & z Number of Voxels
    nx, ny, nz = dims,dims,dims
    # x, y & z Length  
    lx , ly, lz = scale,scale,scale
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
    gridToVTK(vtkfilename, x, y, z, cellData = {vtkfilename : array.astype(int)})

    
#if __name__ == "__main__":
    #main("testGeom_64.binvox")    
    #main("montreal131.binvox")