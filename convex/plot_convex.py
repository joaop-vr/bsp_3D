"""
plot_convex_with_input.py

Este script lê **um ou dois** arquivos:
  1. (Obrigatório) Arquivo de saída do fecho convexo (hull), no formato:
       k
       x1 y1 z1
       ...
       xk yk zk
       m
       V1 V2 V3  T1 T2 T3
       ...
  2. (Opcional) Arquivo de entrada de pontos originais, no formato:
       n
       x1 y1 z1
       ...
       xn yn zn

Se o segundo arquivo for fornecido, plota também todos os pontos originais (scatter cinza);
caso contrário, plota apenas o hull.

Uso:
    python plot_convex_with_input.py <arquivo_saida_hull> [<arquivo_entrada_pontos>]

Exemplo:
    # Apenas hull:
    python plot_convex_with_input.py hull_output.txt

    # Hull + pontos de entrada:
    python plot_convex_with_input.py hull_output.txt entrada_convex.txt
"""

import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def carregar_entrada_pontos(path_arquivo):
    """
    Lê um arquivo no formato:
      n
      x1 y1 z1
      ...
      xn yn zn
    Retorna uma lista de tuplas (x, y, z) com todos os pontos originais.
    """
    pontos = []
    with open(path_arquivo, 'r') as f:
        linha = f.readline().strip()
        if not linha:
            raise ValueError("Arquivo de entrada de pontos vazio ou formato inválido.")
        n = int(linha)
        for _ in range(n):
            l = f.readline().strip()
            if not l:
                raise ValueError("Esperava coordenadas de ponto, mas encontrou linha vazia.")
            x, y, z = map(float, l.split())
            pontos.append((x, y, z))
    return pontos

def carregar_fecho_convexo(path_arquivo):
    """
    Lê um arquivo de texto no formato de saída do fecho convexo:
      k
      x1 y1 z1
      ...
      xk yk zk
      m
      V1 V2 V3  T1 T2 T3
      ...
    Retorna (vertices_hull, faces), onde:
      - vertices_hull: lista de (x, y, z) dos vértices do hull
      - faces: lista de triplas (i, j, k) índices (base-0) em vertices_hull para formar cada triângulo
    """
    vertices = []
    faces = []
    
    with open(path_arquivo, 'r') as f:
        # 1) lê k (número de vértices do hull)
        k_line = f.readline().strip()
        if not k_line:
            raise ValueError("Arquivo de hull vazio ou formato inválido.")
        k = int(k_line)
        
        # 2) lê k linhas de vértices do hull
        for _ in range(k):
            linha = f.readline().strip()
            if not linha:
                raise ValueError("Esperava coordenadas de vértice do hull, mas encontrou linha vazia.")
            x, y, z = map(float, linha.split())
            vertices.append((x, y, z))
        
        # 3) lê m (número de triângulos do hull)
        m_line = f.readline().strip()
        if not m_line:
            raise ValueError("Esperava número de triângulos do hull, mas encontrou linha vazia.")
        m = int(m_line)
        
        # 4) lê m linhas de triângulos (cada uma tem 6 inteiros; usamos apenas V1,V2,V3)
        for _ in range(m):
            linha = f.readline().strip()
            if not linha:
                raise ValueError("Esperava dados do triângulo do hull, mas encontrou linha vazia.")
            nums = list(map(int, linha.split()))
            if len(nums) < 3:
                raise ValueError("Linha de triângulo com menos de 3 índices.")
            v0, v1, v2 = nums[0], nums[1], nums[2]
            # Ajusta para base 0
            v0 -= 1
            v1 -= 1
            v2 -= 1
            faces.append((v0, v1, v2))
    
    return vertices, faces

def plotar_hull(vertices_hull, faces, pontos_originais=None):
    """
    Plota o hull em 3D.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Se houver pontos originais, plota como scatter cinza
    if pontos_originais:
        xs_p = [p[0] for p in pontos_originais]
        ys_p = [p[1] for p in pontos_originais]
        zs_p = [p[2] for p in pontos_originais]
        ax.scatter(xs_p, ys_p, zs_p, color='red', s=50, label='Pontos Originais')
    
    # Monta as faces do hull
    meshes = []
    for (i, j, k) in faces:
        try:
            p0 = vertices_hull[i]
            p1 = vertices_hull[j]
            p2 = vertices_hull[k]
        except IndexError:
            raise IndexError(f"Índice de vértice do hull fora do intervalo: {(i, j, k)}")
        meshes.append([p0, p1, p2])
    
    # Plota as faces do hull em ciano translúcido
    poly3d = Poly3DCollection(meshes, facecolors='cyan', edgecolors='blue', alpha=0.5)
    ax.add_collection3d(poly3d)
    
    # Ajusta limites: combina vértices do hull e pontos originais (se houver)
    xs_h = [v[0] for v in vertices_hull]
    ys_h = [v[1] for v in vertices_hull]
    zs_h = [v[2] for v in vertices_hull]
    
    todos_x = xs_h[:]
    todos_y = ys_h[:]
    todos_z = zs_h[:]
    if pontos_originais:
        todos_x += [p[0] for p in pontos_originais]
        todos_y += [p[1] for p in pontos_originais]
        todos_z += [p[2] for p in pontos_originais]
    
    min_x, max_x = min(todos_x), max(todos_x)
    min_y, max_y = min(todos_y), max(todos_y)
    min_z, max_z = min(todos_z), max(todos_z)
    
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
    title = 'Fecho Convexo'
    if pontos_originais:
        title += ' + Pontos Originais'
        ax.legend()
    ax.set_title(title)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0 or len(args) > 2:
        print("Uso: python plot.py <arquivo_saida_hull> [<arquivo_entrada_pontos>]")
        sys.exit(1)
    
    arquivo_hull = args[0]
    arquivo_entrada = args[1] if len(args) == 2 else None
    
    # Carrega vértices e faces do hull (obrigatório)
    vertices_hull, faces = carregar_fecho_convexo(arquivo_hull)
    
    if arquivo_entrada:
        # Se fornecido, carrega pontos originais
        pontos = carregar_entrada_pontos(arquivo_entrada)
    else:
        pontos = None
    
    # Plota o hull e, se houver, os pontos originais
    plotar_hull(vertices_hull, faces, pontos)