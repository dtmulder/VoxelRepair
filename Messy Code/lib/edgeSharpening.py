# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 17:24:25 2015

@author: Damien
"""
import numpy as np
from operator import itemgetter
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
    angle = np.arccos(np.dot(v1_u, v2_u))
    #print 'angle = '
    #print angle
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

def thinNVList(nvlist):
    NVset_thinned = sorted(nvlist, key=itemgetter(0,1,2))
    for i in range(len(NVset_thinned)-1,-1,-1):
        vec1 = NVset_thinned[i]
        vec2 = NVset_thinned[i-1]
        if np.array_equal(vec1,vec2):
            del NVset_thinned[i]
        else:
            continue
    return NVset_thinned
        
##############################################################################
# filter triangles based on NV collection                                    #
##############################################################################
def NVcollection(triNV,NVset):
    print "********** START TEST ************"
    print "start NVcollection"
    # add 3 lists together
    print NVset
    flatNVset = [NV for subset in NVset for NV in subset]
    NVset_thinned = thinNVList(flatNVset)
    # def thinNVlist
    numberUnique = len(NVset_thinned)
    print "numberUnique  = "+ str(numberUnique)
    # get corner and chamfer tris 
    if numberUnique > 2:
        """chamferNVs = []
        cornerNVs = []""" 
        
        """for vector in NVset_thinned:
            # get angle between vector and tri NV
            #print 'trinv = '
            #print triNV
            #print 'vector = '
            #print vector
            if np.allclose([angle_between(triNV, vector)],[0.955316618125]): # assumption, correct for MC?
                cornerNVs.append(vector)
            elif np.allclose([angle_between(triNV, vector)],[0.785398163397]): # assumption, correct for MC?
                chamferNVs.append(vector)    
        numberCornerNVs = len(cornerNVs)
        numberChamferNVs = len(chamferNVs)"""
        
        #print triNV
        original_CornerNVs = [[],[],[]]
        original_ChamferNVs = [[],[],[]]
        
        
        #print original_ChamferNVs
        for subset in range(3):
            #print subset
            
            for vec in NVset[subset]:
                if np.allclose([angle_between(triNV, vec)],[0.955316618125]): # assumption, correct for MC?
                    original_CornerNVs[subset].append(vec)
                elif np.allclose([angle_between(triNV, vec)],[0.785398163397]):
                    original_ChamferNVs[subset].append(vec)
        
        #print original_CornerNVs
        original_CornerNVs = [NV for subset in original_CornerNVs for NV in subset]
        unique_CornerNVs = thinNVList(original_CornerNVs)
        numberCornerNVs = len(unique_CornerNVs)
        
        
        
        original_ChamferNVs = [NV for subset in original_ChamferNVs for NV in subset]
        unique_ChamferNVs = thinNVList(original_ChamferNVs)       
        numberChamferNVs = len(unique_ChamferNVs)
        
        print "numberCornerNVs = " + str(numberCornerNVs)
        print "numberChamferNVs = " + str(numberChamferNVs)
        """
        print triNV
        print "original_cornerNvs = "
        print original_CornerNVs
        print "original_ChamferNVs = "
        print original_ChamferNVs 
        print NVset_sorted
        print cornerNVs"""
        # FILTER NVset, ortho's only, keep old list structure
        return numberUnique, numberCornerNVs, numberChamferNVs, original_CornerNVs, original_ChamferNVs
    else:
        
        return numberUnique

    #return numberUnique, orthoNVs
    #return numberUnique

def detectTriangles(vertlist,trilist):
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
                VERT.addNeighbourNormal(NNV)
                vertDict[VERT.string] = VERT
                updateTri.append(vertID)
                new_vertlist.append(VERT.getVerticePosition())
                vertID +=1
            # if in dict, attach NNV to existing vert          
            else:
                vertDict[VERT.string].addNeighbourNormal(NNV)
                updateTri.append(vertDict[VERT.string].ID)
        # UPDATE TRIANGLES 
        trilist[index] = updateTri
        
        
    # CREATE TRI DIT 
    # get all NNVs from single points in triangle list
    for index in range(0,1):
        print index
    #for tri in trilist:
        #print trilist[index]
        # add real positions in triangle! 
        TRI = Triangle(new_vertlist[trilist[index][0]-1],new_vertlist[trilist[index][1]-1],new_vertlist[trilist[index][2]-1])
        for node in trilist[index]:
            dict_string = "(%s , %s , %s)" % (new_vertlist[node][0],new_vertlist[node][1],new_vertlist[node][2])
            vertObject = vertDict[dict_string]
            # create Triangle objecs, store in dict? 
            TRI.neighbourNormals.append(vertObject.neighbourNormals)
        triDict[index+1] = TRI
        
    
    # order not important right? 
    for tri in triDict.values():
        print '*************** NEW TRIANGLE TEST **********************'
        #print tri.position
        #print tri.getNormalizedNormalVec()
        print tri.neighbourNormals
        #
        #print 'ortho angle ='
        #print angle_between([0.0, -0.70711, -0.70711],[0.0, 0.0, -1.0])
        #print angle_between([0.57735,0.57735,0.57735],[0.0, 0.0, 1.0])
        #print angle_between([0.57735,0.57735,0.57735],[0.0, 0.0, -1.0])
        #print np.degrees(angle_between([0.0, -0.70711, -0.70711],[0.0, 0.0, -1.0]))
         
        
        print NVcollection(tri.getNormalizedNormalVec(),tri.neighbourNormals)
        """
        #do stuff
        #find cases
        # first find unique number
        # then find orthogonal vectors
        # where to combine vectors and where to seperate? 
        # new obj files can be created for each case for testing.
        """
    return new_vertlist, trilist

   
    #for node in updateTri:
    #    print node
    #    print vertlist[node]
    #print vertDict.items()[0][1].neighbourNormals
    # now for each tri, create triangle class, init uses node NV's?     
            
        