import sys
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

def carregar_fecho_convexo(path_arquivo):
    """
    Lê um arquivo de texto no formato:
      k
      x1 y1 z1
      ...
      xk yk zk
      m
      V1 V2 V3  T1 T2 T3
      ...
      (m linhas de triangulações)
    
    Retorna uma tupla (vertices, faces), onde:
      - vertices é uma lista de tuplas (x, y, z)
      - faces é uma lista de triplas de índices (v0, v1, v2), cada índice
        referindo-se a um vértice em 'vertices'
    """
    vertices = []
    faces = []
    
    with open(path_arquivo, 'r') as f:
        # 1) lê k
        k_line = f.readline().strip()
        if not k_line:
            raise ValueError("Arquivo vazio ou formato inválido.")
        k = int(k_line)
        
        # 2) lê k linhas de vértices
        for _ in range(k):
            linha = f.readline().strip()
            if not linha:
                raise ValueError("Esperava coordenadas de vértice, mas encontrou linha vazia.")
            x, y, z = map(float, linha.split())
            vertices.append((x, y, z))
        
        # 3) lê m (número de triângulos)
        m_line = f.readline().strip()
        if not m_line:
            raise ValueError("Esperava número de triângulos, mas encontrou linha vazia.")
        m = int(m_line)
        
        # 4) lê m linhas de triângulos (cada uma tem 6 inteiros, mas só precisamos dos 3 primeiros)
        for _ in range(m):
            linha = f.readline().strip()
            if not linha:
                raise ValueError("Esperava dados do triângulo, mas encontrou linha vazia.")
            # cada linha: V1 V2 V3  T1 T2 T3
            nums = list(map(int, linha.split()))
            if len(nums) < 3:
                raise ValueError("Linha de triângulo com menos de 3 índices.")
            v0, v1, v2 = nums[0], nums[1], nums[2]
            # ajustar índices se a formulação estiver em base 1:
            # se for base-1, use v0-1, v1-1, v2-1. Caso contrário, comente as linhas abaixo.
            # Exemplo: no seu exemplo de saída, parece que os vértices já vêm em base 1,
            # então subtraímos 1 para usar em Python (base 0).
            v0 -= 1
            v1 -= 1
            v2 -= 1
            
            faces.append((v0, v1, v2))
    
    return vertices, faces


def plotar_fecho_convexo(vertices, faces):
    """
    Recebe:
      - vertices: lista de (x, y, z)
      - faces: lista de tuplos (i, j, k), índices em 'vertices'
    
    Plota o fecho convexo em 3D, desenhando cada face triangular.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Monta uma lista de polígonos, em que cada polígono é uma lista de
    # coordenadas [(x0,y0,z0), (x1,y1,z1), (x2,y2,z2)] 
    meshes = []
    for (i, j, k) in faces:
        try:
            p0 = vertices[i]
            p1 = vertices[j]
            p2 = vertices[k]
        except IndexError:
            raise IndexError(f"Índice de vértice fora do intervalo: {(i,j,k)}")
        meshes.append([p0, p1, p2])
    
    # Cria a coleção de polígonos
    poly3d = Poly3DCollection(meshes, facecolors='cyan', edgecolors='black', alpha=0.5)
    ax.add_collection3d(poly3d)
    
    # Ajusta os limites dos eixos para caber todo o fecho convexo
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]
    
    # Calcula centro e intervalo a partir dos valores mínimos e máximos
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)
    mid_x = (max_x + min_x) / 2.0
    mid_y = (max_y + min_y) / 2.0
    mid_z = (max_z + min_z) / 2.0
    max_range = max(max_x - min_x, max_y - min_y, max_z - min_z) / 2.0
    
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Fecho Convexo em 3D')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Exemplo de uso:
    # Suponha que sua função write_output gravou o resultado em "hull_output.txt".
    # Basta chamar:
    #
    #    python plot_convex_hull.py hull_output.txt
    #
    if len(sys.argv) < 2:
        print("Uso: python plot_convex_hull.py <caminho_para_saida_do_fecho_convexo>")
        sys.exit(1)
    
    arquivo_saida = sys.argv[1]
    vertices, faces = carregar_fecho_convexo(arquivo_saida)
    plotar_fecho_convexo(vertices, faces)
