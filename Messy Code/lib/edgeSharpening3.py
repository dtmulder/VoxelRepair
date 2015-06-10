# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 13:05:53 2015

@author: Damien
"""
import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

class Vertice:

    def __init__(self, vert_id, coords):
        self.id = vert_id
        self.coords = coords
        self.edges = [] 
        self.triangles = []
        self.color = "grey" 
        
    def addEdge(self,edge_position):
        if edge_position not in self.edges:
            self.edges.append(edge_position) 
    
    def addTriangle(self,tri_id):
        #if edge_position not in self.edges:
        self.triangles.append(tri_id)     
    
class Edge:

    def __init__(self, edge_position, first_vertice_pos, second_vertice_pos, first_tri_id):
        self.position = edge_position
        self.first_vertice_pos = first_vertice_pos
        self.second_vertice_pos = second_vertice_pos
        self.first_tri_id = first_tri_id
        self.second_tri_id = 0
        self.color = "grey" 
        self.V = []
        
    def addSecondTri(self,second_tri_id):
        self.second_tri_id = second_tri_id
        
    """def find_new_vert(self):
        print "***************************"
        print edge
        # get point A & B
        A = edge.first_vertice_pos
        B = edge.second_vertice_pos 
        points = [A,B] 
        for point in points:
            #print point
            key = str(point)
            print key
            print topo_verts[key]"""
        
class Triangle:
    def __init__(self, tri_id, edge_keys, vert_keys,vert_positions):
        self.id = tri_id
        self.edges = edge_keys
        self.vertices = vert_keys
        self.color = "grey" 
        self.normal_vec = []
        self.normalized_normal_vec = []
        self.vert_positions = vert_positions
        # calculate normal vec
        self.getNormalizedNormalVec(vert_positions)
        self.W = []
    
    def getNormalizedNormalVec(self,vert_positions):
        tri_positions = [list(vert_pos) for vert_pos in vert_positions]
        # vectors v1-v2 & v2-v3
        tri_vectors = np.subtract(tri_positions[1:],tri_positions[:-1])
        # cross product
        normal_vec = np.cross(tri_vectors[0],tri_vectors[1])+0.0
        self.normal_vec = normal_vec.tolist()
        # get length of surface normal
        length = np.linalg.norm(normal_vec)        
        # divide each component of surface normal by length (= normalized surface normal)
        normalized_normal_vec = np.around(normal_vec / length, decimals=5) 
        self.normalized_normal_vec = normalized_normal_vec.tolist() 
        

def process_triangle_objects(object_list):
    print "***********************"
    vert_list = []
    tri_list = []
    vertID = 1
    
    for triangle in object_list:
        index_tri = []
        
        for vert in triangle.vert_positions:
            vert_list.append(vert)
            index_tri.append(vertID)
            vertID+=1
        tri_list.append(index_tri)
    return vert_list,tri_list
        
        
        
        
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
        
        
def get_blue_edge_vert(edge,A,B,topo_triangles):
    points = [A,B] 
    normalized_weighted_sums = []
    for point in points:
        #print point.triangles
        triangle_normals = []
        triangle_angles = []
        for key in point.triangles:
            triangle = topo_triangles[key]
            if triangle.color == 'red':
                edge_start = point.coords
                # get normals
                triangle_normals.append(triangle.normal_vec)
                # get weights
                edge_ends = [vert for vert in triangle.vert_positions if vert != edge_start]
                v1 = np.subtract(edge_ends[0],edge_start)
                v2 = np.subtract(edge_ends[1],edge_start)
                angle = angle_between(v1,v2)
                triangle_angles.append(angle)
        # calculate weighted sum
        total = sum(triangle_angles)
        triangle_weights = [angle/total for angle in triangle_angles]
        zipped = zip(triangle_normals, triangle_weights)
        weighted_angles = [ normal/weight for normal,weight in zipped]
        weighted_sum = np.sum(weighted_angles, axis=0)
        # normalize weighted sum
        length = np.linalg.norm(weighted_sum)       
        normalized_weighted_sum = np.around(weighted_sum / length, decimals=5)
        normalized_weighted_sums.append(normalized_weighted_sum)
    N,M = normalized_weighted_sums 
    AB = np.subtract(A.coords,B.coords) # A dan B? of ergens anders omgedraaid? 
    # H=ABx(MxN)
    H = np.cross (AB , np.cross(M,N) )
    # h=AB•N
    h = np.dot(  AB , N)
    # k = 2(M•N)(AB•N)–2(AB•M)
    k = (2*np.dot(M,N) * np.dot(AB,N)) - (2* np.dot(AB,M))
    #V = (A+B)/2+(h/k)H
    V = np.add(B.coords,A.coords)/2 + (h/k)*H
    #print "*********************************************"
    #print list(A.coords)
    #print list(B.coords)
    dist1 = np.linalg.norm(np.array(A.coords)-list(B.coords))
    dist2 = np.linalg.norm(V-list(A.coords))
    dist3 = np.linalg.norm(V-list(B.coords))
    
    print dist2
    if dist2 > 0.39:  # CUSTOMIZE THIS VALUE! EEK  
        print "LONG EDGE IN CHAMFER EDGE" 
        print dist2
        print dist3
        print A.coords
        print B.coords
        print V
        V = (np.array(A.coords)+ np.array(B.coords)) / 2
        #print new
    #dist = np.linalg.norm(w-list(planes[0][0]))
    #dist = np.linalg.norm(w-list(planes[0][0]))
    #print dist
    #print V
    #print dist1
    #print dist2
    #print dist3
    return V
    
def get_green_tri_vert(A,B,C,triangle,topo_triangles):
    points = [A,B,C]
    normalized_weighted_sums = []
    for point in points:
        #print point.triangles
        triangle_normals = []
        triangle_angles = []
        for key in point.triangles:
            triangle = topo_triangles[key]
            if triangle.color == 'red':
                edge_start = point.coords
                # get normals
                triangle_normals.append(triangle.normal_vec)
                # get weights
                edge_ends = [vert for vert in triangle.vert_positions if vert != edge_start]
                v1 = np.subtract(edge_ends[0],edge_start)
                v2 = np.subtract(edge_ends[1],edge_start)
                angle = angle_between(v1,v2)
                triangle_angles.append(angle)
        # calculate weighted sum
        total = sum(triangle_angles)
        triangle_weights = [angle/total for angle in triangle_angles]
        zipped = zip(triangle_normals, triangle_weights)
        weighted_angles = [ normal/weight for normal,weight in zipped]
        weighted_sum = np.sum(weighted_angles, axis=0)
        # normalize weighted sum
        length = np.linalg.norm(weighted_sum)       
        normalized_weighted_sum = np.around(weighted_sum / length, decimals=5)
        normalized_weighted_sums.append(normalized_weighted_sum)
    N,M,L = normalized_weighted_sums 
    # solve equations with least squares
    planes = [(A.coords,N),(B.coords,M),(C.coords,L)]
    a = [n for p,n in planes]
    b = [np.dot(p,n) for p,n in planes]

    w, residue, rank, s = np.linalg.lstsq(a, b)
    #print 'w'
    #print w
    #print 'planes'
    #print planes[0][0]
    dist = np.linalg.norm(w-list(planes[0][0]))
    print dist
    #print dist
    if dist > 2:
        print "LONG EDGE IN TRIANGLE"
        print A.coords
        print B.coords 
        print C.coords
        w= (np.array(A.coords)+ np.array(B.coords) + np.array(C.coords)) / 3
        print tuple(w)
        #print dist
        #print "HIERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR"
        #print "HIERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR"
    return w

def createTopology(vertlist,trilist):
    # SET UP TOPOLOGY
    vert_id = 1
    tri_id = 1
    topo_verts = {}
    topo_edges = {}
    topo_triangles = {}
    for tri in trilist:
        # CREATE TOPO VERTICES
        vert_ids = []
        vert_positions = []
        for vert_id in tri:
            vert_pos_real = vertlist[vert_id-1]
            vert_key = str(vert_pos_real) # check precision later
            if vert_key not in topo_verts:
                topo_verts[vert_key] = Vertice(vert_id,vert_pos_real)
                vert_ids.append(vert_id)
                vert_positions.append(vert_pos_real)
                vert_id +=1
            elif vert_key in topo_verts:
                vert_ids.append(topo_verts[vert_key].id)
                vert_positions.append(vert_pos_real)
            # add triangle id to point
            topo_verts[vert_key].addTriangle(tri_id)
            
        # CREATE TOPO EDGES
        edge_positions = []
        vert_positions_sorted = sorted(vert_positions)
        edge_couples = [vert_positions_sorted[:-1], vert_positions_sorted[1:] , [vert_positions_sorted[0],vert_positions_sorted[2]] ]
        edge_positions = [ a+b for a,b in edge_couples]
        for edge_position in edge_positions:
            edge_key = str(edge_position)
            if edge_key not in topo_edges:
                # add edge to dict
                topo_edges[edge_key] = Edge(edge_position,edge_position[:3],edge_position[3:],tri_id)
                
            elif edge_key in topo_edges:
                # add tri
                topo_edges[edge_key].addSecondTri(tri_id)
                
                
        vert_keys = [str(key) for key in vert_positions_sorted]
        edge_keys = [str(edge) for edge in edge_positions]
        
        # UPDATE TOPO VERTICES (ADD EDGES, see edge couples for indexing)
        topo_verts[vert_keys[0]].addEdge(edge_keys[0])
        topo_verts[vert_keys[0]].addEdge(edge_keys[2])
        topo_verts[vert_keys[1]].addEdge(edge_keys[0])
        topo_verts[vert_keys[1]].addEdge(edge_keys[1])
        topo_verts[vert_keys[2]].addEdge(edge_keys[1])   
        topo_verts[vert_keys[2]].addEdge(edge_keys[2])
        
        # CREATE TOPO TRIANGLES 
        topo_triangles[tri_id] = Triangle(tri_id,edge_keys,vert_keys,vert_positions)
        tri_id += 1
    
    
    # FILTER STEP 0
    # loop through edges: incident triangles NNV close? then edge brown
    for key,edge in topo_edges.iteritems():
        # find adjacent triangle normals
        n1 = topo_triangles[edge.first_tri_id].normalized_normal_vec
        n2 = topo_triangles[edge.second_tri_id].normalized_normal_vec
        # get angle between normals
        angle = angle_between(n1,n2)
        if angle < 0.1:        # threshold? 'less than twice the average of such angles'
            edge.color = "brown"
            
    # FILTER STEP 1
    # loop through vertices: all incident edges brown? then vertice red 
    for key,vertice in topo_verts.iteritems():
        # find adjacent edge colors 
        edge_colors = []
        for key in vertice.edges:
            edge_colors.append(topo_edges[key].color)
        # check if all edges are brown
        if edge_colors[0] == 'brown' and len(set(edge_colors)) == 1:
            vertice.color = 'red'
    
    # FILTER STEP 2
    # loop through triangles: any vertice red? then triangle red 
    for key,triangle in topo_triangles.iteritems(): # wat is het snelst? itervalues() !? 
        vert_colors = []
        for key in triangle.vertices:
            vert_colors.append(topo_verts[key].color)
        if 'red' in vert_colors:
            triangle.color = 'red'
    
    # FILTER STEP 3
    # for through non-red triangles: adjacent to red triangle through brown edge? then triangle red (recursively!)
    n = 1
    while n < len(topo_triangles):
        if topo_triangles[n].color != 'red':
            triangle = topo_triangles[n]
            for key in triangle.edges:
                if topo_edges[key].color == 'brown':
                    edge = topo_edges[key]
                    if edge.first_tri_id == triangle.id:
                        adjacent_tri_id = edge.second_tri_id
                    else:
                        adjacent_tri_id = edge.first_tri_id
                        
                    if topo_triangles[adjacent_tri_id].color == 'red':
                        triangle.color = 'red'
                        # start loop from start, correct? 
                        n = 1  # really needed? 
                        continue 
                    else:
                        pass
        n += 1

    # FILTER STEP 4
    # loop through triangles: triangle red? make all edges and vertice red 
    for key,triangle in topo_triangles.iteritems():
        if triangle.color == 'red': 
            for key in triangle.vertices:
                topo_verts[key].color = 'red'
            for key in triangle.edges:
                topo_edges[key].color = 'red'
                
    # FILTER STEP 5
    # loop through non-red edges: both vertices red? make edge blue
    for key,edge in topo_edges.iteritems():
        if edge.color != 'red':
            key_1 = str(edge.first_vertice_pos)
            key_2 = str(edge.second_vertice_pos)
            if topo_verts[key_1].color == 'red' and topo_verts[key_2].color == 'red':
                edge.color = 'blue'
                A = topo_verts[str(edge.first_vertice_pos)]
                B = topo_verts[str(edge.second_vertice_pos)]
                edge.V = get_blue_edge_vert(edge,A,B,topo_triangles)
 
    # FILTER STEP 6
    # loop though triangles: all edges blue? make triangle green
    for key,triangle in topo_triangles.iteritems():
        edge_colors = []
        for key in triangle.edges:
            edge_colors.append(topo_edges[key].color)
        if edge_colors[0] == 'blue' and len(set(edge_colors)) == 1:
            triangle.color = 'green'
        
    # identify triangles
    #vertList = []
    normal_triangles = []
    corner_triangles = []
    chamfer_triangles_one = []
    chamfer_triangles_two = []
    sharpened = []
    # calculate V points on blue edges
    #for key,edge in topo_edges.iteritems():
       #if edge.color == 'blue' 
    
    for key,triangle in topo_triangles.iteritems():
        
        
        # PROCESS CORNER TRIANGLES 
        if triangle.color == 'green':
            points = []
            for key in triangle.vertices:
                points.append(topo_verts[key])
            A,B,C = points
            triangle.W = get_green_tri_vert(A,B,C,triangle,topo_triangles) 
            v1,v2,v3 = triangle.vert_positions
            edge_couples = [[v1,v2],[v2,v3],[v1,v3]]
            edge_verts = []
            for couple in edge_couples:
                sorted_couple = sorted(couple)
                key = str(sorted_couple[0] + sorted_couple[1])
                edge_verts.append(topo_edges[key].V)
                
            v15,v25,v35 = edge_verts
            # write 6 triangles
            # topology can be ignored now
            sharpened.append( Triangle(0,[],[],[v1,v15,triangle.W]) )
            sharpened.append( Triangle(0,[],[],[v15,v2,triangle.W]) )
            sharpened.append( Triangle(0,[],[],[v2,v25,triangle.W]) )
            sharpened.append( Triangle(0,[],[],[v25,v3,triangle.W]) )
            sharpened.append( Triangle(0,[],[],[v3,v35,triangle.W]) )
            sharpened.append( Triangle(0,[],[],[v35,v1,triangle.W]) )
            #corner_triangles.append(triangle)
            corner_triangles.append( Triangle(0,[],[],[v1,v15,triangle.W]) )
            corner_triangles.append( Triangle(0,[],[],[v15,v2,triangle.W]) )
            corner_triangles.append( Triangle(0,[],[],[v2,v25,triangle.W]) )
            corner_triangles.append( Triangle(0,[],[],[v25,v3,triangle.W]) )
            corner_triangles.append( Triangle(0,[],[],[v3,v35,triangle.W]) )
            corner_triangles.append( Triangle(0,[],[],[v35,v1,triangle.W]) )
            
        
        else: 
            edge_colors = []
            blue_edges = []
            for key in triangle.edges:
                edge_colors.append(topo_edges[key].color)
                if topo_edges[key].color == 'blue':
                    blue_edges.append(topo_edges[key])
                    
            # PROCESS TRIANGLES WITH 1 BLUE EDGE    
            if edge_colors.count("blue") == 1:
                unordered = triangle.vert_positions
                #print "1 blue edge only!"
                # define triangles vertices based on blue edges
                # A is point without blue edge
                # B is point after A
                # C is point after B
                blue_occurence = []
                for edge in blue_edges:
                    blue_occurence.append(edge.first_vertice_pos)
                    blue_occurence.append(edge.second_vertice_pos)    
                #print unordered
                #print blue_occurence
                A = list ( set(unordered) - set(blue_occurence) ) [0]
                #print A
                # is this the best way? 
                chamfer_triangles_one.append(triangle)
                
                A_index = unordered.index(A)
                #print A_index
                # order the vertices without changing orientation, A first 
                if A_index == 0:
                    ordered = [unordered[0], unordered[1], unordered[2] ]
                elif A_index == 1:
                    ordered = [unordered[1], unordered[2], unordered[0] ]
                elif A_index == 2:
                    ordered = [unordered[2], unordered[0], unordered[1] ]
                A,B,C = ordered
                #print ordered
                BC_key = str( sorted(ordered[1:])[0] + sorted(ordered[1:])[1] )
                BC = topo_edges[BC_key].V
                #print BC
                sharpened.append( Triangle(0,[],[],[A,B,BC]) )
                sharpened.append( Triangle(0,[],[],[A,BC,C]) )
                chamfer_triangles_one.append( Triangle(0,[],[],[A,B,BC]) )
                chamfer_triangles_one.append( Triangle(0,[],[],[A,BC,C]) )
                # TEST THIS!!! 
                
            # PROCESS TRIANGLES WITH 2 BLUE EDGES    
            elif edge_colors.count("blue") == 2:
                #chamfer_triangles_two.append(triangle)
                unordered = triangle.vert_positions
                # define triangles vertices based on blue edges
                # B is point with 2 blue edges
                # A is point before B
                # C is point after B
                blue_occurence = []
                for edge in blue_edges:
                    blue_occurence.append(edge.first_vertice_pos)
                    blue_occurence.append(edge.second_vertice_pos) 
                
                B = [x for x in blue_occurence if blue_occurence.count(x) == 2][0]
                
                
                B_index = unordered.index(B)
                # order the vertices without changing orientation, B in middle
                if B_index == 0:
                    ordered = [unordered[2], unordered[0], unordered[1] ]
                elif B_index == 1:
                    ordered = [unordered[0], unordered[1], unordered[2] ]
                elif B_index == 2:
                    ordered = [unordered[1], unordered[2], unordered[0] ]
                  
                
                A,B,C = ordered
                AB_key = str( sorted(ordered[:2])[0] + sorted(ordered[:2])[1] )
                AB = topo_edges[AB_key].V
                BC_key = str( sorted(ordered[1:])[0] + sorted(ordered[1:])[1] )
                BC = topo_edges[BC_key].V
                
                sharpened.append( Triangle(0,[],[],[A,AB,C]) )
                sharpened.append( Triangle(0,[],[],[AB,B,BC]) )
                sharpened.append( Triangle(0,[],[],[AB,BC,C]) )
                chamfer_triangles_two.append(Triangle(0,[],[],[A,AB,C]))
                chamfer_triangles_two.append(Triangle(0,[],[],[AB,B,BC]) )
                chamfer_triangles_two.append(Triangle(0,[],[],[AB,BC,C]) )
                
                
                
            else:
                # normal triangle
                normal_triangles.append(triangle)
                sharpened.append(triangle)
                # add old triangle
                 
                
                
                
                
    """   
    print len(topo_triangles)
    print len(normal_triangles)
    print len(corner_triangles)
    print len(chamfer_triangles_one)        
    print len(chamfer_triangles_two)      
        
    # def write to obj    
    """
    # normal triangles to obj
    vert_list,tri_list = process_triangle_objects(normal_triangles)
    writeOBJ(vert_list,tri_list,"normal_triangle.obj")    
    
    # corner triangles to obj
    vert_list,tri_list = process_triangle_objects(corner_triangles)
    writeOBJ(vert_list,tri_list,"corner_triangle.obj")
    
    # chamfer triangles two to obj
    
    vert_list,tri_list = process_triangle_objects(chamfer_triangles_one)
    writeOBJ(vert_list,tri_list,"chamfer_triangle_1.obj")    
    
    vert_list,tri_list = process_triangle_objects(chamfer_triangles_two)
    writeOBJ(vert_list,tri_list,"chamfer_triangle_2.obj")
    """
    """
    # sharpened triangles two to obj
    vert_list,tri_list = process_triangle_objects(sharpened)
    writeOBJ(vert_list,tri_list,"sharpened.obj")
    
    #print "******* TEST *******"
    
    
    #test_tri = corner_triangles[1]
    #print test_tri.W
    
    #test_tri = chamfer_triangles_two[0]
    #for key in test_tri.edges:
    #    if topo_edges[key].color == 'blue':
    #        
    #        print topo_edges[key].V
    
   
    