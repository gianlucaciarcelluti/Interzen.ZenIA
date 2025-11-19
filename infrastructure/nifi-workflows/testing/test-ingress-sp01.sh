#!/bin/bash

# ==============================================
# Test Ingress → SP01 Workflow
# ==============================================

echo "======================================================================"
echo "  🧪 Test Workflow: Ingress → SP01"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Check endpoint availability
echo -e "${YELLOW}[1/4] 🔍 Verifica disponibilità endpoint...${NC}"
echo ""

if curl -s --max-time 5 http://localhost:9099/contentListener/fascicolo > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Endpoint raggiungibile: http://localhost:9099/contentListener/fascicolo${NC}"
else
    echo -e "${RED}❌ Endpoint NON raggiungibile${NC}"
    echo -e "${YELLOW}💡 Verifica che i processors HandleHttpRequest siano avviati${NC}"
fi

echo ""

# Test 2: Check SP01 service
echo -e "${YELLOW}[2/4] 🔍 Verifica servizio SP01...${NC}"
echo ""

if curl -s --max-time 5 http://localhost:5001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ SP01 service attivo su porta 5001${NC}"
    HEALTH=$(curl -s http://localhost:5001/health | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])" 2>/dev/null || echo "unknown")
    echo -e "${BLUE}   Status: ${HEALTH}${NC}"
else
    echo -e "${RED}❌ SP01 service NON raggiungibile${NC}"
    echo -e "${YELLOW}💡 Avvia SP01: docker-compose up -d sp01-eml-parser${NC}"
fi

echo ""

# Test 3: Check NiFi connections
echo -e "${YELLOW}[3/4] 🔍 Verifica connessioni NiFi...${NC}"
echo ""

# Check Ingress PG exists
INGRESS_CHECK=$(curl -s "http://localhost:8080/nifi-api/process-groups/root/process-groups" 2>/dev/null | grep -c "Ingress_ContentListener" || echo "0")

if [ "$INGRESS_CHECK" -gt "0" ]; then
    echo -e "${GREEN}✅ Process Group Ingress_ContentListener esistente${NC}"
else
    echo -e "${RED}❌ Process Group Ingress_ContentListener NON trovato${NC}"
fi

# Check SP01 PG exists
SP01_CHECK=$(curl -s "http://localhost:8080/nifi-api/process-groups/root/process-groups" 2>/dev/null | grep -c "SP01" || echo "0")

if [ "$SP01_CHECK" -gt "0" ]; then
    echo -e "${GREEN}✅ Process Group SP01_EML_Parser esistente${NC}"
else
    echo -e "${RED}❌ Process Group SP01_EML_Parser NON trovato${NC}"
fi

echo ""

# Test 4: Visual verification instructions
echo -e "${YELLOW}[4/4] 👀 Verifica visuale Canvas NiFi${NC}"
echo ""
echo -e "${BLUE}🌐 Apri nel browser: http://localhost:8080/nifi${NC}"
echo ""
echo "Verifica che:"
echo "  ✓ Process Group 'Ingress_ContentListener' sia visibile"
echo "  ✓ Connessione visibile tra Ingress e SP01 (linea blu)"
echo "  ✓ Processors in stato RUNNING (icona verde)"
echo ""

# Summary
echo "======================================================================"
echo -e "${GREEN}  📊 Riepilogo Test${NC}"
echo "======================================================================"
echo ""
echo "📦 Componenti:"
echo "   - Ingress PG: $([ "$INGRESS_CHECK" -gt "0" ] && echo "✅" || echo "❌")"
echo "   - SP01 PG: $([ "$SP01_CHECK" -gt "0" ] && echo "✅" || echo "❌")"
echo ""
echo "🌐 Servizi:"
echo "   - Endpoint Ingress (9099): $(curl -s --max-time 2 http://localhost:9099/contentListener/fascicolo > /dev/null 2>&1 && echo "✅" || echo "❌")"
echo "   - SP01 Service (5001): $(curl -s --max-time 2 http://localhost:5001/health > /dev/null 2>&1 && echo "✅" || echo "❌")"
echo ""
echo "======================================================================"
echo ""
echo -e "${BLUE}📝 Test manuale con file .eml:${NC}"
echo ""
echo "# Crea un file test.eml"
echo 'cat > /tmp/test.eml << EOF'
echo 'From: test@example.com'
echo 'To: recipient@example.com'
echo 'Subject: Test Email'
echo ''
echo 'This is a test email body.'
echo 'EOF'
echo ""
echo "# Invia al workflow"
echo 'curl -X POST http://localhost:9099/contentListener/fascicolo \'
echo '     -H "Content-Type: message/rfc822" \'
echo '     --data-binary @/tmp/test.eml'
echo ""
echo "======================================================================"
echo ""
