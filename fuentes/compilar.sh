#!/bin/bash
# Uso: ./compilar.sh documento.tex  (dos pasadas de LuaLaTeX + informe)
set -e
cd "$(dirname "$0")"
f="${1%.tex}"; mkdir -p build
for i in 1 2; do lualatex -interaction=nonstopmode -halt-on-error -output-directory=build "$f.tex" > build/$f.stdout 2>&1 || { tail -40 build/$f.stdout; exit 1; }; done
echo "Overfull: $(grep -c 'Overfull' build/$f.log || true)"
grep -A1 'Overfull' build/$f.log | grep -oE '[0-9.]+pt too wide.*' | sort -rn | head -8 || true
grep -E 'undefined|Font Warning|LaTeX Warning: Reference' build/$f.log | sort -u | head -10 || true
pdfinfo build/$f.pdf | grep Pages
