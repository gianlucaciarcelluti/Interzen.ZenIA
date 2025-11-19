#!/bin/bash

set -e  # Exit on any error

echo "🧹 Script di pulizia risorse Docker"
echo "=================================="
echo "Questo script:"
echo "  ✅ Pulisce database PostgreSQL (eccetto testdb e postgres) PRIMA di scendere la VM"
echo "  ✅ Ferma tutti i container con docker-compose down"
echo "  ✅ Rimuove tutti i container (attivi e fermi)"
echo "  ✅ Opzionalmente rimuove volumi Docker (con lista dettagliata)"
echo "  ✅ Opzionalmente rimuove immagini (dangling / tutte non utilizzate)"
echo "  ✅ Opzionalmente svuota cache (build / reti / sistema completo)"
echo ""
echo "🛡️  PROTETTO: testdb, postgres, bind mount /Users/giangioiz/postgresql/data"
echo ""

read -p "Procedere con la pulizia? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operazione annullata dall'utente."
    exit 0
fi

echo "🧹 Pulizia risorse Docker e PostgreSQL"
echo "======================================"

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funzione per logging
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 0. Pulizia database PostgreSQL PRIMA di scendere la VM
log "Pulizia database PostgreSQL (mantenendo solo testdb e postgres)..."

# Controlla se il container postgres esiste e è attivo
if docker ps --format "{{.Names}}" | grep -q "^postgres-db$"; then
    log "Container postgres-db trovato e attivo, procedo con pulizia database..."
    
    databases_to_remove=$(docker exec postgres-db psql -U postgres -lqt 2>/dev/null | cut -d\| -f1 | grep -v -E "(^\s*$|template0|template1|postgres|testdb)" | sed 's/^\s*//' | sed 's/\s*$//' || true)
    
    if [ -n "$databases_to_remove" ]; then
        log "Database da rimuovere: $(echo $databases_to_remove | tr '\n' ' ')"
        
        for db in $databases_to_remove; do
            if [ -n "$db" ]; then
                log "Rimozione database: $db"
                docker exec postgres-db psql -U postgres -c "DROP DATABASE IF EXISTS \"$db\";" 2>/dev/null || warn "Impossibile rimuovere database: $db"
            fi
        done
        log "✅ Database rimossi"
    else
        log "Nessun database da rimuovere (solo testdb e postgres presenti)"
    fi
elif docker ps -a --format "{{.Names}}" | grep -q "^postgres-db$"; then
    # Container esiste ma è fermo, avviamolo temporaneamente
    log "Container postgres-db trovato ma fermo, avvio temporaneo per pulizia database..."
    docker start postgres-db 2>/dev/null || warn "Impossibile avviare postgres-db"
    sleep 3
    
    databases_to_remove=$(docker exec postgres-db psql -U postgres -lqt 2>/dev/null | cut -d\| -f1 | grep -v -E "(^\s*$|template0|template1|postgres|testdb)" | sed 's/^\s*//' | sed 's/\s*$//' || true)
    
    if [ -n "$databases_to_remove" ]; then
        log "Database da rimuovere: $(echo $databases_to_remove | tr '\n' ' ')"
        
        for db in $databases_to_remove; do
            if [ -n "$db" ]; then
                log "Rimozione database: $db"
                docker exec postgres-db psql -U postgres -c "DROP DATABASE IF EXISTS \"$db\";" 2>/dev/null || warn "Impossibile rimuovere database: $db"
            fi
        done
        log "✅ Database rimossi"
    else
        log "Nessun database da rimuovere (solo testdb e postgres presenti)"
    fi
else
    log "Container postgres-db non trovato, skip pulizia database"
fi

# 1. Shutdown completo (opzionale ma raccomandato)
log "Shutdown completo dei servizi..."
if [ -f "docker-compose.yml" ]; then
    log "Eseguo docker-compose down..."
    docker-compose down 2>/dev/null || warn "docker-compose down fallito"
fi

# Ferma forzatamente tutti i container attivi (eccetto postgres se esistente)
log "Ferma forzatamente tutti i container..."
all_containers=$(docker ps -q 2>/dev/null || true)
postgres_containers=$(docker ps -q --filter "name=postgres" 2>/dev/null || true)

if [ -n "$all_containers" ]; then
    if [ -n "$postgres_containers" ]; then
        # Ferma tutti tranne postgres
        containers_to_stop=$(docker ps -q | grep -v "$postgres_containers" || true)
        if [ -n "$containers_to_stop" ]; then
            log "Fermando container (eccetto postgres): $(echo $containers_to_stop | wc -w) container"
            docker stop $containers_to_stop 2>/dev/null || warn "Alcuni container potrebbero non essersi fermati"
        else
            log "Solo container postgres attivo, nessun altro da fermare"
        fi
    else
        # Ferma tutti i container (postgres non è attivo)
        log "Fermando tutti i container (postgres non attivo)..."
        docker stop $all_containers 2>/dev/null || warn "Alcuni container potrebbero non essersi fermati"
    fi
    log "✅ Shutdown forzato completato"
else
    log "Nessun container attivo da fermare"
fi

# 1. Rimuovi tutti i container (attivi e fermi, tranne postgres)
log "Rimozione container Docker (attivi e fermi, tranne postgres)..."

# Prima ferma tutti i container attivi (eccetto postgres)
active_containers=$(docker ps -q --filter "name=postgres" --format "{{.Names}}" | grep -v postgres || true)
if [ -n "$active_containers" ]; then
    log "Fermando container attivi (eccetto postgres): $(echo $active_containers | wc -w) container"
    docker stop $active_containers 2>/dev/null || warn "Alcuni container potrebbero non essersi fermati"
fi

# Poi rimuovi tutti i container fermi (eccetto postgres)
stopped_containers=$(docker ps -aq --filter "status=exited" | grep -v postgres || true)
if [ -n "$stopped_containers" ]; then
    log "Rimozione container fermi (eccetto postgres): $(echo "$stopped_containers" | wc -l) container"
    docker rm $stopped_containers 2>/dev/null || warn "Alcuni container potrebbero non essere stati rimossi"
    log "✅ Container fermi rimossi"
else
    log "Nessun container fermo da rimuovere"
fi

# Verifica se ci sono ancora container attivi (dovrebbero essere solo postgres se presente)
remaining_active=$(docker ps -q 2>/dev/null || true)
if [ -n "$remaining_active" ]; then
    log "Container ancora attivi: $(echo $remaining_active | wc -w) (dovrebbe essere solo postgres se presente)"
else
    log "✅ Tutti i container rimossi (postgres non presente)"
fi

# 3. Gestione volumi Docker
log "Gestione volumi Docker..."

all_volumes=$(docker volume ls -q 2>/dev/null || true)

if [ -n "$all_volumes" ]; then
    volume_count=$(echo "$all_volumes" | wc -l)
    log "Trovati $volume_count volumi Docker"
    
    # Identifica volumi NiFi specifici
    nifi_volumes=$(echo "$all_volumes" | grep -E "(nifi|setup_nifi)" || true)
    other_volumes=$(echo "$all_volumes" | grep -v -E "(nifi|setup_nifi)" || true)
    
    # Mostra i volumi che verranno rimossi
    echo ""
    echo "📊 Volumi trovati:"
    if [ -n "$nifi_volumes" ]; then
        echo ""
        echo "  🔴 NiFi (contatori, FlowFiles, provenance - verranno azzerati):"
        echo "$nifi_volumes" | sed 's/^/     • /'
    fi
    if [ -n "$other_volumes" ]; then
        echo ""
        echo "  🔵 Altri volumi:"
        echo "$other_volumes" | sed 's/^/     • /'
    fi
    echo ""
    echo "⚠️  ATTENZIONE: Rimuovendo i volumi NiFi, tutti i contatori e lo storico FlowFiles verranno azzerati!"
    echo ""
    
    read -p "Procedere con la rimozione di TUTTI i volumi? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log "Rimozione volumi..."
        removed_count=$(echo "$all_volumes" | xargs docker volume rm 2>/dev/null | wc -l)
        failed_count=$((volume_count - removed_count))
        
        if [ $failed_count -gt 0 ]; then
            warn "$failed_count volumi potrebbero essere in uso o protetti"
        fi
        log "✅ $removed_count volumi rimossi (contatori NiFi azzerati)"
    else
        log "Rimozione volumi saltata dall'utente"
    fi
else
    log "Nessun volume Docker trovato"
fi

# 4. Gestione immagini Docker
echo ""
echo "🖼️  Gestione immagini Docker:"
echo "  1) Rimuovi solo immagini dangling (sicuro)"
echo "  2) Rimuovi tutte le immagini non utilizzate (aggressivo)"
echo "  3) Salta pulizia immagini"
read -p "Scegli opzione immagini (1/2/3) [3]: " -n 1 -r
echo

case $REPLY in
    1)
        log "Rimozione immagini dangling..."
        docker image prune -f
        log "✅ Immagini dangling rimosse"
        ;;
    2)
        log "Rimozione TUTTE le immagini non utilizzate..."
        docker image prune -a -f
        log "✅ Tutte le immagini non utilizzate rimosse"
        ;;
    *)
        log "Pulizia immagini saltata"
        ;;
esac

# 5. Svuota cache Docker completa (opzionale)
echo ""
echo "🗂️  Svuotamento cache Docker:"
echo "  1) Build cache only (sicuro)"
echo "  2) Build cache + reti + dangling (raccomandato)"
echo "  3) Pulizia sistema COMPLETA (aggressivo)"
echo "  4) Salta svuotamento cache"
read -p "Scegli opzione cache (1/2/3/4) [4]: " -n 1 -r
echo

case $REPLY in
    1)
        log "Rimozione build cache..."
        docker builder prune -f
        log "✅ Build cache svuotata"
        ;;
    2)
        log "Rimozione build cache e reti..."
        docker builder prune -f
        docker network prune -f
        log "✅ Build cache e reti svuotate"
        ;;
    3)
        log "Pulizia sistema COMPLETA..."
        docker system prune -f
        log "✅ Sistema completamente pulito"
        ;;
    *)
        log "Svuotamento cache saltato"
        ;;
esac

# 6. Mostra stato finale
log "Stato finale delle risorse:"
echo ""
echo "📦 Container attivi:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "💾 Volumi:"
docker volume ls
echo ""
echo "�️  Immagini:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
echo ""
echo "�🗄️ Database PostgreSQL:"
if docker ps --format "{{.Names}}" | grep -q "^postgres-db$"; then
    docker exec postgres-db psql -U postgres -l 2>/dev/null || echo "Errore connessione database"
else
    echo "Container postgres-db non attivo"
fi
echo ""

log "🎉 Pulizia completata!"
echo "======================================"
echo "🛡️  Risorse PROTETTE (non toccate):"
echo "  • Database: testdb, postgres (sempre protetti)"
echo "  • Volume: bind mount /Users/giangioiz/postgresql/data"
echo ""
echo "🗑️  Risorse RIPULITE (basato sulle tue scelte):"
echo "  • Database: tutti tranne testdb e postgres (PULITO PRIMA del docker-compose down)"
echo "  • Container: tutti (dopo pulizia database)"
echo "  • Volumi: selezionati dall'utente"
echo "  • Immagini: secondo opzione scelta (dangling/tutte/none)"
echo "  • Cache: secondo opzione scelta (build/reti/sistema/none)"