import sys

def cross_product(u, v):
    return (u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0])

def dot_product(u, v):
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

def vector_subtract(u, v):
    return (u[0]-v[0], u[1]-v[1], u[2]-v[2])

def make_plane(p0, p1, p2):
    v1 = vector_subtract(p1, p0)
    v2 = vector_subtract(p2, p0)
    normal = cross_product(v1, v2)
    if all(abs(coord) < 1e-10 for coord in normal):  # Triângulo degenerado
        return None
    d = -dot_product(normal, p0)
    return (normal[0], normal[1], normal[2], d)

def classify_point(plane, point, tol=1e-10):
    a, b, c, d = plane
    x, y, z = point
    value = a*x + b*y + c*z + d
    if abs(value) < tol:
        return "COPLANAR"
    elif value > 0:
        return "POSITIVE"
    else:
        return "NEGATIVE"

def classify_triangle(plane, triangle):
    sides = [classify_point(plane, p) for p in triangle]
    if all(s == "COPLANAR" for s in sides):
        return "COPLANAR"
    has_positive = any(s == "POSITIVE" for s in sides)
    has_negative = any(s == "NEGATIVE" for s in sides)
    if has_positive and has_negative:
        return "CROSSING"
    elif has_positive:
        return "POSITIVE"
    else:
        return "NEGATIVE"

def intersect_edge_plane(p, q, plane):
    a, b, c, d = plane
    num = -(a*p[0] + b*p[1] + c*p[2] + d)
    denom = a*(q[0]-p[0]) + b*(q[1]-p[1]) + c*(q[2]-p[2])
    if abs(denom) < 1e-10:
        return p
    t = num / denom
    x = p[0] + t*(q[0]-p[0])
    y = p[1] + t*(q[1]-p[1])
    z = p[2] + t*(q[2]-p[2])
    return (x, y, z)

def split_triangle(triangle, plane):
    pts = triangle
    sides = [classify_point(plane, p) for p in pts]
    
    positive_pts = []
    negative_pts = []
    coplanar_pts = []
    for i in range(3):
        if sides[i] == "POSITIVE":
            positive_pts.append(pts[i])
        elif sides[i] == "NEGATIVE":
            negative_pts.append(pts[i])
        else:
            coplanar_pts.append(pts[i])
    
    if len(positive_pts) == 1 and len(negative_pts) == 2:
        P = positive_pts[0]
        N1, N2 = negative_pts
        I1 = intersect_edge_plane(P, N1, plane)
        I2 = intersect_edge_plane(P, N2, plane)
        return [
            [P, I1, I2],      # Triângulo positivo
            [N1, I1, I2],     # Triângulo negativo 1
            [N1, I2, N2]      # Triângulo negativo 2 (conectado a N1)
        ]
    elif len(positive_pts) == 2 and len(negative_pts) == 1:
        N = negative_pts[0]
        P1, P2 = positive_pts
        I1 = intersect_edge_plane(N, P1, plane)
        I2 = intersect_edge_plane(N, P2, plane)
        return [
            [N, I1, I2],       # Triângulo negativo
            [I1, P1, I2],      # Triângulo positivo 1
            [I1, I2, P2]       # Triângulo positivo 2
        ]
    elif len(positive_pts) == 1 and len(negative_pts) == 1 and len(coplanar_pts) == 1:
        P = positive_pts[0]
        N = negative_pts[0]
        C = coplanar_pts[0]
        I = intersect_edge_plane(P, N, plane)
        return [[P, C, I], [N, C, I]]
    else:
        return [triangle]

def point_in_triangle_3d(P, triangle):
    A, B, C = triangle
    AB = vector_subtract(B, A)
    AC = vector_subtract(C, A)
    n = cross_product(AB, AC)
    
    PA = vector_subtract(A, P)
    PB = vector_subtract(B, P)
    PC = vector_subtract(C, P)
    
    n1 = cross_product(PB, PC)
    n2 = cross_product(PC, PA)
    n3 = cross_product(PA, PB)
    
    d1 = dot_product(n1, n)
    d2 = dot_product(n2, n)
    d3 = dot_product(n3, n)
    
    if (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0):
        return True
    return False

def point_on_segment_3d(P, seg):
    A = (seg[0], seg[1], seg[2])
    B = (seg[3], seg[4], seg[5])
    AP = vector_subtract(P, A)
    AB = vector_subtract(B, A)
    crossAP_AB = cross_product(AP, AB)
    if abs(crossAP_AB[0]) > 1e-10 or abs(crossAP_AB[1]) > 1e-10 or abs(crossAP_AB[2]) > 1e-10:
        return False
    PB = vector_subtract(P, B)
    dot1 = dot_product(AP, PB)
    return dot1 <= 1e-10

def intersect_segment_triangle(segment, triangle):
    p0 = (segment[0], segment[1], segment[2])
    p1 = (segment[3], segment[4], segment[5])
    A, B, C = triangle
    plane = make_plane(A, B, C)
    if plane is None:
        return False
    a, b, c, d = plane
    
    dir_vec = [p1[i] - p0[i] for i in range(3)]
    denom = a*dir_vec[0] + b*dir_vec[1] + c*dir_vec[2]
    
    if abs(denom) < 1e-10:
        if classify_point(plane, p0) == "COPLANAR" and point_in_triangle_3d(p0, triangle):
            return True
        if classify_point(plane, p1) == "COPLANAR" and point_in_triangle_3d(p1, triangle):
            return True
        for Q in triangle:
            if classify_point(plane, Q) == "COPLANAR" and point_on_segment_3d(Q, segment):
                return True
        return False
    
    t = -(a*p0[0] + b*p0[1] + c*p0[2] + d) / denom
    if t < 0.0 or t > 1.0:
        return False
    
    x = p0[0] + t * dir_vec[0]
    y = p0[1] + t * dir_vec[1]
    z = p0[2] + t * dir_vec[2]
    P = (x, y, z)
    
    return point_in_triangle_3d(P, triangle)

class Node:
    __slots__ = ('plane', 'triangles', 'positive_child', 'negative_child')
    def __init__(self):
        self.plane = None
        self.triangles = []
        self.positive_child = None
        self.negative_child = None

def build_bsp(triangles):
    if not triangles:
        return None
        
    idx, first_tri = triangles[0]
    plane = make_plane(first_tri[0], first_tri[1], first_tri[2])
    if plane is None:
        return build_bsp(triangles[1:])
        
    node = Node()
    node.plane = plane
    node.triangles = [(idx, first_tri)]
    
    pos_tris = []
    neg_tris = []
    
    for i in range(1, len(triangles)):
        tri_idx, tri = triangles[i]
        classif = classify_triangle(plane, tri)
        if classif == "COPLANAR":
            node.triangles.append((tri_idx, tri))
        elif classif == "POSITIVE":
            pos_tris.append((tri_idx, tri))
        elif classif == "NEGATIVE":
            neg_tris.append((tri_idx, tri))
        elif classif == "CROSSING":
            parts = split_triangle(tri, plane)
            for part in parts:
                part_class = classify_triangle(plane, part)
                if part_class == "COPLANAR":
                    node.triangles.append((tri_idx, part))
                elif part_class == "POSITIVE":
                    pos_tris.append((tri_idx, part))
                elif part_class == "NEGATIVE":
                    neg_tris.append((tri_idx, part))
    
    node.positive_child = build_bsp(pos_tris)
    node.negative_child = build_bsp(neg_tris)
    return node

def traverse_bsp(segment, node, result_set):
    if node is None:
        return
        
    for tri_idx, tri in node.triangles:
        if intersect_segment_triangle(segment, tri):
            result_set.add(tri_idx)
            
    p0 = (segment[0], segment[1], segment[2])
    p1 = (segment[3], segment[4], segment[5])
    side0 = classify_point(node.plane, p0)
    side1 = classify_point(node.plane, p1)
    
    if side0 in ["POSITIVE", "COPLANAR"] and side1 in ["POSITIVE", "COPLANAR"]:
        traverse_bsp(segment, node.positive_child, result_set)
    elif side0 in ["NEGATIVE", "COPLANAR"] and side1 in ["NEGATIVE", "COPLANAR"]:
        traverse_bsp(segment, node.negative_child, result_set)
    else:
        traverse_bsp(segment, node.positive_child, result_set)
        traverse_bsp(segment, node.negative_child, result_set)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
        
    n = int(data[0])
    t = int(data[1])
    l = int(data[2])
    index = 3
    
    points = []
    for i in range(n):
        x = int(data[index]); y = int(data[index+1]); z = int(data[index+2])
        index += 3
        points.append((x, y, z))
        
    triangles = []
    for i in range(t):
        i1 = int(data[index]); i2 = int(data[index+1]); i3 = int(data[index+2])
        index += 3
        p1 = points[i1-1]
        p2 = points[i2-1]
        p3 = points[i3-1]
        triangles.append((i+1, [p1, p2, p3]))
        
    segments = []
    for i in range(l):
        x1 = int(data[index]); y1 = int(data[index+1]); z1 = int(data[index+2])
        x2 = int(data[index+3]); y2 = int(data[index+4]); z2 = int(data[index+5])
        index += 6
        segments.append((x1, y1, z1, x2, y2, z2))
        
    if triangles:
        bsp_tree = build_bsp(triangles)
    else:
        bsp_tree = None
        
    for seg in segments:
        result_set = set()
        if bsp_tree is not None:
            traverse_bsp(seg, bsp_tree, result_set)
        sorted_list = sorted(result_set)
        print(f"{len(sorted_list)} " + " ".join(map(str, sorted_list)))
        
if __name__ == "__main__":
    main()