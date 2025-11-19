#!/bin/bash
"""
Script wrapper per deployment completo del sistema ZenIA
Esegue automaticamente tutti gli script necessari in sequenza
"""

set -e

echo "🚀 DEPLOYMENT COMPLETO - ZenIA"
echo "=============================================="
echo ""
echo "Questo script eseguirà in sequenza:"
echo "  1. deploy.sh (setup infrastruttura + NiFi)"
echo "  2. Verifica finale del sistema"
echo ""

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Verifica che siamo nella directory giusta
if [ ! -f "deploy.sh" ]; then
    echo -e "${RED}❌ Errore: deploy.sh non trovato nella directory corrente${NC}"
    echo -e "${YELLOW}💡 Assicurati di essere in: infrastructure/nifi-workflows/setup/${NC}"
    exit 1
fi

# Verifica Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker non trovato. Installa Docker Desktop.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose non trovato.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker e Docker Compose pronti${NC}"

# Chiedi se fare la build dei Docker images
echo ""
echo -e "${YELLOW}🔨 Vuoi fare la build dei Docker images?${NC}"
echo -e "${YELLOW}   (Questo potrebbe richiedere diversi minuti)${NC}"
read -p "Build Docker images? [y/N]: " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⏭️  Salto la build dei Docker images${NC}"
    SKIP_BUILD=true
else
    echo -e "${GREEN}✅ Procedo con la build dei Docker images${NC}"
    SKIP_BUILD=false
fi

# Esegui il deployment principale
echo ""
echo -e "${YELLOW}🔧 Esecuzione deployment principale...${NC}"
echo "=============================================="

if [ "$SKIP_BUILD" = true ]; then
    ./deploy.sh --skip-build
else
    ./deploy.sh
fi

# Verifica finale
echo ""
echo -e "${YELLOW}🔍 Verifica finale del sistema...${NC}"
echo "==================================="

# Test NiFi
if curl -s "http://localhost:8080/nifi-api/system-diagnostics" &> /dev/null; then
    echo -e "${GREEN}✅ Apache NiFi: OK${NC}"
else
    echo -e "${RED}❌ Apache NiFi: KO${NC}"
fi

# Test PostgreSQL
if docker-compose exec -T postgres pg_isready -U postgres -h localhost &>/dev/null; then
    echo -e "${GREEN}✅ PostgreSQL: OK${NC}"
else
    echo -e "${RED}❌ PostgreSQL: KO${NC}"
fi

# Test Redis
if docker-compose exec -T redis redis-cli ping 2>/dev/null | grep -q PONG; then
    echo -e "${GREEN}✅ Redis: OK${NC}"
else
    echo -e "${RED}❌ Redis: KO${NC}"
fi

# Test SP01
if curl -s --max-time 5 http://localhost:9091/ &>/dev/null; then
    echo -e "${GREEN}✅ SP01 EML Parser: OK${NC}"
else
    echo -e "${YELLOW}⚠️  SP01 EML Parser: Non pronto (normale, potrebbe richiedere più tempo)${NC}"
fi

# Test Audit Database
AUDIT_TABLES=$(docker exec postgres-db psql -U postgres -d nifi_audit -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")
if [ "$AUDIT_TABLES" -gt "0" ]; then
    echo -e "${GREEN}✅ Audit Database: OK ($AUDIT_TABLES tabelle)${NC}"
else
    echo -e "${RED}❌ Audit Database: KO${NC}"
fi

echo ""
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETATO!${NC}"
echo "==========================="
echo ""
echo "Sistema UP & RUNNING su:"
echo "  🔹 NiFi UI: http://localhost:8080/nifi"
echo "  🔹 Ingress: http://localhost:9099/contentListener/fascicolo"
echo "  🔹 Audit DB: docker exec -it postgres-db psql -U postgres -d nifi_audit"
echo ""
echo "Per monitorare i logs: docker-compose logs -f"
echo "Per fermare tutto: docker-compose down"