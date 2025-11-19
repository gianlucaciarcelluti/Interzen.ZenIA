#!/bin/bash

# Script di avvio rapido SP00 Procedural Classifier
# Per macOS/Linux

echo "🏛️  SP00 - Procedural Classifier"
echo "================================"
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato!"
    echo "   Installa Python 3.9+ da: https://www.python.org"
    exit 1
fi

echo "✅ Python $(python3 --version) trovato"

# Verifica directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/procedural_classifier"

# Verifica .env
ENV_FILE="../../.env"
if [ ! -f "$ENV_FILE" ]; then
    echo ""
    echo "⚠️  File .env non trovato!"
    echo "   Crea src/.env con:"
    echo "   GROQ_API_KEY=your-key-here"
    echo ""
    echo "   Ottieni una chiave gratuita su: https://console.groq.com"
    echo ""
    read -p "Premi INVIO per continuare senza .env (puoi inserire la key nell'interfaccia)..."
fi

# Verifica dipendenze
echo ""
echo "🔍 Verifica dipendenze..."

if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  Streamlit non installato"
    echo "   Installazione in corso..."
    pip3 install streamlit groq python-dotenv pandas tqdm
fi

echo "✅ Dipendenze OK"

# Avvia Streamlit
echo ""
echo "🚀 Avvio interfaccia Streamlit..."
echo "   URL: http://localhost:8501"
echo ""
echo "   Premi CTRL+C per terminare"
echo ""

streamlit run streamlit_procedural_app.py
