# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 15:17:20 2015

@author: Damien
"""
import math
import numpy as np 

def rotateZ(a,pointXYZ):
    x = float(pointXYZ[0])
    y = float(pointXYZ[1])
    z = float(pointXYZ[2])
    xrot = x*(math.cos(a)) - y*(math.sin(a))
    yrot = x*math.sin(a) + y*math.cos(a)
    zrot = z
    return (xrot,yrot,zrot)

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

def align(OBJfile):
    # READ OBJ FILE 
    OBJ = open(OBJfile, 'r')
    vertlist = []
    trilist = []
    for line in OBJ:
        if line[0] == 'v':
            vsplit = line.split(" ")
            x = float(vsplit[1]); y = float(vsplit[2]); z = float(vsplit[3].rstrip('\n'))
            pointXYZ = (x,y,z)
            vertlist.append(pointXYZ)
        if line[0] == 'vt':
            print "texture coordinate is present but ignored"
        if line[0] == 'vn':
            print "normal is present but ignored "
        if line[0] == 'vp':
            print "parameter space vertice is present but ignored"
        if line[0] == 'f':
            fsplit = line.split(" ")
            v1 = int(fsplit[1]); v2 = int(fsplit[2]); v3 = int(fsplit[3])
            tri123 = (v1,v2,v3)
            trilist.append(tri123)
    # CHECK TRIANGLE SURFACE NORMALS 
    alignArea = 0
    alignVector = []
    OBJ.close()
    for tri in trilist:
        n1,n2,n3 = np.array(vertlist[tri[0]-1]),np.array(vertlist[tri[1]-1]),np.array(vertlist[tri[2]-1])
        realtri = [n1,n2,n3]
        # GET NORMALIZED NORMAL VECTOR 
        trivectors = np.subtract(realtri[1:],realtri[:-1])
        trinorm = np.cross(trivectors[0],trivectors[1])+0.0
        length = np.linalg.norm(trinorm)
        normalizedsurfnorm = np.around(trinorm / length, decimals=2)
        
        # IF VECTOR IS HORIZONTAL CONTINUE 
        if normalizedsurfnorm[2] > -0.1 and normalizedsurfnorm[2] < 0.1:
            # GET AREA
            a,b,c = np.linalg.norm(n2-n1) ,np.linalg.norm(n3-n2) ,np.linalg.norm(n1-n3) 
            s = (a+b+c) / 2.0
            area = np.sqrt(s*(s-a)*(s-b)*(s-c))
            # TAKE TRI WITH HIGHEST AREA 
            if area > alignArea:
                alignVector = normalizedsurfnorm
                alignArea = area 
    """REWRITE ABOVE?
    HOW TO FIND VECTOR IN DICT WHICH IS CLOSE? 
    1. base on largest tri
    2. base on largest xy distance tri
    3. base on multiple tri's  and sum? 
    """
                
                
    # GET ANGLE 
    alignTarget = [1,0,0]
    angleRAD =  angle_between(alignTarget, alignVector)
    
    if np.linalg.norm(alignTarget[0]-alignVector[0]) < 1.0:   # maak gebouw selectie en test! 
        angleRAD = -angleRAD
    
    # ROTATE OBJ FILE 
    rotOBJfile = OBJfile.replace(".obj", "_rot.obj");
    OBJ = open(OBJfile, 'r')
    OBJrot = open(rotOBJfile, 'w')
    for line in OBJ:
        if line[0] != 'v':
            OBJrot.write(line)
        if line[0] == 'v':
            vsplit = line.split(" ")  
            x = vsplit[1]
            y = vsplit[2]
            z = vsplit[3].rstrip('\n')
            point = (x,y,z)
            rotpoint = rotateZ(angleRAD,point)
            OBJrot.write("v " + str(rotpoint[0]) + " " + str(rotpoint[1]) + " " + str(rotpoint[2]) + "\n")
    OBJ.close()
    OBJrot.close()
    return angleRAD 

#test("9137.obj")

