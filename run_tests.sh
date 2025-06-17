#!/bin/bash

# Este script procura todos os arquivos “*.in” no diretório atual e
# executa o programa “bsp.py” em cada um, redirecionando a saída
# para um arquivo “*.out” com o mesmo nome-base.
# Em seguida, executa o plot.py para gerar uma visualização da entrada.
#
# Uso:
#   chmod +x run_all.sh
#   ./run_all.sh
#

# Verifica se o bsp.py existe
if [[ ! -f "bsp.py" ]]; then
  echo "Erro: não foi encontrado 'bsp.py' neste diretório."
  exit 1
fi

# Verifica se o plot.py existe
if [[ ! -f "plot.py" ]]; then
  echo "Erro: não foi encontrado 'plot.py' neste diretório."
  exit 1
fi

# Loop em todos os arquivos .in
for f in testes/inputs/*.in; do
  # Se não houver nenhum .in, termina
  [[ -e "$f" ]] || { echo "Nenhum arquivo .in encontrado."; break; }

  # Extrai o nome-base (sem diretório e sem extensão .in)
  base="$(basename "$f" .in)"

  # Arquivo de saída .out
  out_file="testes/outputs/$base.out"

  echo "Executando: python3 bsp.py < \"$f\"  ->  \"$out_file\""
  python3 bsp.py < "$f" > "$out_file"

  # Verifica erro de execução
  if [[ $? -ne 0 ]]; then
    echo "  [Erro] execução em '$f' retornou código diferente de zero."
    continue
  fi

  # Geração de imagem com plot.py
  echo "Gerando imagem com plot.py para '$f'..."
  python3 plot.py "$f" "testes/outputs/"

  if [[ $? -ne 0 ]]; then
    echo "  [Erro] ao gerar imagem para '$f'."
  fi
done

echo "Todos os .in processados. Saídas e imagens geradas em testes/outputs/."
