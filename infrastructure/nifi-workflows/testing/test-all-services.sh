#!/bin/bash

# =========================================
# Test Services Script - Apache NiFi Architecture
# =========================================
# SP01, SP02, SP05, SP08: NiFi Process Groups (configured in NiFi UI)
# SP03: Active microservice (RAG + FAISS)
# SP04: Optional microservice (can use Groq in NiFi)

echo "🧪 Testing Active Microservices (Apache NiFi Architecture)..."
echo "=============================================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

services=("sp03" "sp04")
ports=(5003 5004)
names=("Knowledge Base (RAG)" "Classifier (Optional)")
build_types=("local" "root")

echo ""
echo "📦 Building active microservices..."
echo ""

cd "$(dirname "$0")"

for i in "${!services[@]}"; do
    service="${services[$i]}"
    port="${ports[$i]}"
    name="${names[$i]}"
    build_type="${build_types[$i]}"
    
    echo -e "${YELLOW}Building ${service} - ${name}...${NC}"
    
    # SP04 needs special build context (root)
    if [ "$build_type" == "root" ]; then
        if docker build -q -f services/${service}/Dockerfile -t ${service}-service ../.. > /dev/null 2>&1; then
            echo -e "${GREEN}✅ ${service} build successful ${BLUE}(root context)${NC}"
        else
            echo -e "${RED}❌ ${service} build failed${NC}"
            exit 1
        fi
    else
        if docker build -q -t ${service}-service services/${service}/ > /dev/null 2>&1; then
            echo -e "${GREEN}✅ ${service} build successful${NC}"
        else
            echo -e "${RED}❌ ${service} build failed${NC}"
            exit 1
        fi
    fi
done

echo ""
echo -e "${GREEN}🎉 All active microservices built successfully!${NC}"
echo ""
echo -e "${BLUE}📝 Architecture Notes:${NC}"
echo -e "   ${GREEN}✅ SP03${NC} - Knowledge Base (Active microservice with FAISS)"
echo -e "   ${YELLOW}🟡 SP04${NC} - Classifier (Optional, can use Groq in NiFi instead)"
echo ""
echo -e "   ${BLUE}🔄 NiFi Process Groups (configured in NiFi UI):${NC}"
echo "      - SP01 - Template Engine (Groq API + InvokeHTTP)"
echo "      - SP02 - Validator (Groq semantic + RouteOnAttribute)"
echo "      - SP05 - Quality Checker (LanguageTool API + NiFi processors)"
echo "      - SP08 - Security Audit (JWT + NiFi Provenance)"
echo ""
echo "To run active microservices:"
echo "  docker run -p 5003:5003 sp03-service  ${GREEN}# Knowledge Base${NC}"
echo "  docker run -p 5004:5004 sp04-service  ${YELLOW}# Classifier (optional)${NC}"
echo ""
echo "Access Swagger UI:"
echo "  http://localhost:5003/docs ${GREEN}(SP03 - Knowledge Base)${NC}"
echo "  http://localhost:5004/docs ${YELLOW}(SP04 - Classifier)${NC}"
echo ""
echo "Apache NiFi UI:"
echo "  https://localhost:8443/nifi ${BLUE}(NiFi Dashboard - import templates)${NC}"
echo ""

# Optional: cleanup
read -p "Cleanup test images? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleaning up..."
    for service in "${services[@]}"; do
        docker rmi ${service}-service > /dev/null 2>&1
    done
    echo "✅ Cleanup done"
fi