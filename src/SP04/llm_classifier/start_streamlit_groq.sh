#!/bin/bash

# Script per avviare il POC Streamlit Groq Classifier
# Assicurati di avere Streamlit e le dipendenze installate

echo "=========================================="
echo "🏥 Avvio Classificatore Sinistri Groq"
echo "=========================================="
echo ""

# Controlla se Streamlit è installato
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit non trovato!"
    echo "📦 Installalo con: pip install streamlit"
    exit 1
fi

# Controlla se il file esiste
if [ ! -f "streamlit_groq_classifier.py" ]; then
    echo "❌ File streamlit_groq_classifier.py non trovato!"
    echo "📁 Assicurati di essere nella directory corretta (src/llm_classifier)"
    exit 1
fi

# Controlla variabile ambiente GROQ_API_KEY
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  GROQ_API_KEY non trovata nelle variabili d'ambiente"
    echo "💡 Potrai inserirla nell'interfaccia web"
else
    echo "✅ GROQ_API_KEY trovata"
fi

echo ""
echo "🚀 Avvio applicazione Streamlit..."
echo "📱 L'app si aprirà automaticamente nel browser"
echo "🔗 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C per fermare l'applicazione"
echo ""

# Avvia Streamlit
streamlit run streamlit_groq_classifier.py
