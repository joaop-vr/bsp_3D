# mplementação de BSP Tree para Detecção de Interseções 3D

Este documento fornece uma visão geral dos arquivos e instruções de uso do repositório **bsp_3D**.

## Estrutura de Diretórios

```
convex_hulls_3D/
├── bsp.py
├── plot.py
├── Makefile
├── Relatorio.pdf
├── run_tests.sh
└── testes/
    ├── inputs/
    └── outputs/
```

## Descrição dos Arquivos

- **bsp.py**  
  Implementação de uma árvore BSP (Binary Space Partition) para triângulos em 3D.  
  - Funções principais:
    - `make_plane`, `classify_point`, `classify_triangle`
    - `intersect_segment_triangle`
    - Construção e travessia da árvore BSP para detectar interseções de segmentos com triângulos.

- **plot.py**  
  Script para gerar visualizações 3D da cena de entrada (pontos, triângulos e segmentos). Salva um arquivo PNG no diretório de saída especificado.  
  - Parâmetros:
    - `<input_file>`: arquivo de entrada `.in`
    - `<output_dir>`: diretório onde a imagem será salva

- **Makefile**  
  Contém alvos para facilitar compilação e execução de testes.

- **run_tests.sh**  
  Script Bash que:
  1. Executa `bsp.py` em todos os arquivos `.in` dentro de `testes/inputs/`
  2. Salva saídas em `testes/outputs/`
  3. Gera visualizações via `plot.py`

- **Relatorio.pdf**  
  Relatório completo da tarefa de geometria computacional.

- **testes/inputs/**  
  Arquivos de teste de entrada (`.in`).

- **testes/outputs/**  
  Arquivos de saída gerados pelo `run_tests.sh`.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `numpy`
  - `matplotlib`

## Como Executar

1. **Testes automatizados**  
   Torne o script executável e rode:
   ```bash
   chmod +x run_tests.sh
   ./run_tests.sh
   ```

2. **Plotagem individual**  
   ```bash
   python3 plot.py testes/inputs/exemplo.in testes/outputs/
   ```

3. **Execução direta do BSP**  
   ```bash
   python3 bsp.py < testes/inputs/exemplo.in > output.out
   ```

