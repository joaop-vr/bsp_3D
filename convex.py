import sys
from typing import List, Optional, Tuple

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
    Obs.: Os vértices são armazenados em ordem horária (visto de fora) com V1 sendo o menor índice.
    """
    __slots__ = ('verts', 'neighbors')

    def __init__(self, verts: Tuple[int, int, int], points: List[Point3D]):
        # Ordena os vértices.
        sorted_verts = sorted(verts)
        v1, v2, v3 = sorted_verts[0], sorted_verts[1], sorted_verts[2]

        # Verifica a orientação dos vértices, garantindo ordem horária (normal apontando para fora).
        normal = self._compute_normal(points[v1], points[v2], points[v3])
        if not self._is_clockwise(points[v1], points[v2], points[v3], normal):
            v2, v3 = v3, v2  # Inverte a ordem para corrigir a orientação

        self.verts = (v1, v2, v3)
        self.neighbors: List[Optional['TriangleFace']] = [None, None, None]

    def _compute_normal(self, p1: Point3D, p2: Point3D, p3: Point3D) -> Point3D:
        """Calcula a normal do triângulo usando o produto vetorial."""
        vec1 = Point3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
        vec2 = Point3D(p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
        normal = Point3D(vec1.y * vec2.z - vec1.z * vec2.y, vec1.z * vec2.x - vec1.x * vec2.z, vec1.x * vec2.y - vec1.y * vec2.x)
        return normal

    def _is_clockwise(self, p1: Point3D, p2: Point3D, p3: Point3D, normal: Point3D) -> bool:
        """
        Verifica se os pontos estão em ordem horária (visto de fora do casco).
        Assume que a normal aponta para fora.
        """
        # Para simplificar, assume-se que o casco é construído de forma que a normal calculada
        # aponta para fora. Se o produto escalar entre a normal e um vetor arbitrário (ex: (0,0,0) -> p1)
        # for positivo, a ordem está correta.
        centroid = Point3D(
            (p1.x + p2.x + p3.x) / 3,
            (p1.y + p2.y + p3.y) / 3,
            (p1.z + p2.z + p3.z) / 3
        )
        vector_to_centroid = Point3D(centroid.x, centroid.y, centroid.z)  # Vetor arbitrário
        dot_product = (normal.x * vector_to_centroid.x + normal.y * vector_to_centroid.y + normal.z * vector_to_centroid.z)
        return dot_product > 0  # Se positivo, ordem horária está correta.

    def set_neighbor(self, local_edge_idx: int, neighbor: Optional['TriangleFace']):
        self.neighbors[local_edge_idx] = neighbor

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

    def compute(self):
        """Constrói a lista de TriangleFace e para cada face preenche os vizinhos."""

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
        

if __name__ == "__main__":
    hull = ConvexHull3D()
    hull.read_input()
    hull.compute()
    hull.write_output()
