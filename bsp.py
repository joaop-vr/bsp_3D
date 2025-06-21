#!/usr/bin/env python3
import sys

class Node:
    __slots__ = ('plane', 'triangles', 'positive_child', 'negative_child')
    def __init__(self):
        self.plane = None
        self.triangles = []
        self.positive_child = None
        self.negative_child = None

def cross_product(u, v):
    """
    Retorna: vetor resultante do produto vetorial u x v, na forma (x, y, z).
    """
    return (u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0])

def dot_product(u, v):
    """
    Retorna: resultado do produto escalar u · v.
    """
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

def vector_subtract(u, v):
    """
    Retorna: vetor resultante da subtração u - v.
    """
    return (u[0]-v[0], u[1]-v[1], u[2]-v[2])

def make_plane(p0, p1, p2):
    """
    Cria a representação de um plano a partir de três pontos.

    Parâmetros:
    p0, p1, p2: Pontos no espaço (x, y, z) definindo o plano.

    Retorna: os coeficientes (a, b, c, d) da equação do plano ax + by + cz + d = 0,
    ou None se os pontos forem colineares.
    """
    # Vetores no plano a partir de p0
    v1 = vector_subtract(p1, p0)
    v2 = vector_subtract(p2, p0)
    
    normal = cross_product(v1, v2)
    # Se a normal for (quase) zero, os pontos são colineares
    if all(abs(coord) < 1e-10 for coord in normal):
        return None
    # Constante d na equação do plano: d = -n · p0
    d = -dot_product(normal, p0)
    return (normal[0], normal[1], normal[2], d)

def classify_point(plane, point, tol=1e-10):
    """
    Classifica um ponto em relação a um plano.

    Parâmetros:
    plane: Coeficientes (a, b, c, d) do plano ax + by + cz + d = 0.
    point: Coordenadas do ponto (x, y, z).
    tol: Tolerância para considerar ponto como coplanar.

    Retorna: "COPLANAR" se |ax+by+cz+d| < tol,
             "POSITIVE" se ax+by+cz+d > tol,
             "NEGATIVE" se ax+by+cz+d < -tol.
    """
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
    """
    Classifica um triângulo inteiro em relação a um plano.

    Parâmetros:
    plane: Coeficientes (a, b, c, d) do plano.
    triangle: Lista de três vértices [(x1,y1,z1), (x2,y2,z2), (x3,y3,z3)].

    Retorna: "COPLANAR" (todos os vértices coplanares),
             "POSITIVE" (todos os vértices no lado positivo),
             "NEGATIVE" (todos no lado negativo),
             "CROSSING" (vértices de ambos os lados).
    """
    # Classifica cada vértice
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
    """
    Calcula o ponto de interseção entre uma aresta e um plano.

    Parâmetros:
    p: Primeiro ponto da aresta (x, y, z).
    q: Segundo ponto da aresta (x, y, z).
    plane: Coeficientes (a, b, c, d) do plano ax + by + cz + d = 0.

    Retorna: o ponto de interseção (x, y, z). Se a aresta for quase paralela ao plano,
    retorna o ponto p.
    """
    a, b, c, d = plane
    num = -(a*p[0] + b*p[1] + c*p[2] + d)
    denom = a*(q[0]-p[0]) + b*(q[1]-p[1]) + c*(q[2]-p[2])
    # Se denom próximo de 0, considere paralelo e retorna p
    if abs(denom) < 1e-10:
        return p
    # Parâmetro t da interseção ao longo do seg pq
    t = num / denom
    # Calcula coordenadas do ponto de interseção
    x = p[0] + t*(q[0]-p[0])
    y = p[1] + t*(q[1]-p[1])
    z = p[2] + t*(q[2]-p[2])
    return (x, y, z)

def split_triangle(triangle, plane):
    """
    Divide um triângulo em sub-triângulos de acordo com sua interseção com um plano.

    Parâmetros:
    triangle: Lista de três vértices [(x,y,z), ...].
    plane : Coeficientes (a, b, c, d) do plano.

    Retorna: o sub-conjunto de triângulos resultantes da divisão.
    """
    pts = triangle
    # Classifica cada vértice em relação ao plano
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
        return [[P, I1, I2],[N1, I1, I2],[N1, I2, N2]]
    elif len(positive_pts) == 2 and len(negative_pts) == 1:
        N = negative_pts[0]
        P1, P2 = positive_pts
        I1 = intersect_edge_plane(N, P1, plane)
        I2 = intersect_edge_plane(N, P2, plane)
        return [[N, I1, I2],[I1, P1, I2],[I1, I2, P2]]
    elif len(positive_pts) == 1 and len(negative_pts) == 1 and len(coplanar_pts) == 1:
        P = positive_pts[0]
        N = negative_pts[0]
        C = coplanar_pts[0]
        I = intersect_edge_plane(P, N, plane)
        return [[P, C, I], [N, C, I]]
    # Não cruza ou todos coplanares
    else:
        return [triangle]

def point_in_triangle(P, triangle):
    """
    Verifica se um ponto P está dentro de um triângulo.

    Parâmetros:
    P: Ponto a testar (x, y, z).
    triangle : Vértices do triângulo.

    Retorna: True se P estiver dentro (ou no limite) do triângulo; False caso contrário.
    """
    A, B, C = triangle
    # Calcula vetor normal do triângulo (n)
    AB = vector_subtract(B, A)
    AC = vector_subtract(C, A)
    n = cross_product(AB, AC)
    
    # Vetores de P para cada vértice
    PA = vector_subtract(A, P)
    PB = vector_subtract(B, P)
    PC = vector_subtract(C, P)
    
    n1 = cross_product(PB, PC)
    n2 = cross_product(PC, PA)
    n3 = cross_product(PA, PB)
    
    d1 = dot_product(n1, n)
    d2 = dot_product(n2, n)
    d3 = dot_product(n3, n)
    
    # Se todos os produtos escalar têm mesmo sinal, P está dentro
    if (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0):
        return True
    return False

def point_on_segment(P, seg):
    """
    Verifica se um ponto P está sobre um segmento de reta.
    Retorna:
    bool: True se P estiver colinear e entre A e B, False caso contrário.
    """
    A = (seg[0], seg[1], seg[2])
    B = (seg[3], seg[4], seg[5])
    AP = vector_subtract(P, A)
    AB = vector_subtract(B, A)
    crossAP_AB = cross_product(AP, AB)
    # testa colinearidade via produto vetorial
    if abs(crossAP_AB[0]) > 1e-10 or abs(crossAP_AB[1]) > 1e-10 or abs(crossAP_AB[2]) > 1e-10:
        return False
    # verifica se P está entre A e B via produto escalar
    PB = vector_subtract(P, B)
    return dot_product(AP, PB) <= 1e-10

def segments_intersect_2d(s1_p1, s1_p2, s2_p1, s2_p2):
    """
    Testa interseção entre dois segmentos em 2D.

    Parâmetros:
    s1_p1,s1_p2,s2_p1,s2_p2: Pontos finais dos segmentos (x,y).

    Retorna: True se segmentos se cruzam ou tocam.
    """
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def sign(x):
        return 1 if x > 1e-10 else -1 if x < -1e-10 else 0
        
    def on_segment(a, b, c):
        return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and 
                min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))
    
    d1 = cross(s1_p1, s1_p2, s2_p1)
    d2 = cross(s1_p1, s1_p2, s2_p2)
    d3 = cross(s2_p1, s2_p2, s1_p1)
    d4 = cross(s2_p1, s2_p2, s1_p2)
    if sign(d1) * sign(d2) < 0 and sign(d3) * sign(d4) < 0: return True
    if abs(d1) < 1e-10 and on_segment(s1_p1, s1_p2, s2_p1): return True
    if abs(d2) < 1e-10 and on_segment(s1_p1, s1_p2, s2_p2): return True
    if abs(d3) < 1e-10 and on_segment(s2_p1, s2_p2, s1_p1): return True
    if abs(d4) < 1e-10 and on_segment(s2_p1, s2_p2, s1_p2): return True
        
    return False

def intersect_segment_triangle(segment, triangle):
    """
    Verifica se um segmento intersecta um triângulo.

    Parâmetros:
    segment: Coordenadas (x1,y1,z1,x2,y2,z2) do segmento.
    triangle: Vértices do triângulo.

    Retorna: True se houver interseção, False caso contrário.
    """
    p0 = (segment[0], segment[1], segment[2])
    p1 = (segment[3], segment[4], segment[5])
    A, B, C = triangle
    plane = make_plane(A, B, C)
    if plane is None:
        return False
    a, b, c, d = plane
    
    dir_vec = [p1[i] - p0[i] for i in range(3)]
    denom = a*dir_vec[0] + b*dir_vec[1] + c*dir_vec[2]
    
    # caso paralelo
    if abs(denom) < 1e-10:
        coplanar0 = classify_point(plane, p0) == "COPLANAR"
        coplanar1 = classify_point(plane, p1) == "COPLANAR"
        
        # Verifica pontos finais dentro do triângulo
        if coplanar0 and point_in_triangle(p0, triangle):
            return True
        if coplanar1 and point_in_triangle(p1, triangle):
            return True
            
        # Verifica vértices do triângulo no segmento
        for Q in triangle:
            if point_on_segment(Q, segment):
                return True
        
        # Só faz projeção se o segmento estiver no plano
        if coplanar0 and coplanar1:
            normal = plane[:3]
            abs_normal = [abs(normal[0]), abs(normal[1]), abs(normal[2])]
            axis = abs_normal.index(max(abs_normal))
            
            def project(pt):
                if axis == 0:
                    return (pt[1], pt[2])
                elif axis == 1:
                    return (pt[0], pt[2])
                else:
                    return (pt[0], pt[1])
                    
            seg_proj = [project(p0), project(p1)]
            tri_proj = [project(A), project(B), project(C)]
            
            edges = [(tri_proj[0], tri_proj[1]), (tri_proj[1], tri_proj[2]), (tri_proj[2], tri_proj[0])]
            
            for edge in edges:
                if segments_intersect_2d(seg_proj[0], seg_proj[1], edge[0], edge[1]):
                    return True
                    
        return False
    
    # Caso não paralelo
    t = -(a*p0[0] + b*p0[1] + c*p0[2] + d) / denom
    if t < 0.0 or t > 1.0:
        return False
    
    x = p0[0] + t * dir_vec[0]
    y = p0[1] + t * dir_vec[1]
    z = p0[2] + t * dir_vec[2]
    P = (x, y, z)
    
    return point_in_triangle(P, triangle)

def build_bsp(triangles):
    """
    Constrói recursivamente uma árvore BSP a partir de uma lista de triângulos.

    Retorna: O nó raiz da BSP ou None se não houver triângulos.
    """
    if not triangles:
        return None
    
    # Seleciona o primeiro triângulo para definir o plano de divisão
    idx, first_tri = triangles[0]
    plane = make_plane(first_tri[0], first_tri[1], first_tri[2])
    if plane is None:
        return build_bsp(triangles[1:])
        
    node = Node()
    node.plane = plane
    node.triangles = [(idx, first_tri)]
    pos_tris = []
    neg_tris = []
    
    # Distribui os triângulos restantes
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
    # Cria subárvores positiva e negativa
    node.positive_child = build_bsp(pos_tris)
    node.negative_child = build_bsp(neg_tris)
    return node

def traverse_bsp(segment, node, result_set):
    """
    Percorre a BSP para encontrar triângulos interceptados por um segmento.

    Parâmetros:
    segment: Segmento definido por 6 coordenadas.
    node: Nó atual da BSP.
    result_set: Conjunto para coletar índices de triângulos interceptados.

    Retorna: Os resultados são adicionados em result_set.
    """
    if node is None:
        return
    # Testa todos os triângulos coplanares ao plano deste nó
    for tri_idx, tri in node.triangles:
        if intersect_segment_triangle(segment, tri):
            result_set.add(tri_idx)
    # Classifica as extremidades do segmento
    p0 = (segment[0], segment[1], segment[2])
    p1 = (segment[3], segment[4], segment[5])
    side0 = classify_point(node.plane, p0)
    side1 = classify_point(node.plane, p1)
    # Decide qual sub-árvore visitar
    if side0 in ["POSITIVE", "COPLANAR"] and side1 in ["POSITIVE", "COPLANAR"]:
        traverse_bsp(segment, node.positive_child, result_set)
    elif side0 in ["NEGATIVE", "COPLANAR"] and side1 in ["NEGATIVE", "COPLANAR"]:
        traverse_bsp(segment, node.negative_child, result_set)
    else:
        # Segmento cruza o plano, explora ambas as subárvores
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