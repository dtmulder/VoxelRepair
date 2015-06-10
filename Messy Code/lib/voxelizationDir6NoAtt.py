# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:08:46 2015

@author: Damien
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 11:47:47 2015

@author: Damien
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 19:32:26 2015

@author: Damien
"""
import vtk 
import numpy as np
from evtk.hl import gridToVTK


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
# Point class                                                                #
##############################################################################
class Point(object):
    def __init__(self, x, y):
        '''Defines x and y variables'''
        self.x = x
        self.y = y

##############################################################################
# Line class                                                                 #
##############################################################################        
class Line(object):
    def __init__(self,startPoint,endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint
        
    def pointOnLeft(self,point):
        position = ((self.endPoint.x - self.startPoint.x)*(point.y-self.startPoint.y)) - ((self.endPoint.y-self.startPoint.y)*(point.x-self.startPoint.x))
        if position > 0.0:
            return True
        else:
            return False   
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
def parityCount(voxels,intersections):
    boolScanLineAsc, boolScanLineDesc = [], []
    for voxel in voxels:
        smaller = [intersection for intersection in intersections if intersection < voxel]
        if len(smaller)%2 != 0:  # uneven intersection on the left side
            boolScanLineAsc.append(True)
        else:
            boolScanLineAsc.append(False)
        larger = [intersection for intersection in intersections if intersection > voxel]
        if len(larger)%2 != 0:  # uneven intersection on the left side
            boolScanLineDesc.append(True)
        else:
            boolScanLineDesc.append(False)
    return boolScanLineAsc, boolScanLineDesc
    
#print parityCount([3.2,5.1],[1.0,2.1,4.9,6.0])

##############################################################################
# Grid to VTK function                                                       #
##############################################################################

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

##############################################################################
# Single scan direction for voxelization                                     #
##############################################################################
def ScanInDirection(objfile,bbox,dims,voxelsize, scale, direction = "x"):
    array3DAsc = np.zeros((dims, dims, dims))
    array3DDesc = np.zeros((dims, dims, dims))
    print "direction = " + str(direction)
    if direction == "x": 
        start0 = bbox.minX + (voxelsize/2.0)
        start1 = bbox.minY + (voxelsize/2.0)
        start2 = bbox.minZ + (voxelsize/2.0)
        index= 0
    elif direction == "y": 
        start1 = bbox.minX + (voxelsize/2.0)           
        start0 = bbox.minY + (voxelsize/2.0)
        start2 = bbox.minZ + (voxelsize/2.0)
        index= 1
    elif direction == "z": 
        start1 = bbox.minX + (voxelsize/2.0)
        start2 = bbox.minY + (voxelsize/2.0)
        start0 = bbox.minZ + (voxelsize/2.0)
        index= 2
    s0 = start0 - voxelsize
    e0 = start0 + scale  
    for k in range(0,dims):
        s2 = start2 + k*voxelsize
        for j in range(0,dims):
            s1 = start1+ j*voxelsize
            if direction == "x":
                pSource = [s0,s1,s2]
                pTarget = [e0,s1,s2]
            elif direction == "y":
                pSource = [s1,s0,s2]
                pTarget = [s1,e0,s2]
            elif direction == "z": 
                pSource = [s1,s2,s0]
                pTarget = [s1,s2,e0]
            voxList = []
            for i in range(0,dims): # dims +1? , removed, i+1 now
                vox = ((i)*voxelsize) + start0
                voxList.append(vox)
            intersections = getIntersections(objfile,pSource,pTarget)
            if len(intersections) == 0:
                boolScanLineAsc = [0] * dims
                boolScanLineDesc = [0] * dims
            elif len(intersections) != 0:
                Intersections = [intersection[index] for intersection in intersections]
                boolScanLineAsc = parityCount(voxList,Intersections)[0] # parityCount should return two arrays, start and end intersect
                boolScanLineDesc = parityCount(voxList,Intersections)[1]
                #  boolScanLineAsc
            if direction == "x":
                array3DAsc[:,j,k] = boolScanLineAsc
                array3DDesc[:,j,k] = boolScanLineDesc
            elif direction == "y":
                array3DAsc[j,:,k]= boolScanLineAsc
                array3DDesc[j,:,k]= boolScanLineDesc
            elif direction == "z":
                array3DAsc[j,k,:]= boolScanLineAsc
                array3DDesc[j,k,:]= boolScanLineDesc
            #array3D[:,j,k]= boolScanLine  
    return array3DAsc, array3DDesc




##############################################################################
# Main function                                                              #
##############################################################################
def voxelizeDir6NoAtt(objfile,dims):
    #print "main function"
    # GET OBJ FILE VERTLIST 
    vertsOut = loadOBJ(objfile)
    #vertsOut= a
    #print vertsOut
    bbox = verts_to_bbox(vertsOut)
    #print bbox.full
    dX,dY,dZ = bbox.maxX-bbox.minX, bbox.maxY-bbox.minY, bbox.maxZ-bbox.minZ
    # minX minY, minZ are translation values? 
    translation = [bbox.minX,bbox.minY,bbox.minZ]
    dList = [dX, dY, dZ]
    scale = max(dList)
    #print dMax
    
    cube_bbox = BoundingBox(bbox.minX, bbox.minX+scale, bbox.minY, bbox.minY+scale,bbox.minZ, bbox.minZ+scale)     
    #print cube_bbox.full
    # CREATE CUBIC BBOX!  
    #print bbox 
    # STILL CREATE CUBIC BBOX, TEST WITH NEW OBJ FILE  
    # cubebbox has same minx,miny,minz,   get dx,dy,dz  largest is used in all directions 
    
    #scaleX,scaleY,scaleZ = bbox.maxX-bbox.minX, bbox.maxY-bbox.minY, bbox.maxZ-bbox.minZ
    """currently square, what if it is not square?  why should it be?
    either input = voxelsize, or dimensions in a cube """
    
    voxelsize = scale/dims    
    #print "voxelsize = " + str(voxelsize)
    # get translation values  
    

    
    
    ##########################################################################
    
    
    # X DIRECTION
    xDirection = ScanInDirection(objfile,bbox,dims,voxelsize,scale, direction = "x")
    xAsc = xDirection[0]
    xDesc = xDirection[1]
    
    
    #vtkfilename = objfile.replace(".obj","Xdir")
    #NParray2VTK(xAsc,dims,scale,"TESTxAsc")
    #NParray2VTK(xDesc,dims,scale,"TESTxDesc")
    ##########################################################################
    # Y DIRECTION
    yDirection = ScanInDirection(objfile,bbox,dims,voxelsize,scale, direction = "y")
    yAsc = yDirection[0]
    yDesc = yDirection[1]
    #vtkfilename = objfile.replace(".obj","Ydir")
    #NParray2VTK(Xarray3D ,dims,scale,vtkfilename)
    #NParray2VTK(yAsc,dims,scale,"TESTyAsc")
    #NParray2VTK(yDesc,dims,scale,"TESTyDesc")
    ##########################################################################
    # Z DIRECTION
    
    zDirection = ScanInDirection(objfile,bbox,dims,voxelsize,scale, direction = "z")
    zAsc = zDirection[0]
    zDesc = zDirection[1]
    
    #vtkfilename = objfile.replace(".obj","Zdir")
    #NParray2VTK(Zarray3D ,dims,scale,vtkfilename)
    #NParray2VTK(zAsc,dims,scale,"TESTzAsc")
    #NParray2VTK(zDesc,dims,scale,"TESTzDesc")
    ##########################################################################
    # SUM OF X Y AND Z DIR ARRAY 
    """
    vtkname = objfile.replace(".obj","TEST_xAsc")
    NParray2VTK(xAsc,dims,scale,vtkname)
    vtkname = objfile.replace(".obj","TEST_xDesc")
    NParray2VTK(xDesc,dims,scale,vtkname)
    vtkname = objfile.replace(".obj","TEST_yAsc")
    NParray2VTK(yAsc,dims,scale,vtkname)
    vtkname = objfile.replace(".obj","TEST_yDesc")
    NParray2VTK(yDesc,dims,scale,vtkname)
    
    vtkname = objfile.replace(".obj","TEST_zAsc")
    NParray2VTK(zAsc,dims,scale,vtkname)
    
    vtkname = objfile.replace(".obj","TEST_zDesc")
    NParray2VTK(zDesc,dims,scale,vtkname)
    
    
    
    
    vtkname = objfile.replace(".obj","TESTfull6")
     
    #vtkname = 
    NParray2VTK(fullArray,dims,scale,vtkname)
    """
    fullArray = xAsc + xDesc + yAsc + yDesc + zAsc + zDesc
    threshold = 4
    # filter on threshold, array becomes boolean
    fullArray[fullArray<threshold] = 0 # order of these is import, is this the best way?     
    fullArray[fullArray>=threshold] = 1
    vtkname = objfile.replace(".obj","_4")
    NParray2VTK(fullArray,dims,scale,vtkname)
    #fullArray = xAsc + xDesc + yAsc + yDesc + zAsc + zDesc 
    # translation should be added 
    return fullArray,dims,scale,voxelsize,translation

    

