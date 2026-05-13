#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Uso: $0 <arquivo.md> [argumentos extras para gera_html.py]"
  exit 1
fi

MD_PATH="$1"
shift || true

if [[ ! -f "$MD_PATH" ]]; then
  echo "Erro: arquivo não encontrado: $MD_PATH"
  exit 1
fi

if [[ "${MD_PATH##*.}" != "md" ]]; then
  echo "Erro: o parâmetro deve ser um arquivo .md"
  exit 1
fi

BASENAME="$(basename "$MD_PATH" .md)"
OUT_HTML="html/${BASENAME}.html"

python3 scripts/gera_html.py \
  "$MD_PATH" \
  "$OUT_HTML" \
  --template templates/topico.template.html \
  "$@"

echo "Gerado: $OUT_HTML"
