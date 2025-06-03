import sys
from typing import List, Optional, Tuple, Set, Dict

class Point3D:
    """Representa um ponto em ℝ³."""
    __slots__ = ('x','y','z')
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def __repr__(self): # mostra o ponto bonitinho ao imprimir
        return f"Point3D({self.x}, {self.y}, {self.z})"


class TriangleFace:
    """
    Representa um triângulo da malha do casco convexo.
    - verts: tupla de índices (i, j, k)
    - neighbors: lista de 3 referências (ou None) a outros TriangleFace vizinhos
    Obs.: Os vértices são armazenados em ordem horária (visto de fora).
    """
    __slots__ = ('verts', 'neighbors')

    def __init__(self, verts: Tuple[int, int, int]):
        self.verts = verts
        self.neighbors: List[Optional['TriangleFace']] = [None, None, None]

    @staticmethod
    def _compute_normal(p1: Point3D, p2: Point3D, p3: Point3D) -> Point3D:
        """Calcula a normal do triângulo usando o produto vetorial."""
        vec1 = Point3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
        vec2 = Point3D(p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
        normal = Point3D(
            vec1.y * vec2.z - vec1.z * vec2.y,
            vec1.z * vec2.x - vec1.x * vec2.z,
            vec1.x * vec2.y - vec1.y * vec2.x
        )
        return normal

    def __repr__(self):
        return f"Tri{self.verts} neighbors={[n.verts if n else None for n in self.neighbors]}"


class ConvexHull3D:
    """
    Classe principal para:
      - ler entrada
      - executar algoritmo de fecho convexo
      - gerar saída no formato de triangulação
    """
    def __init__(self):
        self.points: List[Point3D] = []
        self.faces: List[TriangleFace] = []

    def read_input(self, f=sys.stdin):
        """Lê o conjunto de pontos."""
        n = int(f.readline().strip())
        for _ in range(n):
            x,y,z = map(int, f.readline().split())
            self.points.append(Point3D(x,y,z))

    def is_visible(self, face: TriangleFace, point: Point3D) -> bool:
        """Determina se um ponto é visível a partir de uma face (está fora do casco)."""
        p0 = self.points[face.verts[0]]
        p1 = self.points[face.verts[1]]
        p2 = self.points[face.verts[2]]
        normal = TriangleFace._compute_normal(p0, p1, p2)
        vec = Point3D(point.x - p0.x, point.y - p0.y, point.z - p0.z)
        dot = normal.x * vec.x + normal.y * vec.y + normal.z * vec.z
        return dot > 1e-7  # Tolerância para evitar problemas numéricos

    def compute(self):
        """Constrói a lista de TriangleFace e preenche os vizinhos para cada face."""
        n = len(self.points)
        if n < 4:
            # Casos com menos de 4 pontos não formam um volume 3D
            return

        # Passo 1: Encontrar 4 pontos não coplanares para formar o tetraedro inicial
        # P0: primeiro ponto
        p0 = self.points[0]
        
        # P1: ponto mais distante de P0
        max_dist = -1
        i1 = -1
        for i in range(1, n):
            dist = (self.points[i].x - p0.x)**2 + (self.points[i].y - p0.y)**2 + (self.points[i].z - p0.z)**2
            if dist > max_dist:
                max_dist = dist
                i1 = i
        
        if i1 == -1:
            return  # Todos os pontos são iguais
        
        # P2: ponto mais distante da linha P0-P1
        line_dir = Point3D(
            self.points[i1].x - p0.x,
            self.points[i1].y - p0.y,
            self.points[i1].z - p0.z
        )
        max_dist = -1
        i2 = -1
        for i in range(1, n):
            if i == i1:
                continue
            vec = Point3D(
                self.points[i].x - p0.x,
                self.points[i].y - p0.y,
                self.points[i].z - p0.z
            )
            # Produto vetorial: line_dir × vec
            cross = Point3D(
                line_dir.y * vec.z - line_dir.z * vec.y,
                line_dir.z * vec.x - line_dir.x * vec.z,
                line_dir.x * vec.y - line_dir.y * vec.x
            )
            dist = cross.x**2 + cross.y**2 + cross.z**2
            if dist > max_dist:
                max_dist = dist
                i2 = i
        
        if i2 == -1:
            return  # Todos os pontos são colineares
        
        # P3: ponto mais distante do plano P0-P1-P2 (com sinal)
        p1 = self.points[i1]
        p2_val = self.points[i2]
        vec1 = Point3D(p1.x - p0.x, p1.y - p0.y, p1.z - p0.z)
        vec2 = Point3D(p2_val.x - p0.x, p2_val.y - p0.y, p2_val.z - p0.z)
        base_normal = Point3D(
            vec1.y * vec2.z - vec1.z * vec2.y,
            vec1.z * vec2.x - vec1.x * vec2.z,
            vec1.x * vec2.y - vec1.y * vec2.x
        )
        max_dist = -1
        i3 = -1
        for i in range(n):
            if i == 0 or i == i1 or i == i2:
                continue
            vec3 = Point3D(
                self.points[i].x - p0.x,
                self.points[i].y - p0.y,
                self.points[i].z - p0.z
            )
            volume = base_normal.x * vec3.x + base_normal.y * vec3.y + base_normal.z * vec3.z
            if abs(volume) > max_dist:
                max_dist = abs(volume)
                i3 = i
        
        if i3 == -1:
            return  # Todos os pontos são coplanares

        # Criar as 4 faces do tetraedro inicial
        indices = [0, i1, i2, i3]
        
        def create_face(a: int, b: int, c: int, fourth: int) -> TriangleFace:
            """Cria uma face ajustando a orientação para fora."""
            p_a = self.points[a]
            p_b = self.points[b]
            p_c = self.points[c]
            normal = TriangleFace._compute_normal(p_a, p_b, p_c)
            vec_fourth = Point3D(
                self.points[fourth].x - p_a.x,
                self.points[fourth].y - p_a.y,
                self.points[fourth].z - p_a.z
            )
            dot = normal.x * vec_fourth.x + normal.y * vec_fourth.y + normal.z * vec_fourth.z
            if dot > 0:
                return TriangleFace((c, b, a))  # Inverte para normal apontar para fora
            else:
                return TriangleFace((a, b, c))
        
        # Faces do tetraedro
        face0 = create_face(0, i1, i2, i3)
        face1 = create_face(0, i1, i3, i2)
        face2 = create_face(0, i2, i3, i1)
        face3 = create_face(i1, i2, i3, 0)
        tetra_faces = [face0, face1, face2, face3]
        self.faces = tetra_faces

        # Conectar as faces do tetraedro
        edge_map = {}
        for idx, face in enumerate(tetra_faces):
            for edge_idx in range(3):
                u = face.verts[edge_idx]
                v = face.verts[(edge_idx+1) % 3]
                key = (min(u, v), max(u, v))
                if key not in edge_map:
                    edge_map[key] = []
                edge_map[key].append((idx, edge_idx))
        
        for key, faces_list in edge_map.items():
            if len(faces_list) == 2:
                idx1, edge_idx1 = faces_list[0]
                idx2, edge_idx2 = faces_list[1]
                face1 = tetra_faces[idx1]
                face2 = tetra_faces[idx2]
                face1.neighbors[edge_idx1] = face2
                face2.neighbors[edge_idx2] = face1

        # Processar os pontos restantes incrementalmente
        remaining = set(range(n)) - set(indices)
        for idx in remaining:
            point = self.points[idx]
            visible = [face for face in self.faces if self.is_visible(face, point)]
            if not visible:
                continue

            # Encontrar arestas do horizonte
            visible_set = set(visible)
            horizon_edges = []  # (a, b, face_vis, neighbor_face, edge_idx)
            for face in visible:
                for edge_idx in range(3):
                    neighbor = face.neighbors[edge_idx]
                    if neighbor is None or neighbor not in visible_set:
                        a = face.verts[(edge_idx+1) % 3]
                        b = face.verts[(edge_idx+2) % 3]
                        horizon_edges.append((a, b, face, neighbor, edge_idx))

            # Criar novas faces
            new_faces = []
            for a, b, face_vis, neighbor_face, edge_idx in horizon_edges:
                # Nova face com orientação correta (b, a, idx)
                new_face = TriangleFace((b, a, idx))
                new_face.neighbors[2] = neighbor_face  # Aresta do horizonte
                
                # Atualizar vizinho antigo
                if neighbor_face is not None:
                    for i in range(3):
                        if neighbor_face.neighbors[i] == face_vis:
                            neighbor_face.neighbors[i] = new_face
                            break
                new_faces.append(new_face)
            
            # Conectar novas faces entre si
            edge_map_new = {}
            for new_face in new_faces:
                for local_idx in [0, 1]:  # Arestas não-horizonte
                    u = new_face.verts[(local_idx+1) % 3]
                    v = new_face.verts[(local_idx+2) % 3]
                    key = (min(u, v), max(u, v))
                    edge_map_new[key] = (new_face, local_idx)
            
            for new_face in new_faces:
                for local_idx in [0, 1]:
                    u = new_face.verts[(local_idx+1) % 3]
                    v = new_face.verts[(local_idx+2) % 3]
                    key = (min(u, v), max(u, v))
                    if key in edge_map_new:
                        other_face, other_idx = edge_map_new[key]
                        if other_face != new_face:
                            new_face.neighbors[local_idx] = other_face
                            other_face.neighbors[other_idx] = new_face
            
            # Atualizar estrutura global
            self.faces.extend(new_faces)
            for face in visible:
                self.faces.remove(face)

    def write_output(self, f=sys.stdout):
        """
        Escreve na saída padrão:
          k
          x1 y1 z1
          ...
          xm ym zm
          m
          V1 V2 V3  T1 T2 T3
        """
        # Coletar vértices únicos do casco
        vertex_indices = set()
        for face in self.faces:
            for v in face.verts:
                vertex_indices.add(v)
        sorted_vertices = sorted(vertex_indices)
        vertex_map = {old_idx: new_idx for new_idx, old_idx in enumerate(sorted_vertices)}
        
        # Escrever vértices
        f.write(f"{len(sorted_vertices)}\n")
        for idx in sorted_vertices:
            p = self.points[idx]
            f.write(f"{p.x} {p.y} {p.z}\n")
        
        # Mapear faces para índices
        face_index_map = {face: idx for idx, face in enumerate(self.faces)}
        
        # Escrever faces
        f.write(f"{len(self.faces)}\n")
        for face in self.faces:
            v0, v1, v2 = [vertex_map[v] for v in face.verts]
            n0 = face_index_map.get(face.neighbors[0], -1) if face.neighbors[0] is not None else -1
            n1 = face_index_map.get(face.neighbors[1], -1) if face.neighbors[1] is not None else -1
            n2 = face_index_map.get(face.neighbors[2], -1) if face.neighbors[2] is not None else -1
            f.write(f"{v0} {v1} {v2}  {n0} {n1} {n2}\n")
        

if __name__ == "__main__":
    hull = ConvexHull3D()
    hull.read_input()
    hull.compute()
    hull.write_output()