#!/bin/bash
"""
Script per testare tutti gli endpoint SP01-SP11
"""

echo "═══════════════════════════════════════════════════════════"
echo "🧪 TEST COMPLETO ENDPOINT SP01-SP11"
echo "═══════════════════════════════════════════════════════════"
echo

# Test SP01 - EML Parser
echo "📧 Test SP01 - EML Parser (porta 9091)"
curl -s -X POST "http://localhost:9091/sp01" \
  -H "Content-Type: application/json" \
  -d '{"eml_content": "From: test@example.com\nTo: recipient@example.com\nSubject: Test\n\nTest body"}' | head -1
echo " (expected: HTTP 200)"
echo

# Test SP02 - Document Extractor
echo "📄 Test SP02 - Document Extractor (porta 9092)"
curl -s -X POST "http://localhost:9092/sp02" \
  -H "Content-Type: application/json" \
  -d '{"document_content": "Test document content", "filename": "test.pdf"}' | head -1
echo " (expected: HTTP 200)"
echo

# Test SP03 - Procedural Classifier
echo "🏛️  Test SP03 - Procedural Classifier (porta 9093)"
curl -s -X POST "http://localhost:9093/sp03" \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "test123", "istanza_metadata": {"oggetto": "Test", "richiedente": {"tipo": "PERSONA_FISICA"}, "descrizione_istanza": "Test"}}' | head -1
echo " (expected: HTTP 200)"
echo

# Test SP04 - Knowledge Base
echo "🧠 Test SP04 - Knowledge Base (porta 9094)"
curl -s -X POST "http://localhost:9094/sp04" \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "context": "test context"}' | head -1
echo " (expected: HTTP 200)"
echo

# Test SP05 - Template Engine
echo "📝 Test SP05 - Template Engine (porta 9095)"
curl -s -X POST "http://localhost:9095/sp05" \
  -H "Content-Type: application/json" \
  -d '{"template_type": "test", "metadata": {"test": "data"}}' | head -1
echo " (expected: HTTP 200 - placeholder)"
echo

# Test SP06 - Validator
echo "✅ Test SP06 - Validator (porta 9096)"
curl -s -X POST "http://localhost:9096/sp06" \
  -H "Content-Type: application/json" \
  -d '{"document_content": "Test document", "validation_rules": ["test"]}' | head -1
echo " (expected: HTTP 200 - placeholder)"
echo

# Test SP07 - Content Classifier
echo "🏷️  Test SP07 - Content Classifier (porta 9097)"
curl -s -X POST "http://localhost:9097/sp07" \
  -H "Content-Type: application/json" \
  -d '{"text_content": "Test content", "document_type": "test"}' | head -1
echo " (expected: HTTP 200 - placeholder)"
echo

# Test SP08 - Quality Checker
echo "⭐ Test SP08 - Quality Checker (porta 9098)"
curl -s -X POST "http://localhost:9098/sp08" \
  -H "Content-Type: application/json" \
  -d '{"document_content": "Test document", "quality_checks": ["test"]}' | head -1
echo " (expected: HTTP 200 - placeholder)"
echo

# Test SP11 - Security Audit
echo "🔒 Test SP11 - Security Audit (porta 9101)"
curl -s -X POST "http://localhost:9101/sp11" \
  -H "Content-Type: application/json" \
  -d '{"event_type": "test", "user_id": "test", "document_id": "test", "action": "test"}' | head -1
echo " (expected: HTTP 200 - placeholder)"
echo

echo "═══════════════════════════════════════════════════════════"
echo "📊 VERIFICA STATISTICHE PROCESSORI"
echo "═══════════════════════════════════════════════════════════"
echo

# Verifica che NiFi sia attivo
if curl -s "http://localhost:8080/nifi-api/flow/status" > /dev/null; then
    echo "✅ NiFi è attivo"
else
    echo "❌ NiFi non risponde"
    exit 1
fi

echo
echo "🎯 Test completato!"
echo "Nota: Gli endpoint placeholder restituiranno errore 503 (servizio non disponibile)"
echo "ma i processor groups NiFi saranno attivi e riceveranno le richieste."
echo
echo "═══════════════════════════════════════════════════════════"