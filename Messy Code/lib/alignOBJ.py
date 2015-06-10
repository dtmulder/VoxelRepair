# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:42:19 2015

@author: Damien
"""
import math
import numpy as np 
def getANGLE(OBJfile): # REWRITE, FIND LARGEST XY DISTACE IN ALL TRIANGLES
    OBJ = open(OBJfile, 'r')
    vertlist = []
    trilist = []
    for line in OBJ:
        #print line
        if line[0] == 'v':
            vsplit = line.split(" ")
            x = vsplit[1]; y = vsplit[2]; z = vsplit[3]
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
    OBJ.close()
    #print '_' * 50
    # DETERMINE THE ANGLE      REWRITE THIS!  
    # STEP 1 get point with smallest x, if several, take smallest y?
    p1 = min(vertlist)
    #print p1
    # sorts on x automatically? 
    #print 'step 1: point with minimal x'
    #print p1
    # for y use sorted([('abc', 121),('abc', 231),('abc', 148), ('abc',221)],key=lambda x: x[1])
    # STEP 2 get index of this point
    p1index = vertlist.index(p1)+1
    # STEP 3 get all triangles with this point, store their unique nodes
    connectedvertlist = []
    for tri in trilist: 
        if p1index in tri:
            #print tri
            for node in tri:
                if node not in connectedvertlist:
                    if node != p1index:
                        connectedvertlist.append(node)
    # 4 get all x values of the connected vert list
    xconnectedvertlist = []    
    for index in connectedvertlist: xconnectedvertlist.append(vertlist[index-1])
    #print xconnectedvertlist 
    # 5 get highest x 
    p2 = max(xconnectedvertlist) # again, sorts on x automatically  
    #print p2
    dx = float(p1[0]) - float(p2[0])
    dy = float(p1[1]) - float(p2[1]) 
    angleRAD = math.atan(dy/dx)
    angleDEG = math.degrees(angleRAD)
    #print "angldeRAD = " + str(angleRAD)
    #print "angleDEG = " + str(angleDEG)
    a = -angleRAD #blijkaar?
    #print a
    return a
    

def rotateXYZ(a,pointXYZ):
    x = float(pointXYZ[0])
    y = float(pointXYZ[1])
    z = float(pointXYZ[2])
    # x rotation   
    xrot = x*(math.cos(a)) - y*(math.sin(a))
    # y rotation 
    yrot = x*math.sin(a) + y*math.cos(a)
    # z rotation
    zrot = z
    return (xrot,yrot,zrot)
    
def allignOBJ(OBJfile):
    #print OBJfile
    rotOBJfile = OBJfile.replace(".obj", "_rot.obj");
    #print rotOBJfile
    #READ EXISTING AND NEW OBJ FILE     
    OBJ = open(OBJfile, 'r')
    OBJrot = open(rotOBJfile, 'w')
    # GET ALLIGNMENT ANGLE 
    a = getANGLE(OBJfile)
    # OVERWRITE FOR MISTAKES!! 
    
    # 6153 angle = 19.910
    #a = np.radians(-60.682)
    # 9137 angle = 28.811
    #a = np.radians(-28.811)

    #a = np.radians(-27.777)
    # LOOP THROUGH ALL LINES IN OBJfile
    
    for line in OBJ:
        if line[0] != 'v':
            #print line
            OBJrot.write(line)
        if line[0] == 'v':
            vsplit = line.split(" ")  
            #print vsplit
            x = vsplit[1]
            y = vsplit[2]
            z = vsplit[3]
            point = (x,y,z)
            #print point
            rotpoint = rotateXYZ(a,point)
            #print rotpoint
            OBJrot.write("v " + str(rotpoint[0]) + " " + str(rotpoint[1]) + " " + str(rotpoint[2]) + "\n")
    OBJ.close()
    OBJrot.close()
    return a
    



"""Rotation along X:
y' = y*cos(a) - z*sin(a)
z' = y*sin(a) + z*cos(a)
x' = x

Rotation along Y:
z' = z*cos(a) - x*sin(a)
x' = z*sin(a) + x*cos(a)
y' = y

Rotation along Z:
x' = x*cos(a) - y*sin(a)
y' = x*sin(a) + y*cos(a)
z' = z"""