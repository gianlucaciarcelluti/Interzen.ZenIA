#!/bin/bash
# Test script for Ingress endpoint

ENDPOINT="http://localhost:9099/contentListener/fascicolo"
TEST_EMAIL="../../../examples/eml-samples/01_autorizzazione_scarico_acque.eml"

echo "🧪 Test Ingress Endpoint"
echo "========================"
echo ""
echo "Endpoint: $ENDPOINT"
echo "Email:    $TEST_EMAIL"
echo ""

if [ ! -f "$TEST_EMAIL" ]; then
    echo "❌ File di test non trovato: $TEST_EMAIL"
    exit 1
fi

echo "📤 Invio email..."
response=$(curl -s -w "\n%{http_code}" -X POST "$ENDPOINT" \
    -H "Content-Type: message/rfc822" \
    --data-binary "@$TEST_EMAIL")

http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | head -n -1)

echo ""
if [ "$http_code" -eq 200 ]; then
    echo "✅ Successo! HTTP $http_code"
    echo ""
    echo "Risposta:"
    echo "$body" | head -20
else
    echo "❌ Errore! HTTP $http_code"
    echo ""
    echo "Risposta:"
    echo "$body"
fi

echo ""
echo "🔍 Verifica audit database:"
echo "   docker exec postgres-db psql -U nifi -d nifi_audit -c 'SELECT * FROM workflow_executions ORDER BY started_at DESC LIMIT 1;'"
