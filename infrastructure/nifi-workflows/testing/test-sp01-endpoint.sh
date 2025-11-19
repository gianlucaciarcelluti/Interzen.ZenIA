#!/bin/bash

# =========================================
# Test SP01 Endpoint Script
# =========================================

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

SP01_URL="http://localhost:9091"

echo -e "${BLUE}🧪 Test SP01 EML Parser Endpoint${NC}"
echo "=================================="

# Test 1: Simple JSON test
echo -e "${YELLOW}Test 1: Richiesta JSON semplice...${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$SP01_URL/" \
  -H "Content-Type: application/json" \
  -d '{"test": "SP01 endpoint test", "timestamp": "'$(date)'"}')

http_status=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
body=$(echo "$response" | sed '/HTTP_STATUS:/d')

if [ "$http_status" = "200" ]; then
    echo -e "${GREEN}✅ Test 1 PASSED (HTTP $http_status)${NC}"
    echo "Response: $body"
else
    echo -e "${RED}❌ Test 1 FAILED (HTTP $http_status)${NC}"
    echo "Response: $body"
fi

echo ""

# Test 2: EML-like content test
echo -e "${YELLOW}Test 2: Contenuto simile a EML...${NC}"
eml_content='{
  "subject": "Test Provvedimento",
  "from": "test@example.com",
  "to": "destinatario@example.com",
  "body": "Questo è un test del parser EML per provvedimenti amministrativi.",
  "attachments": ["documento.pdf"],
  "metadata": {
    "tipo_provvedimento": "autorizzazione",
    "numero_protocollo": "123/2024"
  }
}'

response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$SP01_URL/" \
  -H "Content-Type: application/json" \
  -d "$eml_content")

http_status=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
body=$(echo "$response" | sed '/HTTP_STATUS:/d')

if [ "$http_status" = "200" ]; then
    echo -e "${GREEN}✅ Test 2 PASSED (HTTP $http_status)${NC}"
    echo "Response: $body"
else
    echo -e "${RED}❌ Test 2 FAILED (HTTP $http_status)${NC}"
    echo "Response: $body"
fi

echo ""
echo -e "${BLUE}📊 Monitora i logs NiFi:${NC}"
echo "   docker-compose logs -f nifi | grep -i sp01"
echo ""
echo -e "${BLUE}📊 Monitora i logs SP01:${NC}"
echo "   docker-compose logs -f sp01-eml-parser"