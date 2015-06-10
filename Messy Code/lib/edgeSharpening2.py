# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 17:24:25 2015

@author: Damien
"""
import numpy as np
from operator import itemgetter
import itertools


def writeOBJ(vertlist,trilist,filename):
    print "number of triangles: " + str(len(trilist))
    print "number of vertices: " + str(len(vertlist))
    OBJ = open(filename, "w")
    OBJ.write('# Created with OBJ writer test version DM\n')
    OBJ.write('# COORDINATE_SYSTEM:  OGC_DEF PROJCS["Netherlands, Amersfoort RD 2008 datum, New System",GEOGCS["Amersfoort",DATUM["Amersfoort",SPHEROID["Bessel, 1841",6377397.155,299.1528153513275,AUTHORITY["EPSG","7004"]],AUTHORITY["EPSG","6289"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4289"]],PROJECTION["Stereographic"],PARAMETER["latitude_of_origin",52.1561605555556],PARAMETER["central_meridian",5.38763888888889],PARAMETER["scale_factor",0.9999079],PARAMETER["false_easting",155000],PARAMETER["false_northing",463000],UNIT["METER",1],AUTHORITY["EPSG","28992"]]\n')
    OBJ.write('# Number of Geometry Coordinates  : ' + str(len(vertlist)) + '\n')
    OBJ.write('# Number of Texture  Coordinates  : 0\n')
    OBJ.write('# Number of Normal   Coordinates  : 0\n')
    # loop through vertices and write to obj    
    for vert in vertlist:
        OBJ.write("v " + str(vert[0]) + " " + str(vert[1]) + " " + str(vert[2]) + "\n")
    OBJ.write('# Number of Elements in set       : ' + str(len(trilist)) + '\n') 
    # loop through triangles and write to obj
    for tri in trilist:
        OBJ.write("f " + str(tri[0]) + " " + str(tri[1]) + " " + str(tri[2]) + "\n")
    OBJ.write('# Total Number of Elements in file: ' + str(len(trilist)) + '\n') 
    OBJ.write('# EOF')
    OBJ.close()


class Vertice:
    def __init__(self,x,y,z,vertID):# ,vertID
        self.X  = float(x)
        self.Y  = float(y)
        self.Z  = float(z)
        self.ID = int(vertID)
        self.string = "(%s , %s , %s)" % (self.X,self.Y,self.Z)
        self.neighbourNormals = []
        
    
    def getVerticePosition(self):
       #def getvoxelpos(model,scale,dims,translate,i,j,k): #centroid!
       """self.X = self.scale * ((self.I+.5)/self.dims) + self.translate[0]
       self.Y = self.scale * ((self.J+.5)/self.dims) + self.translate[1]  
       self.Z = self.scale * ((self.K+.5)/self.dims) + self.translate[2]   # klopt dit, centroid vs vertice? """
       return(self.X,self.Y,self.Z)
       
    def addNeighbourNormal(self,normalvec):
        self.neighbourNormals.append(normalvec)
        
##############################################################################
# triangle class                                                             #
##############################################################################
        
class Triangle: 
    def __init__(self,n1,n2,n3): # should node indexes be stored? 
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.position = [n1,n2,n3]
        #self.fullpos = (n1,n2,n3)
        self.neighbourNormals = [] 
        # [n1.neighbourNormals,n2.neighbourNormals,n3.neighbourNormals]
    #def addPosition(self,p1,p2,p3):
        #self.position = [p1,p2,p3]
    #def getNodeIndexes(self):
        #return (self.n1,self.n2,self.n3)
        #self.id = triID
        #triID += 1 # werkt dit?  # niet nodig?
    def getNormalizedNormalVec(self):
        """# create Vertice for each node
        Vert1 = Vertice(self.n1[0],self.n1[1],self.n1[2],self.model,self.dims,self.scale,self.translate)
        Vert2 = Vertice(self.n2[0],self.n2[1],self.n2[2],self.model,self.dims,self.scale,self.translate)
        Vert3 = Vertice(self.n3[0],self.n3[1],self.n3[2],self.model,self.dims,self.scale,self.translate)
        # get real pos for each Vertice, list as TriPos
        Vert1Pos = Vert1.getVerticePosition()
        Vert2Pos = Vert2.getVerticePosition()
        Vert3Pos = Vert3.getVerticePosition()"""
        TriPos = self.position
        # calc normalized normal vecor for Tri
        # get vectors Vert1Vert2 & Vert2Vert3
        TriVectors = np.subtract(TriPos[1:],TriPos[:-1])
        # get crossproduct of Vert1Vert2 & Vert2Vert3 (= surface normal)
        TriNorm = np.cross(TriVectors[0],TriVectors[1])+0.0
        # get length of surface normal
        length = np.linalg.norm(TriNorm)
        # divide each component of surface normal by length (= normalized surface normal)
        NormalizedNormalVec = np.around(TriNorm / length, decimals=5) # rounded, otherwise different values, equals not found
        # create string of tuple for segment dict        
        #SegmDict = str(tuple(NormalizedNormalVec))
        return NormalizedNormalVec.tolist()
        
##############################################################################
# get angle between vectors                                                  #
##############################################################################
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    #print 'unit_vector'
    #print vector
    #print type(vector)
    #npvector = np.array(vector)
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    #print v1, v2
    angle = np.arccos(np.dot(v1_u, v2_u))
    #print angle
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

def thinNVList(nvlist):
    NVset_thinned = sorted(nvlist, key=itemgetter(0,1,2))
    for i in range(len(NVset_thinned)-1,0,-1):
        vec1 = NVset_thinned[i]
        vec2 = NVset_thinned[i-1]
        if np.array_equal(vec1,vec2):
            del NVset_thinned[i]
        else:
            continue
    #print 'nvset thinned'
    #print NVset_thinned
    #a = [subset[0] for subset in NVset_thinned]
    #print a
    #return a
    #if len(NVset_thinned) > 0:
    return NVset_thinned #[0]
    #else: 
        #return []
    
def testlist2OBJ(testlist,filename):
    temp_vertlist = []
    temp_trilist = []
    vertID = 1
    for tri in testlist:
        index_tri = []
        #print tri.position
        for vert in tri.position:
            temp_vertlist.append(vert)
            index_tri.append(vertID)
            vertID+=1
        temp_trilist.append(index_tri)
    writeOBJ(temp_vertlist,temp_trilist,filename)    
    #print temp_vertlist,temp_trilist
    
    return
    
def checkOrtho(NVset):
    flatNVset = [NV for subset in NVset for NV in subset]   
    thinned_flatNVset = thinNVList(flatNVset)
    numberNVs = len(thinned_flatNVset)
    #print numberNVs
    #numberNVs = 3
    count = [i for i in range(numberNVs)]
    #print count
    indexes = list(itertools.combinations(count,2))
    for indexpair in indexes:
        #print list(indexpair)
        pair = [thinned_flatNVset[ids] for ids in indexpair]
        #print pair
        angle = angle_between(pair[0],pair[1])
        if not np.allclose(angle, 1.57079632679): 
            return False
        else:
            continue
    return True 
    # extend later?  remove non ortho? 
        
    
    
#print checkOrtho([[[0.0, 0.0, 1.0]], [[0.0, 1.0, 0.0]], [[1.0, 0.0, 0.0]]])


def distance(point1,point2):
    nppoint1 = np.array(point1)
    nppoint2 = np.array(point2)
    dist = np.linalg.norm(nppoint1-nppoint2)
    return dist


def testEquilateral(Tri): 
    dist1 = distance(Tri[0],Tri[1])
    dist2 = distance(Tri[1],Tri[2])
    dist3 = distance(Tri[2],Tri[0])
    if np.allclose(dist1,dist2) and np.allclose(dist2,dist3) and np.allclose(dist3,dist1):
        # get center
        ##print "*********** EQUILAT TRI***************"
        ##print "p1 = " + str(Tri[0])
        #print Tri[0][0], Tri[0][1],Tri[0][2]
        ##print "p2 = " + str(Tri[1])
        #print Tri[1][0], Tri[1][1],Tri[1][2]
        ##print "p3 = "+ str(Tri[2])
        center = [np.sum([Tri[0][0],Tri[1][0],Tri[2][0]])/3.0,np.sum([Tri[0][1],Tri[1][1],Tri[2][1]])/3.0, np.sum([Tri[0][2],Tri[1][2],Tri[2][2]])/3.0 ]
        ##print "p4 = " + str(center)
        return [True, center ]
    else:
        return [False ]

def testCornerConcaveConvex(Tri,NVset): # cornerTriTest       only run on single corner triangles? or extend? 
    dist1, dist2,dist3 = distance(Tri[0],Tri[1]),distance(Tri[1],Tri[2]),distance(Tri[2],Tri[0])
    stepsize = dist1/10.0 # must be much smaller than polygon
    NVset = [subset[0] for subset in NVset]
    movedTri = (np.array(Tri) + (np.array(NVset) * stepsize)).tolist()
    moved_dist1 = distance(movedTri[0],movedTri[1])
    moved_dist2 = distance(movedTri[1],movedTri[2])
    moved_dist3 = distance(movedTri[2],movedTri[0])
    boolList = [moved_dist1 >dist1,moved_dist2 > dist2,moved_dist3 > dist3]
    if sum(boolList) == 3: 
        return "CONVEX"
    elif sum(boolList) == 0: 
        return "CONCAVE"
    elif sum(boolList) == 2:    # for convex chamfer, change later 
        return "CONVEX"
    else:
        #print "ONVERWACHTE CASE????????????????"
        #print sum(boolList)
        
        return "CONVEX/CONCAVE"
    
def testChamferConcaveConvex(Tri,NVset):
    dist1, dist2,dist3 = distance(Tri[0],Tri[1]),distance(Tri[1],Tri[2]),distance(Tri[2],Tri[0])
    stepsize = dist1/10.0 # must be much smaller than polygon
    pass 
            
##############################################################################
# filter triangles based on NV collection                                    #
##############################################################################
def testAngles(triNV,NVset):
    #print "********** START testAngles ************"
    # GET UNIQUE NUMBER 
    flatNVset = [NV for subset in NVset for NV in subset]
    NVset_thinned = thinNVList(flatNVset)
    numberUnique = len(NVset_thinned)
    #print "numberUnique  = "+ str(numberUnique)
    # GET CORNER AND CHAMFER VECTORS 
    if numberUnique > 2:
        original_CornerNVs = [[],[],[]]
        original_ChamferNVs = [[],[],[]]
        for subset in range(3):
            for vec in NVset[subset]:
                if np.allclose([angle_between(triNV, vec)],[0.955316618125]): # assumption, correct for MC?
                    original_CornerNVs[subset].append(vec)
                elif np.allclose([angle_between(triNV, vec)],[0.785398163397]):
                    original_ChamferNVs[subset].append(vec)
        flat_original_CornerNVs = [NV for subset in original_CornerNVs for NV in subset]
        unique_CornerNVs = thinNVList(flat_original_CornerNVs)
        numberCornerNVs = len(unique_CornerNVs)
        flat_original_ChamferNVs = [NV for subset in original_ChamferNVs for NV in subset]
        unique_ChamferNVs = thinNVList(flat_original_ChamferNVs)       
        numberChamferNVs = len(unique_ChamferNVs)
        # for subset in original, thin the list?
        for i in range(3):
            #print i
            #print original_CornerNVs
            original_CornerNVs[i] = thinNVList(original_CornerNVs[i])
            #print original_CornerNVs
            original_ChamferNVs[i] = thinNVList(original_ChamferNVs[i])
            
            
        
        return numberUnique, numberCornerNVs, numberChamferNVs, original_CornerNVs, original_ChamferNVs
    else:
        return numberUnique, 0, 0, [], [] # niet netjes? 


def detectTriangles(vertlist,trilist,voxelsize):
    print "starting triangle detection"
    vertDict = {}
    vertID = 1
    triDict = {}
    triID = 1
    new_vertlist = []
    #print len(vertlist)
    # CREATE VER DICT
    # for tri in tri list,  get normal vec
    # for vert in tri, check in vertdict, if there: add normal vec, if not there, add it, vertid +1 add normal vec 
    for index in range(len(trilist)):
        tri = trilist[index]
        node1,node2,node3 = tri[0], tri[1], tri[2]
        updateTri = []
        TRI = Triangle(vertlist[node1-1],vertlist[node2-1],vertlist[node3-1])
        NNV = TRI.getNormalizedNormalVec()
        for node in tri:
            Node = vertlist[node-1]
            VERT = Vertice(Node[0],Node[1],Node[2],vertID)
            # if not in dict: attach NNV, add vert to dict
            if VERT.string not in vertDict:  
                #print "**********CHECK******"
                #print NNV
                VERT.addNeighbourNormal(NNV)
                vertDict[VERT.string] = VERT
                #print vertDict[VERT.string].neighbourNormals
                updateTri.append(vertID)
                new_vertlist.append(VERT.getVerticePosition())
                vertID +=1
            # if in dict, attach NNV to existing vert          
            else:
                #print "**********CHECK******"
                #print vertDict[VERT.string].neighbourNormals
                vertDict[VERT.string].addNeighbourNormal(NNV)
                #print vertDict[VERT.string].neighbourNormals
                updateTri.append(vertDict[VERT.string].ID)
        trilist[index] = updateTri
        
        
    # CREATE TRI DICT 
    # get all NNVs from single points in triangle list
    #for index in range(0,1):
    for index in range(len(trilist)):
        TRI = Triangle(new_vertlist[trilist[index][0]-1],new_vertlist[trilist[index][1]-1],new_vertlist[trilist[index][2]-1]) #-1 needed?
        for node in trilist[index]:
            #print node
            dict_string = "(%s , %s , %s)" % (new_vertlist[node-1][0],new_vertlist[node-1][1],new_vertlist[node-1][2]) #-1 needed!
            #print dict_string            
            vertObject = vertDict[dict_string]
            #print vertObject.neighbourNormals
            TRI.neighbourNormals.append(vertObject.neighbourNormals)
        triDict[index+1] = TRI
        
    convexCornerList = []
    concaveCornerList = []
    convexChamferList = []
    concaveChamferList = []
    concaveConvexCase1List = []
    concaveConvexCase2List = []
    
    # SHARPENING 
    sharpenedTriList = []
    # order not important right? 
    for tri in triDict.values():
        triNV = tri.getNormalizedNormalVec()
        angleResults = testAngles(tri.getNormalizedNormalVec(),tri.neighbourNormals)
        
        # FLAT TRI
        if angleResults[0] < 3:   
            sharpenedTriList.append(tri)
            
        # CORNER TRI
        elif angleResults[1] == 3:
            equilateralTest = testEquilateral(tri.position)
            if equilateralTest[0]:
                directionVec = [-1 if val < 0 else 1 for val in triNV]
                moveVec = np.array(directionVec) * voxelsize/3.0
                convexConcavetest = testCornerConcaveConvex(tri.position,angleResults[3])
                if convexConcavetest == "CONCAVE": 
                    # DETECTION 
                    #print "CONCAVE"
                    concaveCornerList.append(tri)
                    # SHARPENING       
                    newpoint = np.around(np.array(equilateralTest[1]) - np.array(moveVec), decimals=5)
                    moveVecs = [(-np.multiply(item[0],voxelsize)/2.0) for item in angleResults[3]]
                    n15 = np.add(tri.n1,moveVecs[1])
                    n25 = np.add(tri.n2,moveVecs[2])
                    n35 = np.add(tri.n3,moveVecs[0])
                    TRI1 = Triangle(tri.n1,n15,newpoint)
                    sharpenedTriList.append(TRI1)
                    TRI2 = Triangle(n15,tri.n2,newpoint)
                    sharpenedTriList.append(TRI2)
                    TRI3 = Triangle(tri.n2,n25,newpoint)
                    sharpenedTriList.append(TRI3)
                    TRI4 = Triangle(n25,tri.n3,newpoint)
                    sharpenedTriList.append(TRI4)
                    TRI5 = Triangle(tri.n3,n35,newpoint)
                    sharpenedTriList.append(TRI5)
                    TRI6 = Triangle(n35,tri.n1,newpoint)
                    sharpenedTriList.append(TRI6)
                    
                elif convexConcavetest == "CONVEX": 
                    # DETECTION 
                    #print "CONVEX"
                    convexCornerList.append(tri)
                    # SHARPENING
                    newpoint = np.around(np.array(equilateralTest[1]) + np.array(moveVec), decimals=5)
                    moveVecs = [(np.multiply(item[0],voxelsize)/2.0) for item in angleResults[3]]
                    n15 = np.add(tri.n1,moveVecs[1])
                    n25 = np.add(tri.n2,moveVecs[2])
                    n35 = np.add(tri.n3,moveVecs[0])
                    TRI1 = Triangle(tri.n1,n15,newpoint)
                    sharpenedTriList.append(TRI1)
                    TRI2 = Triangle(n15,tri.n2,newpoint)
                    sharpenedTriList.append(TRI2)
                    TRI3 = Triangle(tri.n2,n25,newpoint)
                    sharpenedTriList.append(TRI3)
                    TRI4 = Triangle(n25,tri.n3,newpoint)
                    sharpenedTriList.append(TRI4)
                    TRI5 = Triangle(tri.n3,n35,newpoint)
                    sharpenedTriList.append(TRI5)
                    TRI6 = Triangle(n35,tri.n1,newpoint)
                    sharpenedTriList.append(TRI6)
                    
                    
                    
                    
                """else: 
                    # change nothing
                    sharpenedTriList.append(tri)"""
               
            else:
                print '***********************CASE1******************* '
                # DETECTION
                concaveConvexCase1List.append(tri)
                # SHARPENING
                dist1,dist2,dist3 = distance(tri.n1,tri.n2),distance(tri.n2,tri.n3),distance(tri.n3,tri.n1)
                #print dist1, dist2,dist3
                if np.isclose(dist3,dist1):
                    middleIndex,middlePos = 0,tri.n1
                elif np.isclose(dist1,dist2):
                    middleIndex,middlePos = 1,tri.n2
                elif np.isclose(dist2,dist3):
                    middleIndex,middlePos = 2,tri.n3
                
                                
                sideIndexes = [0,1,2]#.remove(singleIndex)
                sideIndexes.remove(middleIndex)
                moveVecs = [(np.multiply(item[0],voxelsize)/2.0) for item in angleResults[3]]
                #print moveVecs
                triList = [tri.n1,tri.n2,tri.n3]
                moveCheck = np.add(moveVecs,triList)
                if np.allclose(moveCheck[sideIndexes[0]],moveCheck[middleIndex]):
                    print moveCheck[sideIndexes[0]]
                    print moveCheck[middleIndex] 
                    sideOutterIndex,sideInnerIndex = sideIndexes[0],sideIndexes[1]
                elif np.allclose(moveCheck[sideIndexes[1]],moveCheck[middleIndex]):
                    print moveCheck[sideIndexes[1]]
                    print moveCheck[middleIndex] 
                    sideOutterIndex,sideInnerIndex = sideIndexes[1],sideIndexes[0]
                else:
                    print "OOPS"
                
                # sideOutter / sideInner check is fout? 
                
                
                singleFirst = np.add(triList[sideOutterIndex],np.subtract(triList[sideInnerIndex],middlePos))
                singleSecond = np.subtract(triList[sideOutterIndex],moveVecs[middleIndex])
                singleThird = np.add(singleFirst,moveVecs[sideOutterIndex])
                TRI1 = Triangle(singleFirst,singleSecond,middlePos)
                sharpenedTriList.append(TRI1)
                #TRI2 = Triangle(singleFirst,singleSecond,triList[sideOutterIndex])
                #sharpenedTriList.append(TRI2)
                TRI3 = Triangle(middlePos,singleThird,singleFirst)
                sharpenedTriList.append(TRI3)
                
        
        elif angleResults[1] == 2:
            # DETECTION
            concaveConvexCase2List.append(tri) 
            # SHARPENING
            #print "****************** CASE 2 ****************************"
            vecList = [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0],[-1.0, 0.0, 0.0],[0.0, -1.0, 0.0],[0.0, 0.0, -1.0]]
            for cornerVec in vecList:
            # write above in better way, unnecessary searches?)
                if angleResults[3].count([cornerVec]) == 2:
                    double = cornerVec # niet nodig 
                elif angleResults[3].count([cornerVec]) == 1:
                    single = cornerVec
                    singleIndex = angleResults[3].index([single])
            #print singleIndex
            triList = [tri.n1,tri.n2,tri.n3]
            doubleIndexes = [0,1,2]#.remove(singleIndex)
            #print doubleIndexes
            doubleIndexes.remove(singleIndex)
            #print doubleIndexes 
            # check distances from double to single
            if distance(triList[doubleIndexes[0]],triList[singleIndex]) > distance(triList[doubleIndexes[1]],triList[singleIndex]):
                doubleFIndex, doubleCIndex = doubleIndexes[0],doubleIndexes[1]
            elif distance(triList[doubleIndexes[1]],triList[singleIndex]) > distance(triList[doubleIndexes[0]],triList[singleIndex]):
                doubleFIndex,doubleCIndex = doubleIndexes[1],doubleIndexes[0]
            # triangle vertices defined
            singlePos = triList[singleIndex]
            doubleFPos = triList[doubleFIndex]
            doubleCPos = triList[doubleCIndex]
            # define 3 new vertices
            singleFirst = np.add(doubleCPos,doubleFPos)/2.0
            #print triList
            empty = [0.0,0.0,0.0]
            vecList = [ ]
            moveVec = np.subtract(singlePos,singleFirst)
            for i in range(len(moveVec)):
                if moveVec[i] != 0:
                    temp = np.copy(empty)
                    temp[i] = moveVec[i]
                    vecList.append(temp) 
            if np.allclose(distance(singleFirst,np.add(singleFirst,vecList[1])),distance(singlePos,np.add(singleFirst,vecList[1]))):
                singleSecond,singleThird = np.add(singleFirst,vecList[0]),np.add(singleFirst,vecList[1])
                 
            elif np.allclose(distance(singleFirst,np.add(singleFirst,vecList[0])),distance(singlePos,np.add(singleFirst,vecList[0]))): 
                singleSecond,singleThird = np.add(singleFirst,vecList[1]),np.add(singleFirst,vecList[0])
            # write sharpened triangles
            TRI1 = Triangle(singleFirst,doubleCPos,singleSecond)
            sharpenedTriList.append(TRI1)
            TRI2 = Triangle(singleFirst,singleSecond,singlePos)
            sharpenedTriList.append(TRI2)
            TRI3 = Triangle(singleFirst,singlePos,singleThird)
            sharpenedTriList.append(TRI3)    
            singleFourth = np.add(singleFirst,np.subtract(singleSecond,doubleCPos,))
            TRI4 = Triangle(singleFirst,doubleFPos,singleFourth)
            sharpenedTriList.append(TRI4)            
            
            """moveVecs = [(np.multiply(item[0],voxelsize)/2.0) for item in angleResults[3]]
            #print moveVecs
            singleSecond = np.add(singleFirst,moveVecs[doubleFIndex])
            singleThird = np.subtract(singlePos,moveVecs[doubleFIndex])
            # write sharpened triangles
            TRI1 = Triangle(doubleCPos,singleFirst,singleThird)
            sharpenedTriList.append(TRI1)
            TRI2 = Triangle(singleFirst,singleSecond,singleThird)
            sharpenedTriList.append(TRI2)
            TRI3 = Triangle(singleThird,singleSecond,singlePos)
            sharpenedTriList.append(TRI3)"""
            
           
           
           
           
        
        # CHAMFER TRI
        elif angleResults[2] == 2:
            if checkOrtho(angleResults[4]):
                convexConcavetest = testCornerConcaveConvex(tri.position,angleResults[4])
                if convexConcavetest == "CONCAVE": 
                    # DETECTION
                    convexChamferList.append(tri)
                    # SHARPENING
                    vecList = [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0],[-1.0, 0.0, 0.0],[0.0, -1.0, 0.0],[0.0, 0.0, -1.0]]
                    for chamferVec in vecList:
                    # write above in better way, unnecessary searches?)
                        if angleResults[4].count([chamferVec]) == 2:
                            double = chamferVec # niet nodig 
                        elif angleResults[4].count([chamferVec]) == 1:
                            single = chamferVec
                            singleIndex = angleResults[4].index([single]) # only finds first, allowed in case of single
                    triList = [tri.n1,tri.n2,tri.n3]
                    doubleIndexes = [0,1,2]#.remove(singleIndex)
                    doubleIndexes.remove(singleIndex)
                    # check distances from double to single
                    if distance(triList[doubleIndexes[0]],triList[singleIndex]) > distance(triList[doubleIndexes[1]],triList[singleIndex]):
                        doubleFIndex, doubleCIndex = doubleIndexes[0],doubleIndexes[1]
                    elif distance(triList[doubleIndexes[1]],triList[singleIndex]) > distance(triList[doubleIndexes[0]],triList[singleIndex]):
                         doubleFIndex,doubleCIndex = doubleIndexes[1],doubleIndexes[0]
                    
                    # triangle vertices defined
                    singlePos = triList[singleIndex]
                    doubleFPos = triList[doubleFIndex]
                    doubleCPos = triList[doubleCIndex]
                    # construct next 2 vertices 
                    moveVec = [(-np.multiply(item,voxelsize)/2.0) for item in double]
                    singleFirst = np.add(singlePos,moveVec)
                    singleSecond = np.add(singleFirst,np.subtract(doubleFPos,doubleCPos))
                    # write sharpened triangles 
                    TRI1 = Triangle(singleFirst,doubleCPos,doubleFPos)
                    sharpenedTriList.append(TRI1)
                    TRI2 = Triangle(singleFirst,doubleFPos,singleSecond)
                    sharpenedTriList.append(TRI2)
                    
                elif convexConcavetest == "CONVEX": 
                    concaveChamferList.append(tri)
                    #print "*************** CONVEX CHAMFER *****************"
                    #print tri
                    #print angleResults[4]
                    vecList = [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0],[-1.0, 0.0, 0.0],[0.0, -1.0, 0.0],[0.0, 0.0, -1.0]]
                    for chamferVec in vecList:
                    # write above in better way, unnecessary searches?)
                        if angleResults[4].count([chamferVec]) == 2:
                            double = chamferVec # niet nodig 
                        elif angleResults[4].count([chamferVec]) == 1:
                            single = chamferVec
                            singleIndex = angleResults[4].index([single]) # only finds first, allowed in case of single
                            
                    triList = [tri.n1,tri.n2,tri.n3]
                    doubleIndexes = [0,1,2]#.remove(singleIndex)
                    doubleIndexes.remove(singleIndex)
                    # check distances from double to single
                    if distance(triList[doubleIndexes[0]],triList[singleIndex]) > distance(triList[doubleIndexes[1]],triList[singleIndex]):
                        doubleFIndex, doubleCIndex = doubleIndexes[0],doubleIndexes[1]
                    elif distance(triList[doubleIndexes[1]],triList[singleIndex]) > distance(triList[doubleIndexes[0]],triList[singleIndex]):
                         doubleFIndex,doubleCIndex = doubleIndexes[1],doubleIndexes[0]
                    
                    # triangle vertices defined
                    singlePos = triList[singleIndex]
                    doubleFPos = triList[doubleFIndex]
                    doubleCPos = triList[doubleCIndex]
                    # construct next 2 vertices 
                    moveVec = [(np.multiply(item,voxelsize)/2.0) for item in double]
                    singleFirst = np.add(singlePos,moveVec)
                    singleSecond = np.add(singleFirst,np.subtract(doubleFPos,doubleCPos))
                    # write sharpened triangles 
                    TRI1 = Triangle(singleFirst,doubleCPos,doubleFPos)
                    sharpenedTriList.append(TRI1)
                    TRI2 = Triangle(singleFirst,doubleFPos,singleSecond)
                    sharpenedTriList.append(TRI2)
                    
                    
                else:
                    # change nothing
                    sharpenedTriList.append(tri)
                    
            else: 
                # change nothing
                sharpenedTriList.append(tri)
        else:
            # change nothing
            #print tri
            sharpenedTriList.append(tri)
    # WRITE SHARPENED TRIANGLES TO VERT AND TRI LIST 
    sharp_vertlist = []
    sharp_trilist = []
    vertID = 1
    for tri in sharpenedTriList:
        index_tri = []
        #print tri.position
        for vert in tri.position:
            sharp_vertlist.append(vert)
            index_tri.append(vertID)
            vertID+=1
        sharp_trilist.append(index_tri)

            
             
            
            
    """    
    testlist2OBJ(convexCornerList, "convexCornerList.obj")
    testlist2OBJ(concaveCornerList, "concaveCornerList.obj")
    testlist2OBJ(concaveConvexCase1List, "concaveConvexCase1List.obj")
    testlist2OBJ(concaveConvexCase2List, "concaveConvexCase2List.obj")
    testlist2OBJ(convexChamferList, "convexChamferList.obj")
    testlist2OBJ(concaveChamferList, "concaveChamferList.obj")
    testlist2OBJ(sharpenedTriList, "sharpenedTriList.obj")"""
    return sharp_vertlist, sharp_trilist
  
            
        