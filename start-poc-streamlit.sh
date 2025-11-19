#!/bin/bash
# Start Streamlit POC for EML → HITL workflow testing

echo "🚀 Avvio POC Streamlit: Email → HITL Workflow"
echo "=============================================="
echo ""

# Check if in venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment non attivo"
    echo "💡 Attiva il venv con: source .venv/Scripts/activate"
    echo ""
    read -p "Vuoi continuare comunque? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check dependencies
echo "📦 Verifica dipendenze..."
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit non installato"
    echo "💡 Installa con: pip install streamlit"
    exit 1
fi

if ! python -c "import psycopg2" 2>/dev/null; then
    echo "⚠️  psycopg2 non installato (tracking workflow non disponibile)"
    echo "💡 Installa con: pip install psycopg2-binary"
fi

# Check services
echo "🔍 Verifica servizi..."
services_ok=true

if ! curl -s http://localhost:8080/nifi-api/system-diagnostics > /dev/null; then
    echo "❌ NiFi non disponibile su porta 8080"
    services_ok=false
fi

if ! curl -s http://localhost:9099/contentListener/fascicolo -X POST -d "test" > /dev/null 2>&1; then
    echo "⚠️  Ingress endpoint potrebbe non essere disponibile su porta 9099"
fi

if ! curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo "⚠️  SP01 EML Parser non disponibile su porta 5001"
fi

if ! curl -s http://localhost:5009/health > /dev/null 2>&1; then
    echo "⚠️  HITL Manager non disponibile su porta 5009"
fi

if [ "$services_ok" = false ]; then
    echo ""
    echo "❌ Alcuni servizi non sono disponibili"
    echo "💡 Esegui prima: cd infrastructure/nifi-workflows/setup && ./deploy.sh"
    exit 1
fi

echo "✅ Servizi disponibili"
echo ""

# Start Streamlit
POC_FILE="src/frontend/poc_eml_to_hitl.py"

if [ ! -f "$POC_FILE" ]; then
    echo "❌ File POC non trovato: $POC_FILE"
    exit 1
fi

echo "🎨 Avvio interfaccia Streamlit..."
echo ""
echo "📖 L'applicazione si aprirà nel browser su: http://localhost:8501"
echo ""
echo "Premi Ctrl+C per fermare"
echo ""

streamlit run "$POC_FILE"
