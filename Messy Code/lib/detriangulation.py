# -*- coding: utf-8 -*-
"""
Created on Thu May 07 21:58:35 2015

@author: Damien
"""
import numpy as np

# mc_detriangulation.py
##############################################################################
# segment dictionary
##############################################################################
SegmentDict = {
		'(1.0, 0.0, 0.0)'  											:	0,
		'(-1.0, 0.0, 0.0)' 											:	1,
		'(0.0, 1.0, 0.0)'  											:	2,
		'(0.0, -1.0, 0.0)' 											:	3,
		'(0.0, 0.0, 1.0)'  											:	4,
		'(0.0, 0.0, -1.0)' 											:	5,
		'(0.70711000000000002, 0.70711000000000002, 0.0)' 				:	6,
		'(0.70711000000000002, -0.70711000000000002, 0.0)' 				:	7,
		'(0.70711000000000002, 0.0, 0.70711000000000002)' 				:	8,
		'(0.70711000000000002, 0.0, -0.70711000000000002)' 				:	9,
		'(-0.70711000000000002, 0.70711000000000002, 0.0)' 				:	10,
		'(-0.70711000000000002, -0.70711000000000002, 0.0)' 				:	11,
		'(-0.70711000000000002, 0.0, 0.70711000000000002)'  				:	12,
		'(-0.70711000000000002, 0.0, -0.70711000000000002)'				: 	13,
        '(0.0, 0.70711000000000002, 0.70711000000000002)'  				: 	14,
        '(0.0, 0.70711000000000002, -0.70711000000000002)'  				:  	15,
        '(0.0, -0.70711000000000002, 0.70711000000000002)'  				:  	16,   
        '(0.0, -0.70711000000000002, -0.70711000000000002)' 				: 	17,
		'(0.57735000000000003, 0.57735000000000003, 0.57735000000000003)'  : 	18,
        '(0.57735000000000003, 0.57735000000000003, -0.57735000000000003)'  : 	19,	
        '(0.57735000000000003, -0.57735000000000003, 0.57735000000000003)'  : 	20,
        '(0.57735000000000003, -0.57735000000000003, -0.57735000000000003)' : 	21,
        '(-0.57735000000000003, 0.57735000000000003, 0.57735000000000003)'  : 	22,
        '(-0.57735000000000003, -0.57735000000000003, 0.57735000000000003)' : 	23,
        '(-0.57735000000000003, 0.57735000000000003, -0.57735000000000003)' : 	24,
        '(-0.57735000000000003, -0.57735000000000003, -0.57735000000000003)':	25,
		} 
  
##############################################################################
# Triangle class
##############################################################################  
class Triangle: 
    def __init__(self,n1,n2,n3):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        
    def getNormalizedNormalVec(self,vertlist):
        # create Vertice for each node
        #Vert1 = Vertice(self.n1[0],self.n1[1],self.n1[2],self.model,self.dims,self.scale,self.translate)
        #Vert2 = Vertice(self.n2[0],self.n2[1],self.n2[2],self.model,self.dims,self.scale,self.translate)
        #Vert3 = Vertice(self.n3[0],self.n3[1],self.n3[2],self.model,self.dims,self.scale,self.translate)
        # get real pos for each Vertice, list as TriPos
        #Vert1Pos = Vert1.getVerticePosition()
        #Vert2Pos = Vert2.getVerticePosition()
        #Vert3Pos = Vert3.getVerticePosition()
        
        Vert1Pos = vertlist[self.n1]
        Vert2Pos = vertlist[self.n2] 
        Vert3Pos = vertlist[self.n3]
        TriPos = [Vert1Pos,Vert2Pos,Vert3Pos]
        # calc normalized normal vecor for Tri
        # get vectors Vert1Vert2 & Vert2Vert3
        TriVectors = np.subtract(TriPos[1:],TriPos[:-1])
        # get crossproduct of Vert1Vert2 & Vert2Vert3 (= surface normal)
        TriNorm = np.cross(TriVectors[0],TriVectors[1])+0.0
        # get length of surface normal
        length = np.linalg.norm(TriNorm)
        # divide each component of surface normal by length (= normalized surface normal)
        TriNormSurfNorm = np.around(TriNorm / length, decimals=5) # rounded, otherwise different values, equals not found
        # create string of tuple for segment dict        
        SegmVector = str(tuple(TriNormSurfNorm))
        return SegmVector
  
def detriangulate(trilist,vertlist):
    testtri = trilist[0]
    print testtri
    i1,i2,i3 = testtri
    print i1,i2,i3
    tri_nodes_index = [i1,i2,i3]
    print vertlist[testtri[2]]
    tri_vec = Triangle(i1,i2,i3).getNormalizedNormalVec(vertlist)
    SegmentTriList[SegmentDict[tri_vec]].append(IndexNodesTri)
    # write gml file
    print "blabla"
    SegmentTriList = [[] for i in range(26)]
    
    
    
    
    
    
    
    
    
    
    
    
    
    