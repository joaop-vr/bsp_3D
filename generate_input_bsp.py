import random
import sys

def generate_input(n, t, l, filename):
    with open(filename, 'w') as f:
        f.write(f"{n} {t} {l}\n")
        
        # Gerar pontos aleatórios
        points = []
        for _ in range(n):
            x = random.randint(1, 99)
            y = random.randint(1, 99)
            z = random.randint(1, 99)
            points.append((x, y, z))
            f.write(f"{x} {y} {z}\n")
        
        # Gerar triângulos (garantir índices válidos)
        for _ in range(t):
            idx1, idx2, idx3 = random.sample(range(1, n+1), 3)
            f.write(f"{idx1} {idx2} {idx3}\n")
        
        # Gerar segmentos aleatórios
        for _ in range(l):
            x1 = random.randint(1, 99)
            y1 = random.randint(1, 99)
            z1 = random.randint(1, 99)
            x2 = random.randint(1, 99)
            y2 = random.randint(1, 99)
            z2 = random.randint(1, 99)
            f.write(f"{x1} {y1} {z1} {x2} {y2} {z2}\n")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python generate_bsp.py <n_points> <n_triangles> <n_segments> <output_file>")
        sys.exit(1)
    
    n = int(sys.argv[1])
    t = int(sys.argv[2])
    l = int(sys.argv[3])
    filename = sys.argv[4]
    
    generate_input(n, t, l, filename)
    print(f"Arquivo {filename} gerado com {n} pontos, {t} triângulos e {l} segmentos")