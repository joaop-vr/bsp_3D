#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_convex_tests.py

Script para gerar entradas aleatórias de pontos em R3 para testar implementações de Fecho Convexo.
Gera coordenadas em intervalo [-coord_range..coord_range], com opções de duplicatas
e casos degenerados (coplanar ou colinear).

Formato de saída (stdin do seu programa 'convex'):
    n
    x1 y1 z1
    x2 y2 z2
    ...
    xn yn zn

Como usar:
    # Gera 20 pontos em [-99..99], sem duplicatas:
    $ python3 generate_inputs.py --n-points 20 > entrada_convex.txt

    # Gera 50 pontos, permite duplicatas:
    $ python3 generate_inputs.py --n-points 50 --allow-duplicates > entrada_convex_dup.txt

    # Gera 30 pontos, todos coplanares (z = 0):
    $ python3 generate_inputs.py --n-points 30 --force-coplanar > entrada_convex_coplanar.txt

    # Gera 25 pontos, todos colineares (x = y = z):
    $ python3 generate_inputs.py --n-points 25 --force-colinear > entrada_convex_colinear.txt

    # Ajusta o intervalo de coordenadas para [-50..50]:
    $ python3 generate_inputs.py --n-points 40 --coord-range 50 > entrada_convex_50.txt
"""

import sys
import random
import argparse


def generate_convex_input(n_points: int,
                          coord_range: int,
                          allow_duplicates: bool,
                          force_coplanar: bool,
                          force_colinear: bool):
    """
    Gera n_points pontos em R3 e imprime no formato:
        n
        x1 y1 z1
        x2 y2 z2
        ...
    Opções de caso degenerado (coplanaridade z=0 ou colinear x=y=z) e duplicatas.
    """
    pts = []
    seen = set()

    def random_point():
        return (
            random.randint(-coord_range, coord_range),
            random.randint(-coord_range, coord_range),
            random.randint(-coord_range, coord_range)
        )

    # Se ambos são True, sai com erro
    if force_coplanar and force_colinear:
        print("Erro: --force-coplanar e --force-colinear não podem ser usados juntos.", file=sys.stderr)
        sys.exit(1)

    # Gera pontos de acordo com flags
    if force_coplanar:
        # Todos no plano z=0
        while len(pts) < n_points:
            x = random.randint(-coord_range, coord_range)
            y = random.randint(-coord_range, coord_range)
            z = 0
            p = (x, y, z)
            if not allow_duplicates and p in seen:
                continue
            seen.add(p)
            pts.append(p)

    elif force_colinear:
        # Todos na reta x=y=z
        while len(pts) < n_points:
            t = random.randint(-coord_range, coord_range)
            p = (t, t, t)
            if not allow_duplicates and p in seen:
                continue
            seen.add(p)
            pts.append(p)

    else:
        # Geração geral
        while len(pts) < n_points:
            p = random_point()
            if not allow_duplicates and p in seen:
                continue
            seen.add(p)
            pts.append(p)

    # Imprime no formato exigido
    print(n_points)
    for (x, y, z) in pts:
        print(f"{x} {y} {z}")


def main():
    parser = argparse.ArgumentParser(
        description="Gera casos de teste aleatórios para Fecho Convexo em R3."
    )
    parser.add_argument(
        "--n-points", "-n", type=int, default=20,
        help="Número de pontos a gerar (default: 20)."
    )
    parser.add_argument(
        "--coord-range", "-r", type=int, default=99,
        help="Raio máximo absoluto das coordenadas (coord ∈ [-r..r], default: 99)."
    )
    parser.add_argument(
        "--allow-duplicates", action="store_true",
        help="Permite pontos duplicados na entrada."
    )
    parser.add_argument(
        "--force-coplanar", action="store_true",
        help="Gera todos os pontos em um mesmo plano (z=0)."
    )
    parser.add_argument(
        "--force-colinear", action="store_true",
        help="Gera todos os pontos em uma mesma reta (x=y=z)."
    )

    args = parser.parse_args()

    generate_convex_input(
        n_points=args.n_points,
        coord_range=args.coord_range,
        allow_duplicates=args.allow_duplicates,
        force_coplanar=args.force_coplanar,
        force_colinear=args.force_colinear
    )


if __name__ == "__main__":
    main()
