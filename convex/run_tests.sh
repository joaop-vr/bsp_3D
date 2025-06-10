#!/bin/bash

# Este script procura todos os arquivos “*.in” no diretório atual e
# executa o programa “convex.py” em cada um, redirecionando a saída
# para um arquivo “*.out” com o mesmo nome-base.
#
# Uso:
#   chmod +x run_all.sh
#   ./run_all.sh
#

# Verifica se o convex.py existe
if [[ ! -f "convex.py" ]]; then
  echo "Erro: não foi encontrado 'convex.py' neste diretório."
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

  echo "Executando: python3 convex.py < \"$f\"  ->  \"$out_file\""
  python3 convex.py < "$f" > "$out_file"

  # Opcional: verifica se houve erro de execução
  if [[ $? -ne 0 ]]; then
    echo "  [Erro] execução em '$f' retornou código diferente de zero."
  fi
done

echo "Todos os .in processados. Saídas em testes/outputs/*.out."
