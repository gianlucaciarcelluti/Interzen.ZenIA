#!/bin/bash
# Script: converti_fonti_in_testo.sh
# Descrizione: Converte tutti i PDF e HTML nella cartella docs/fonti in file di testo .txt
# Requisiti: pdftotext, lynx (installabili con brew install poppler lynx)

# Path corretto dalla radice del repo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
FONTI_DIR="$REPO_ROOT/docs/fonti"
OUTPUT_DIR="$FONTI_DIR/txt_output"

echo "Script dir: $SCRIPT_DIR"
echo "Repo root: $REPO_ROOT"
echo "Fonti dir: $FONTI_DIR"
echo "Output dir: $OUTPUT_DIR"

# Verifica tool
if ! command -v pdftotext &> /dev/null; then
    echo "Errore: pdftotext non installato. Installa con: brew install poppler"
    exit 1
fi

if ! command -v lynx &> /dev/null; then
    echo "Errore: lynx non installato. Installa con: brew install lynx"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Conversione PDF
echo "Cercando PDF in $FONTI_DIR..."
for pdf in "$FONTI_DIR"/*.pdf; do
  if [ -f "$pdf" ] && [ -s "$pdf" ]; then  # -s controlla che non sia vuoto
    nome=$(basename "$pdf" .pdf)
    echo "Tentando conversione PDF: $pdf"
    
    # Prova prima pdftotext
    pdftotext "$pdf" "$OUTPUT_DIR/$nome.txt" 2>/dev/null
    if [ $? -eq 0 ] && [ -s "$OUTPUT_DIR/$nome.txt" ]; then
      echo "[PDF] $pdf -> $OUTPUT_DIR/$nome.txt"
    else
      echo "[PDF fallito] Provando come HTML: $pdf"
      # Se pdftotext fallisce, prova lynx (per file HTML con estensione .pdf)
      rm -f "$OUTPUT_DIR/$nome.txt"  # Rimuovi file vuoto se creato
      lynx -dump -nolist "$pdf" > "$OUTPUT_DIR/$nome.txt" 2>/dev/null
      if [ $? -eq 0 ] && [ -s "$OUTPUT_DIR/$nome.txt" ]; then
        echo "[HTML] $pdf -> $OUTPUT_DIR/$nome.txt (trattato come HTML)"
      else
        echo "[ERRORE] Conversione fallita per $pdf (né PDF né HTML valido)"
        rm -f "$OUTPUT_DIR/$nome.txt"  # Rimuovi file se vuoto
      fi
    fi
  elif [ -f "$pdf" ]; then
    echo "[SKIP] File vuoto: $pdf"
  fi
done

# Conversione HTML
echo "Cercando HTML in $FONTI_DIR..."
for html in "$FONTI_DIR"/*.html; do
  if [ -f "$html" ] && [ -s "$html" ]; then
    nome=$(basename "$html" .html)
    echo "Convertendo HTML: $html"
    lynx -dump -nolist "$html" > "$OUTPUT_DIR/$nome.txt"
    if [ $? -eq 0 ]; then
      echo "[HTML] $html -> $OUTPUT_DIR/$nome.txt"
    else
      echo "[ERRORE] Conversione fallita per $html"
    fi
  elif [ -f "$html" ]; then
    echo "[SKIP] File vuoto: $html"
  fi
done

echo "Conversione completata. File di testo in $OUTPUT_DIR"
