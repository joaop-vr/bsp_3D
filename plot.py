import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import sys
import matplotlib as mpl
from matplotlib.lines import Line2D
import os

def plot_input_with_legend(input_file, output_dir):
    # Ler o arquivo de entrada
    with open(input_file, 'r') as f:
        data = f.read().split()
    
    if not data:
        print("Arquivo vazio")
        return
        
    n = int(data[0])
    t = int(data[1])
    l = int(data[2])
    index = 3
    
    # Ler pontos
    points = []
    for i in range(n):
        x = int(data[index]); y = int(data[index+1]); z = int(data[index+2])
        index += 3
        points.append((x, y, z))
    
    # Ler triângulos (índices)
    triangles = []
    for i in range(t):
        i1 = int(data[index]); i2 = int(data[index+1]); i3 = int(data[index+2])
        index += 3
        triangles.append((i1, i2, i3))
    
    # Ler segmentos
    segments = []
    for i in range(l):
        coords = list(map(int, data[index:index+6]))
        index += 6
        segments.append(coords)
    
    # Criar figura 3D
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Configurar título e eixos
    ax.set_title(f"Cena de Entrada: {n} pontos, {t} triângulos, {l} segmentos", fontsize=14)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 100)
    
    # Plotar pontos
    xs, ys, zs = zip(*points)
    ax.scatter(xs, ys, zs, c='black', s=20, alpha=0.6, label='Pontos')
    
    # Plotar triângulos
    for i, tri in enumerate(triangles):
        verts = [points[idx-1] for idx in tri]
        poly = Poly3DCollection([verts], alpha=0.3)
        poly.set_facecolor('lightblue')
        poly.set_edgecolor('black')
        ax.add_collection3d(poly)
        
        # Adicionar rótulo do triângulo
        centroid = np.mean(verts, axis=0)
        ax.text(centroid[0], centroid[1], centroid[2], f'T{i+1}', fontsize=9, ha='center')
    
    # Gerar paleta de cores para os segmentos
    colors = plt.cm.tab10(np.linspace(0, 1, min(l, 10)))
    if l > 10:
        colors = plt.cm.tab20(np.linspace(0, 1, l))
    
    # Plotar segmentos
    for i, seg in enumerate(segments):
        x = [seg[0], seg[3]]
        y = [seg[1], seg[4]]
        z = [seg[2], seg[5]]
        
        color = colors[i % len(colors)]
        ax.plot(x, y, z, color=color, linewidth=2.5, marker='o', markersize=6, 
                label=f'S{i+1}')
        
        # Adicionar rótulo do segmento
        mid_point = [(seg[0]+seg[3])/2, (seg[1]+seg[4])/2, (seg[2]+seg[5])/2]
        ax.text(mid_point[0], mid_point[1], mid_point[2], 
                f'S{i+1}', color='black', fontsize=10, weight='bold',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))
    
    # Criar legenda personalizada
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
               markersize=8, label='Pontos'),
        mpl.patches.Patch(facecolor='lightblue', edgecolor='black',
                          alpha=0.3, label='Triângulos')
    ]
    
    for i in range(l):
        color = colors[i % len(colors)]
        label = f'S{i+1} ({segments[i][0]},{segments[i][1]},{segments[i][2]})→({segments[i][3]},{segments[i][4]},{segments[i][5]})'
        legend_elements.append(Line2D([0], [0], color=color, lw=2, label=label))
    
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1), 
              title="Legenda", fontsize=10, title_fontsize=12)
    
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.subplots_adjust(right=0.8)

    # Gerar nome do arquivo de saída limpo
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_path = os.path.join(output_dir, f"{base_name}_plot.png")
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    #plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 plot.py <input_file> <output_dir>")
        print("Exemplo: python3 plot.py entrada.txt saida/")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    plot_input_with_legend(input_file, output_dir)
