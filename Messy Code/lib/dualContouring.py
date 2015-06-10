# -*- coding: utf-8 -*-
"""
Created on Thu Apr 09 12:36:57 2015

@author: Damien
"""
import numpy as np
import vtk 

dirs = [ [1,0,0], [0,1,0], [0,0,1] ] 

def splitOBJ(OBJfile):
    normalDict = {}
    normalTriList = []
    normal_index = 0
    # READ OBJ FILE 
    OBJ = open(OBJfile, 'r')
    vertlist = []
    trilist = []
    for line in OBJ:
        if line[0] == 'v':
            vsplit = line.split(" ")
            x = float(vsplit[1]); y = float(vsplit[2]); z = float(vsplit[3].rstrip('\n'))
            vertlist.append((x,y,z))
        if line[0] == 'f':
            fsplit = line.split(" ")
            v1 = int(fsplit[1]); v2 = int(fsplit[2]); v3 = int(fsplit[3])
            trilist.append((v1,v2,v3))
    # CHECK TRIANGLE SURFACE NORMALS 
    OBJ.close()
    for tri in trilist:
        n1,n2,n3 = np.array(vertlist[tri[0]-1]),np.array(vertlist[tri[1]-1]),np.array(vertlist[tri[2]-1])
        realtri = [n1,n2,n3]
        # GET NORMALIZED NORMAL VECTOR 
        trivectors = np.subtract(realtri[1:],realtri[:-1])
        trinorm = np.cross(trivectors[0],trivectors[1])+0.0
        length = np.linalg.norm(trinorm)
        normalizedsurfnorm = np.around(trinorm / length, decimals=2)
        # PLACE TRIANGLES 
        indice = tuple(normalizedsurfnorm)
        if not indice in normalDict:
            print indice
            normalDict[indice] = normal_index
            normal_index += 1
            normalTriList.append([tri])
        elif indice in normalDict:
            normalTriList[normalDict[indice]].append(tri)
            
    number_of_normals = len(normalDict)
    print "number of normals = %s" % number_of_normals
    # WRITE OBJ PER NORMAL  
    for n_index in range(len(normalTriList)):
        temp_trilist = normalTriList[n_index]
        temp_name = 'temp_%s.obj' % str(n_index)
        writeOBJ(temp_name,vertlist,temp_trilist)
    
    # MAKE SPLIT OBJ LIST 
    OBJlist = []
    for norm,index in normalDict.iteritems():
        #print norm,index,'temp_%s.obj' % str(index)
        OBJlist.append([norm,index,('temp_%s.obj' % str(index))])
    # norm as string or list in OBJlist?      
    return OBJlist


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
    
def getIntersections(surfaceOBJ,pSource,pTarget):
    mesh = loadOBJforVTK(surfaceOBJ) 
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

class Stick:
    def __init__(self,start,end,dims,scale,translate,objlist):
        self.Is, self.Js, self.Ks = start
        self.Ie, self.Je, self.Ke = end
        self.scale = scale
        self.dims = dims
        self.translate = translate
        self.objs = objlist # objnames + normal? 
        
        self.intersection = []
        self.normal = []
            
    def getRay(self):
        # USE GET POSITION FUNCTION 
        self.Xs = self.scale * ((self.Is+.5)/self.dims) + self.translate[0]
        self.Ys = self.scale * ((self.Js+.5)/self.dims) + self.translate[1]  
        self.Zs = self.scale * ((self.Ks+.5)/self.dims) + self.translate[2]   # klopt dit, centroid vs vertice?
        self.Xe = self.scale * ((self.Ie+.5)/self.dims) + self.translate[0]
        self.Ye = self.scale * ((self.Je+.5)/self.dims) + self.translate[1]  
        self.Ze = self.scale * ((self.Ke+.5)/self.dims) + self.translate[2]
        return [[self.Xs,self.Ys,self.Zs],[self.Xe,self.Ye,self.Ze]]
    
    def getHermite(self):
        print "***************************"
        for obj in self.objs: 
            
            #print obj[2]
            #print self.getRay()
            check = getIntersections(obj[2],self.getRay()[0],self.getRay()[1])
            if len(check) > 0:
                print "INTERSECTION"
                print check, obj[0]
                # get point
                # get nv 
                return [check, obj[0]]
                
                
def getPosition(i,j,k,dims,scale,translate):
    x = scale * ((i+.5)/dims) + translate[0]
    y = scale * ((j+.5)/dims) + translate[1]  
    z = scale * ((k+.5)/dims) + translate[2]   
    return x,y,z
    
def getCubeEdges(cubeCentroid):
    i,j,k = cubeCentroid
    e1 =  str( [int(item) for item in  [i -0.5, j -0.5, k -0.5, i +0.5, j -0.5, k -0.5 ] ] ) 
    e2 =  str( [int(item) for item in  [i -0.5, j -0.5, k -0.5, i -0.5, j +0.5, k -0.5 ] ] )
    e3 =  str( [int(item) for item in  [i -0.5, j -0.5, k -0.5, i -0.5, j -0.5, k +0.5 ] ] )
    e4 =  str( [int(item) for item in  [i +0.5, j -0.5, k -0.5, i +0.5, j +0.5, k -0.5 ] ] )    
    e5 =  str( [int(item) for item in  [i +0.5, j -0.5, k -0.5, i +0.5, j -0.5, k +0.5 ] ] )  
    e6 =  str( [int(item) for item in  [i -0.5, j +0.5, k -0.5, i +0.5, j +0.5, k -0.5 ] ] )
    e7 =  str( [int(item) for item in  [i -0.5, j +0.5, k -0.5, i -0.5, j +0.5, k +0.5 ] ] )
    e8 =  str( [int(item) for item in  [i -0.5, j -0.5, k +0.5, i +0.5, j -0.5, k +0.5 ] ] )
    e9 =  str( [int(item) for item in  [i -0.5, j -0.5, k +0.5, i -0.5, j +0.5, k +0.5 ] ] )
    e10 = str( [int(item) for item in  [i +0.5, j -0.5, k +0.5, i +0.5, j +0.5, k +0.5 ] ] )
    e11 = str( [int(item) for item in  [i -0.5, j +0.5, k +0.5, i +0.5, j +0.5, k +0.5 ] ] )
    e12 = str( [int(item) for item in  [i +0.5, j +0.5, k -0.5, i +0.5, j +0.5, k +0.5 ] ] )
    return e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12     
            
def createStick(start,end,dims,scale,translate,objlist):
    stick = Stick(start,end,dims,scale,translate,objlist)
    #print stick.getRay()
    #stick.getHermite()
    return stick

def dualContouring(objfile,array,dims,scale,translate):
    # SPLIT OBJ 
    split_obj = splitOBJ(objfile)
    print split_obj
    # GET STICKS 
    stickDict = {} 
    #test = 0
    for k in range(0,dims-1):
        for j in range(0,dims-1):
            for i in range(0,dims-1):
                # use cardinal directions 
                if array[i,j,k] != array[i+1,j,k]:
                    indice = str([i,j,k,i+1,j,k])
                    # get intersections + normal vector
                    stick = createStick([i,j,k],[i+1,j,k],dims,scale,translate,split_obj)
                    intersection, normal = stick.getHermite()
                    # add to dict
                    #test += 1
                    stickDict[indice] = intersection, normal 
                    
                if array[i,j,k] != array[i,j+1,k]:
                    indice = str([i,j,k,i,j+1,k])
                    # get intersections + normal vector
                    stick = createStick([i,j,k],[i,j+1,k],dims,scale,translate,split_obj)
                    intersection, normal = stick.getHermite()
                    # add to dict
                    stickDict[indice] = intersection, normal
                    
                    
                if array[i,j,k] != array[i,j,k+1]:
                    indice = str([i,j,k,i,j,k+1])
                    # get intersections + normal vector
                    stick = createStick([i,j,k],[i,j,k+1],dims,scale,translate,split_obj)
                    intersection, normal = stick.getHermite()
                    # add to dict
                    stickDict[indice] = intersection, normal
                    
                    
    print "STICK DICT"                 
    # get cubes for sticks 
    cubeDict = {}
    for stick,hermite in stickDict.iteritems():
        # get stick start & end from string in dict 
        #print stick
        f_stick = stick.replace("[", "")
        f_stick = f_stick.replace("]", "")
        f_stick = f_stick.split(",")
        start = [float(val) for val in f_stick[:3] ]
        end = [float(val) for val in f_stick[3:] ] 
        # get the 4 cubes that are surrounding the dict 
        direction = list(np.subtract(end,start)).index(1) 
        # SLECHTE CODE
        if direction == 0: neighbours = [[0.5,0.5,-0.5],[0.5,-0.5,-0.5],[0.5,0.5,0.5],[0.5,-0.5,0.5]]    
        elif direction == 1: neighbours = [[0.5,0.5,-0.5],[-0.5,0.5,-0.5],[0.5,0.5,0.5],[-0.5,0.5,0.5]]
        elif direction == 2: neighbours = [[0.5,-0.5,0.5],[-0.5,-0.5,0.5],[0.5,0.5,0.5],[-0.5,0.5,0.5]]
        #print neighbours
        neighbours = [list(np.add(start,neighbour)) for neighbour in neighbours]    
        stickDict[stick] = intersection, normal, neighbours
        # add neighbours to stickDict 
        
        #print neighbours
        for cube in neighbours:
            indice = tuple(cube)
            if not indice in cubeDict:
                cubeDict[indice] = 0
            
    # for cube get all edges, check if stick exists         
    for cube in cubeDict.keys():
        print "**** NEW CUBE ****"
        cubeEdges =  getCubeEdges(list(cube))
        hermiteData = []
        for edge in cubeEdges:
            if edge in stickDict:
                hermiteData.append(stickDict[edge])
                
        print cube
        #print hermiteData
        p = [intersection[0] for intersection,normal in hermiteData]
        
        
        # if less than 3 intersections
        if len(p) < 3:
            # assign cube center 
            print "less than 3 intersection found"
            c = getPosition(cube[0],cube[1],cube[2],dims,scale,translate)
            cubeDict[cube] = c
        else:     
            
            # calculate masspoint
            m = np.mean([intersection for intersection,normal in hermiteData],axis=0)[0]
            # calculate number of normals
            A = [normal for intersection,normal in hermiteData]
            number_of_normals = len(set(A))
            print p
            print A
            #print "number_of_normals = " + str(number_of_normals)     
            # if all normals equal                                  alternative: if n.count(n[0])== len(n):
            if number_of_normals == 1:
                #print "1 normal found"
                # assign mass point
                cubeDict[cube] = m
            else:
                B = [np.dot(p,n) for p,n in hermiteData ]
                if number_of_normals == 2:
                    #print "2 normals found"
                    v, residue, rank, s = np.linalg.lstsq(A, B)
                    print v
                    print A
                    
                    # decide point along line 
                    # IF NO 0'S IN NORMALS, IS THERE ALWAYS AN INTERSECTION? TWO PLANES ARE STILL ALONG A LINE
                    # TEEESSTTTT!! 
                    nparray = np.array([list(tup) for tup in A]) # [np.array(tup) for tup in A]
                    if nparray.sum(axis=0)[0] == 0:
                        v[0] = m[0]
                        
                    elif nparray.sum(axis=0)[1] == 0:
                        v[1] = m[1]
                        
                    elif nparray.sum(axis=0)[2] == 0:
                        v[2] = m[2]
                        
                elif number_of_normals > 2:
                    #print "3 normals found"
                    v, residue, rank, s = np.linalg.lstsq(A, B)
                    #print v
                    # always correct? / solvable? 
                    # add try? 
                    cubeDict[cube] = v
                    
    # for key,value stick in stickDict:
    # neighbours = value[3]  ?? test
    # for neighbour in neighbours cubeDict[neighbour]
    # write tri neigh1 neigh2 neigh3 & neigh 1 neigh 3 neigh 4 
    # add vertices, vertid += 1 etc 
    # make triid 
    # get neighbours 
        
        # 3 - select case  (not enoguh intersections / all nv's same / two nv's third direction manual / three nv's intersection found)
        # 4 - write dualPoint to cubeDict!  skip 2 )
        
    """    
    #Vertices of cube
    cube_verts = [ np.array([x, y, z])
    for x in range(2)
    for y in range(2)
    for z in range(2) ]

    #Edges of cube
    cube_edges = [ 
    [ k for (k,v) in enumerate(cube_verts) if v[i] == a and v[j] == b ]
    for a in range(2)
    for b in range(2)
    for i in range(3) 
    for j in range(3) if i != j ]
    """
    # get dual for cube                 
                    
    #print test
    print "number of sticks = %s " % len(stickDict)
    print "number of cubes = %s "% len(cubeDict)   


def writeOBJ(OBJfile,vertlist,trilist):
    OBJ = open(OBJfile, 'w')
    for vert in vertlist:
        OBJ.write("v %s %s %s \n" % (vert[0],vert[1],vert[2]) )
    for tri in trilist:   
        OBJ.write("f %s %s %s \n" % (tri[0],tri[1],tri[2]) )
    OBJ.close()
    
def getRealPos(dims,scale,translate,i,j,k):
    x = scale * ((i+.5)/dims[0]) + translate[0]
    y = scale * ((j+.5)/dims[1]) + translate[1]  
    z = scale * ((k+.5)/dims[2]) + translate[2]    
    return x,y,z
             

    
     
     
     
     
     
     
     
     
     
     
     
     
    