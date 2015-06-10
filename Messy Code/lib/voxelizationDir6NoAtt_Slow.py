# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:43:58 2015

@author: Damien
"""

import vtk 
import numpy as np
from evtk.hl import gridToVTK
import math


##############################################################################
# load surface as vtk polydata                                               #
##############################################################################
def loadOBJforVTK(filenameOBJ):
    readerOBJ = vtk.vtkOBJReader()
    readerOBJ.SetFileName(filenameOBJ)
    # 'update' the reader i.e. read the .stl file
    readerOBJ.Update()
    polydata = readerOBJ.GetOutput()
    # If there are no points in 'vtkPolyData' something went wrong
    if polydata.GetNumberOfPoints() == 0:
        raise ValueError(
            "No point data could be loaded from '" + filenameOBJ)
        return None
    return polydata

##############################################################################
# Bounding box class (for convenience)                                       #
##############################################################################            
class BoundingBox(object):
    def __init__(self, minX, maxX, minY, maxY, minZ, maxZ):
        self.minX,self.maxX = minX,maxX
        self.minY,self.maxY = minY,maxY
        self.minZ,self.maxZ = minZ,maxZ
        self.full = [(minX,minY,minZ),(maxX,maxY,maxZ)]
        
##############################################################################
# Create bounding box from vertlist                                          #
##############################################################################        
def verts_to_bbox(verts):
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]
    return BoundingBox(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)) 
    

##############################################################################
# loadOBJ to list of verts and normals, normals not used, took from http://www.nandnor.net/?p=86
##############################################################################    
def loadOBJ(filename):  
    numVerts = 0  
    verts = []  
    norms = []  
    vertsOut = []  
    normsOut = []  
    for line in open(filename, "r"):  
        vals = line.split()  
        #print vals
        if vals[0] == "v":  
            #print vals
            v = map(float, vals[1:4])  
            verts.append(v)  
            #print v
        if vals[0] == "vn":  
            n = map(float, vals[1:4])  
            norms.append(n)  
            
        if vals[0] == "f":  
            for f in vals[1:]:  
                w = f.split("/")  
                # OBJ Files are 1-indexed so we must subtract 1 below  
                vertsOut.append(list(verts[int(w[0])-1]))  
                #normsOut.append(list(norms[int(w[2])-1]))  
                # no triangles?? 
                numVerts += 1  
    return vertsOut #, normsOut      

##############################################################################
# Get intersections between surface/mesh and line                            #
##############################################################################
def getIntersections(surfaceOBJ,pSource,pTarget):
    mesh = loadOBJforVTK(surfaceOBJ) # "SQUARE.obj"
    obbTree = vtk.vtkOBBTree()
    obbTree.SetDataSet(mesh)
    obbTree.BuildLocator()
    pointsVTKintersection = vtk.vtkPoints()
    obbTree.IntersectWithLine(pSource, pTarget, pointsVTKintersection, None) #!?   eerst code = 
    pointsVTKIntersectionData = pointsVTKintersection.GetData()
    noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
    pointsIntersection = []
    for idx in range(noPointsVTKIntersection):
        _tup = pointsVTKIntersectionData.GetTuple3(idx)
        pointsIntersection.append(_tup)
    return pointsIntersection

#print getIntersections("SQUARE.obj",[-50.0, 15.0, 15.0],[50.0, 15.0, 15.0])
#print getIntersections("SQUARE.obj",[50.0, 15.0, 15.0],[150.0, 15.0, 15.0])

##############################################################################
# Perform parity count on list of voxelpoints and intersections along scan line, return boolean list for scan line (length = dimension)
##############################################################################
def parityCount(intersectionsList):
    parityCountList = []
    for intersections in intersectionsList:
        if len(intersections)%2 != 0:
            # uneven --> inside
            parityCountList.append(True)
        elif len(intersections)%2 == 0:
            # even --> outside
            parityCountList.append(False)
    return parityCountList
    

    
def NParray2VTK(npmodel,dims,scale,vtkfilename):
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
    gridToVTK(vtkfilename, x, y, z, cellData = {vtkfilename : npmodel.astype(int)})
  
o = 0.0
a = math.sqrt(1.0/1.0)
b = math.sqrt(1.0/2.0)
c = math.sqrt(1.0/3.0)
vectorDict = { 
1: [ a, o, o],
2: [-a, o, o],
3: [ o, a, o],
4: [ o,-a, o],
5: [ o, o, a],
6: [ o, o,-a]
} 
"""
7: [ b, b, o],
8: [ b,-b, o],
9: [ b, o, b],
10:[ b, o,-b],
11:[-b, b, o],
12:[-b,-b, o],
13:[-b, o, b],
14:[-b, o,-b],
15:[ o, b, b],
16:[ o, b,-b], 
17:[ o,-b, b],
18:[ o,-b,-b],
19:[ c, c, c],
20:[ c, c,-c],
21:[ c,-c, c],
22:[ c,-c,-c],
23:[-c, c, c],
24:[-c,-c, c],
25:[-c, c,-c],
26:[-c,-c,-c]
}"""

    
##############################################################################
# get 26 rays shooting from voxel center shooting outside                    #
##############################################################################
def getRays(voxel):
    rayList = []
    vectorScale = 100
    for vector in vectorDict:
        # scale vector
        scaledVec = ([vec * vectorScale for vec in vectorDict[vector]])
        # move vector 
        #print "***************TEST*****************"
        #print [scaledVec[i] for i in range(len(scaledVec))]
        #print voxel
        #print [scaledVec[i]+voxel[i] for i in range(len(scaledVec))]
        ray = [scaledVec[ii]+voxel[ii] for ii in range(len(scaledVec))]
        rayList.append(ray)
    #print rayList
    return rayList 
    
    
def getVoxelPosition(voxel,dims,scale,translate):
        #def getvoxelpos(model,scale,dims,translate,i,j,k): #centroid!
        I,J,K = voxel[0],voxel[1],voxel[2]
        X = ((scale/dims) * (I+ 0.5)) + translate[0]
        Y = ((scale/dims) * (J+ 0.5)) + translate[1]  
        Z = ((scale/dims) * (K+ 0.5)) + translate[2]   # klopt dit, centroid vs vertice? + 0.5 of +0.0?
        return([X,Y,Z])
    
##############################################################################
# Main function                                                              #
##############################################################################
def voxelizeDir6NoAtt(objfile,dims):
    # GET OBJ FILE VERTLIST 
    vertsOut = loadOBJ(objfile)
    bbox = verts_to_bbox(vertsOut)
    print "BOUNDING BOX = "
    print bbox.full
    dX,dY,dZ = bbox.maxX-bbox.minX, bbox.maxY-bbox.minY, bbox.maxZ-bbox.minZ
    # minX minY, minZ are translation values? 
    translation = [bbox.minX,bbox.minY,bbox.minZ]
    dList = [dX, dY, dZ]
    print "DLIST = "
    print dList
    scale = max(dList)
    print "SCALE = "
    print scale
    cube_bbox = BoundingBox(bbox.minX, bbox.minX+scale, bbox.minY, bbox.minY+scale,bbox.minZ, bbox.minZ+scale)  
    voxelsize = scale/dims
    # KLOPT TRANSLATE? 
    #print "translate? = %s,%s,%s" % (bbox.minX, bbox.minY, bbox.minZ)
    translate = [bbox.minX, bbox.minY, bbox.minZ]
    print translate 
    #emptyArray = np.zeros((dims,dims,dims)) 
    
    arrayList = []
    for count in range(6):
        arrayList.append(np.zeros((dims,dims,dims)))
    #arrayList =  [np.zeros((dims,dims,dims))]*26 # FOUT!! 
    """arrayList[0][5,5,5] = 999
    print arrayList[0][5,5,5]
    print arrayList[1][5,5,5]"""
    
    #print arrayList
    # loop through emptyArray 
    for k in range(0,dims):
        print k
        for j in range(0,dims):
            for i in range(0,dims): 
                #print "voxel = %s,%s,%s" % (i, j,k) 
                voxel = [i,j,k]
                # get all rays
                
                # get intersections per rayList 
                rayIntersectionList = []
                #pSource = voxel position! 
                #print getVoxelPosition(voxel,dims,scale,translate)
                pSource = getVoxelPosition(voxel,dims,scale,translate)
                rayList = getRays(pSource)
                #print pSource
                for pTarget in rayList:
                    intersections = getIntersections(objfile,pSource,pTarget)
                    rayIntersectionList.append(intersections)
                parityCountList = parityCount(rayIntersectionList)
                #print parityCountList
                for index in range(0,len(arrayList)):
                    #print "TEST!!!!!!!!!!!!"
                    #print index
                    #print type(arrayList[index])
                    #print arrayList[index][i,j,k] 
                    arrayList[index][i,j,k] = parityCountList[index] 
                    #print arrayList[index][i,j,k] # ?? 
                
    #fullArray = np.zeros((dims,dims,dims)) 
    # add all numpy arrays
    #array0 = 
    fullArray = arrayList[0] + arrayList[1] + arrayList[2] + arrayList[3] + arrayList[4] + arrayList[5] #+ arrayList[6] + arrayList[7] + arrayList[8] + arrayList[9] + arrayList[10] + arrayList[11] + arrayList[12]+ arrayList[13] + arrayList[14] + arrayList[15] + arrayList[16] + arrayList[17] + arrayList[18] + arrayList[19] + arrayList[20] + arrayList[21] + arrayList[22] + arrayList[23] + arrayList[24]+ arrayList[25]
    print 40 * "*"
    print "main"
    print scale
    print dims
    print scale/dims
    
    threshold = 4
    # filter on threshold, array becomes boolean
    fullArray[fullArray<threshold] = 0 # order of these is import, is this the best way?     
    fullArray[fullArray>=threshold] = 1
    #print 40 * "*"
    
    print getVoxelPosition([0,0,0],dims,scale,translate)
    #print getVoxelPosition([31,31,31],dims,scale,translate)
    
    
    vtkfilename = objfile.replace(".obj","_6dir64dims_slowclean")
    NParray2VTK(fullArray,dims,scale,vtkfilename)        
    return fullArray,dims,scale,voxelsize,translation
    
#voxelizeDir26NoAtt("5439_rot.obj",128)








