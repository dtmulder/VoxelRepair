# -*- coding: utf-8 -*-
"""
Created on Thu Apr 09 12:36:57 2015

@author: Damien
"""
import numpy as np
import vtk 
import os 

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
        normalizedsurfnorm = np.around(trinorm / length, decimals=1)
        #normalizedsurfnorm = trinorm / length
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
        #print "***************************"
        for obj in self.objs: 
            
            #print obj[2]
            #print self.getRay()
            check = getIntersections(obj[2],self.getRay()[0],self.getRay()[1])
            #print check
            if len(check) > 0:
                #print "INTERSECTION"
                #print check #, obj[0]
                # get point
                # get nv 
                #print "obj[0] is = "
                #print obj[0]
                #print type(obj[0])
                return [check, obj[0]]
        print "NO INTERSECTION FOUND"
        #print 
        #print "NO INTERSECTION FOUND2"
        #print "NO INTERSECTION FOUND3"
        return [[check],"empty"] # test! 
                
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
    #print split_obj
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
                    if normal == 'empty':
                        print ([i,j,k],[i+1,j,k])
                        stick_behind = createStick([i-1,j,k],[i,j,k],dims,scale,translate,split_obj)
                        stick_infront = createStick([i+1,j,k],[i+2,j,k],dims,scale,translate,split_obj)
                        # CHECK PROBING
                    # add to dict
                    #test += 1
                    stickDict[indice] = intersection, normal 
                    
                if array[i,j,k] != array[i,j+1,k]:
                    indice = str([i,j,k,i,j+1,k])
                    #print indice
                    # get intersections + normal vector
                    stick = createStick([i,j,k],[i,j+1,k],dims,scale,translate,split_obj)
                    intersection, normal = stick.getHermite()
                    if normal == 'empty':
                        print ([i,j,k],[i,j+1,k])
                    # add to dict
                    stickDict[indice] = intersection, normal
                    
                    
                if array[i,j,k] != array[i,j,k+1]:
                    indice = str([i,j,k,i,j,k+1])
                    # get intersections + normal vector
                    stick = createStick([i,j,k],[i,j,k+1],dims,scale,translate,split_obj)
                    intersection, normal = stick.getHermite()                    
                    if normal == 'empty':
                        print ([i,j,k],[i,j,k+1])
                    # add to dict
                    stickDict[indice] = intersection, normal
                    
    """ 
    # delete temp obj files
    print len(split_obj)
    for n in range(len(split_obj)):
        temp_name = 'temp_%s.obj' % str(n)
        os.remove(temp_name)               
    """    
           
    # get cubes for sticks 
    cubeDict = {}
    for stick,hermite in stickDict.iteritems():
        # get stick start & end from string in dict 
        f_stick = stick.replace("[", "")
        f_stick = f_stick.replace("]", "")
        f_stick = f_stick.split(",")
        a = [int(val) for val in f_stick[:3] ]
        b = [int(val) for val in f_stick[3:] ] 
        # all sticks pointed from inside to outside
        a_val = array[a[0],a[1],a[2]]
        b_val = array[b[0],b[1],b[2]]
        # ugly code, but not that easy? 
        if a_val-b_val == 1:
            start = [float(val) for val in f_stick[:3] ]
            end = [float(val) for val in f_stick[3:] ] 
            direction = list(np.subtract(end,start)).index(1) 
            if direction == 0: neighbours = [[0.5,0.5,-0.5],[0.5,0.5,0.5],[0.5,-0.5,0.5],[0.5,-0.5,-0.5]]    
            elif direction == 1: neighbours = [[0.5,0.5,-0.5],[-0.5,0.5,-0.5],[-0.5,0.5,0.5],[0.5,0.5,0.5]]
            elif direction == 2: neighbours = [[0.5,-0.5,0.5],[0.5,0.5,0.5],[-0.5,0.5,0.5],[-0.5,-0.5,0.5]]
                
        elif a_val-b_val == -1:
            start = [float(val) for val in f_stick[3:] ] 
            end = [float(val) for val in f_stick[:3] ]
            direction = list(np.subtract(end,start)).index(-1) 
            if direction == 0: neighbours = [[-0.5,-0.5,-0.5],[-0.5,-0.5,0.5],[-0.5,0.5,0.5],[-0.5,0.5,-0.5]]    
            elif direction == 1: neighbours = [[-0.5,-0.5,-0.5],[0.5,-0.5,-0.5],[0.5,-0.5,0.5],[-0.5,-0.5,0.5]]
            elif direction == 2: neighbours = [[-0.5,0.5,-0.5],[0.5,0.5,-0.5],[0.5,-0.5,-0.5],[-0.5,-0.5,-0.5]]
        
       
        neighbours = [list(np.add(start,neighbour)) for neighbour in neighbours] 
        intersection,normal = stickDict[stick]
        # add neighbours to stickDict 
        stickDict[stick] = intersection, normal, neighbours
        # add cube indexes to cubeDict
        for cube in neighbours:
            indice = tuple(cube)
            if not indice in cubeDict:
                cubeDict[indice] = 0
                
    print "number of sticks = %s " % len(stickDict)
    print "number of cubes = %s "% len(cubeDict)
        
    # for cube get all edges, check if stick exists         
    for cube in cubeDict.keys():
        cubeEdges =  getCubeEdges(list(cube))
        hermiteData = []
        #exception = 0
        for edge in cubeEdges:
            
            if edge in stickDict:
                # if stick does not have intersection 
                #edge_check = [edge[1] for edge in stickDict]
                
                #print edge_check
                #if "empty" in edge_check:
                    #print "EXCEPTION"
                    #exception = 1
                    
                # if stick does have intersection    
                #else:
                hermiteData.append(stickDict[edge][0:2])
        
        #print hermiteData    
        empty_check = [n for p,n in hermiteData]
        p = [intersection[0] for intersection,normal in hermiteData]
        A = [normal for intersection,normal in hermiteData]
        number_of_normals = len(set(A))
        #print empty_check
        
        
        # ADJUST HERE
        # IF NO INTERSECTIONS FOUND AT ALL, APPEND C
        # IF SOME INTERSECTIONS FOUND BUT EMPTY IN EMPTY CHECK, APPEND M
        # IF NUMBER OF NORMALS == 1  APPEND M
        # ELSE   CALC QEF 
        if 'empty' in empty_check:
            #print empty_check
            #print "exception found, cube center assigned"
            c = getPosition(cube[0],cube[1],cube[2],dims,scale,translate)
            #print c
            cubeDict[cube] = c
        #else:
            # already rounded? otherwise np.round(array,decimals=5)
        
            #p = [intersection[0] for intersection,normal in hermiteData]
            # if less than 3 intersections
        elif len(p) < 3:
            # assign cube center 
            #print "less than 3 intersection found"
            c = getPosition(cube[0],cube[1],cube[2],dims,scale,translate)
            cubeDict[cube] = c
            # already rounded? otherwise np.round(array,decimals=5) """
        
        elif number_of_normals == 1:
            m = np.mean([intersection for intersection,normal in hermiteData],axis=0)[0]
            cubeDict[cube] = m
            # if more than 2 intersections
        else:     
            #print "intersection found"
            # calculate masspoint
            m = np.mean([intersection for intersection,normal in hermiteData],axis=0)[0]
            #print np.round(m,decimals=2)
            # calculate number of normals
            #A = [normal for intersection,normal in hermiteData]
             
            number_of_normals = len(set(A))
            B = [np.dot(np.subtract(p[0],m),n) for p,n in hermiteData ]
            v, residue, rank, s = np.linalg.lstsq(A, B)
            d = np.round(np.add(v,m) ,decimals=5)
            
            if d[0] > -240000 or d[0] < -260000 :
                #print d
                #print "WRONG POINT"
                #print d
                print hermiteData
                #print v
            #if d[0] + 250000 > 100000:
            #    print d
            #if d[0] - 250000 < -100000:
            #    print d
            cubeDict[cube] = d
    
    # write two triangles for every stick
    vertID = 1
    vertDict = {}
    vertList = []
    triList = []
    
    for a,b in stickDict.iteritems():
        # find stick neighbour duals
        neighbours = b[2]
        p0 = list(cubeDict[tuple(neighbours[0])])
        p1 = list(cubeDict[tuple(neighbours[1])])
        p2 = list(cubeDict[tuple(neighbours[2])])
        p3 = list(cubeDict[tuple(neighbours[3])])
        pointList = [p0,p1,p2,p3]
        
        # check dict for vert ID's 
        idList = []
        for point in pointList:
            if tuple(point) in vertDict:
                idList.append(vertDict[tuple(point)])
            
            else:
                vertDict[tuple(point)] = vertID
                vertList.append(point)
                idList.append(vertID)
                vertID += 1
        # get vert ID's and write triangles
        v0,v1,v2,v3 = idList
        tri1 = [v0,v1,v2]
        tri2 = [v0,v2,v3]   
        triList.append(tri1)
        triList.append(tri2)
    # write to OBJ
    output_filename = objfile.replace(".obj","_DualContouring_%s.obj" % (dims-2) )
    writeOBJ(output_filename,vertList,triList)     
    print split_obj

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
             

    
     
     
     
     
     
     
     
     
     
     
     
     
    