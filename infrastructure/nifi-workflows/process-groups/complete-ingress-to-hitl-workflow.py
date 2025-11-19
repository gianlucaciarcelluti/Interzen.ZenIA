#!/usr/bin/env python3
"""
Complete Ingress → SP01 → HITL Workflow
Automatizza la creazione del flusso completo fino al primo checkpoint HITL
"""

import requests
import json
import time
import sys

NIFI_API = "http://localhost:8080/nifi-api"

# IDs noti
SP01_PG_ID = "4e7dc896-019a-1000-0ec8-aa1b9a496844"
HITL_PG_ID = "4e7dcd0f-019a-1000-72e8-9912307e8eb2"
SP01_INPUT_PORT_ID = "4f040fa9-019a-1000-d8a4-36cd9662c23d"  # From_Ingress
SP01_SUCCESS_PORT_ID = "4e7dc8f1-019a-1000-7319-2cb900d6dec8"
SP01_CALL_MICROSERVICE_ID = "4e7dc8b9-019a-1000-9068-896bef10d2ec"

def log_step(step_num, description):
    """Log formattato per i vari step"""
    print(f"\n{'='*70}")
    print(f"  {step_num} {description}")
    print('='*70)

def log_success(message):
    """Log di successo"""
    print(f"   ✓ {message}")

def log_error(message):
    """Log di errore"""
    print(f"   ❌ {message}")

def log_info(message):
    """Log informativo"""
    print(f"   ℹ️  {message}")

def fix_sp01_call_microservice():
    """Fix processor Call_SP01_Microservice: auto-termina relationship 'Original'"""
    log_step("1️⃣", "Fix SP01 Call_SP01_Microservice")
    
    response = requests.get(f"{NIFI_API}/processors/{SP01_CALL_MICROSERVICE_ID}")
    proc_data = response.json()
    
    update_data = {
        "revision": proc_data['revision'],
        "component": {
            "id": SP01_CALL_MICROSERVICE_ID,
            "config": {
                "properties": {
                    "HTTP Method": "POST",
                    "Remote URL": "http://sp01:5001/parse",
                    "Content-Type": "message/rfc822"
                },
                "autoTerminatedRelationships": ["Original", "Retry", "No Retry"]
            }
        }
    }
    
    response = requests.put(
        f"{NIFI_API}/processors/{SP01_CALL_MICROSERVICE_ID}",
        headers={"Content-Type": "application/json"},
        json=update_data
    )
    
    if response.status_code == 200:
        log_success("Call_SP01_Microservice configurato")
        log_info("URL: http://sp01:5001/parse")
        log_info("Relationships auto-terminate: Original, Retry, No Retry")
    else:
        log_error(f"Errore configurazione: {response.status_code}")
        return False
    
    return True

def start_sp01_processors():
    """Avvia tutti i processor in SP01"""
    log_step("2️⃣", "Avvio Processor SP01")
    
    # Avvia Input Port
    response = requests.get(f"{NIFI_API}/input-ports/{SP01_INPUT_PORT_ID}")
    port_data = response.json()
    
    run_data = {
        "revision": port_data['revision'],
        "state": "RUNNING"
    }
    
    response = requests.put(
        f"{NIFI_API}/input-ports/{SP01_INPUT_PORT_ID}/run-status",
        headers={"Content-Type": "application/json"},
        json=run_data
    )
    
    if response.status_code == 200:
        log_success("Input Port 'From_Ingress' avviato")
    
    # Avvia Call_SP01_Microservice
    response = requests.get(f"{NIFI_API}/processors/{SP01_CALL_MICROSERVICE_ID}")
    proc_data = response.json()
    
    run_data = {
        "revision": proc_data['revision'],
        "state": "RUNNING"
    }
    
    response = requests.put(
        f"{NIFI_API}/processors/{SP01_CALL_MICROSERVICE_ID}/run-status",
        headers={"Content-Type": "application/json"},
        json=run_data
    )
    
    if response.status_code == 200:
        log_success("Call_SP01_Microservice avviato")
    else:
        log_error(f"Errore avvio: {response.status_code}")
    
    # Avvia Success Output Port
    response = requests.get(f"{NIFI_API}/output-ports/{SP01_SUCCESS_PORT_ID}")
    port_data = response.json()
    
    run_data = {
        "revision": port_data['revision'],
        "state": "RUNNING"
    }
    
    response = requests.put(
        f"{NIFI_API}/output-ports/{SP01_SUCCESS_PORT_ID}/run-status",
        headers={"Content-Type": "application/json"},
        json=run_data
    )
    
    if response.status_code == 200:
        log_success("Output Port 'Success' avviato")
    
    return True

def create_hitl_input_port():
    """Crea Input Port in HITL Process Group"""
    log_step("3️⃣", "Creazione Input Port in HITL")
    
    # Verifica se esiste già
    response = requests.get(f"{NIFI_API}/process-groups/{HITL_PG_ID}/input-ports")
    existing_ports = response.json().get('inputPorts', [])
    
    for port in existing_ports:
        if 'From_SP01' in port['component']['name']:
            log_info(f"Input Port già esistente: {port['id']}")
            return port['id']
    
    # Crea nuovo Input Port
    port_data = {
        "revision": {"version": 0},
        "component": {
            "name": "From_SP01",
            "position": {
                "x": 100,
                "y": 100
            }
        }
    }
    
    response = requests.post(
        f"{NIFI_API}/process-groups/{HITL_PG_ID}/input-ports",
        headers={"Content-Type": "application/json"},
        json=port_data
    )
    
    if response.status_code == 201:
        port_id = response.json()['id']
        log_success(f"Input Port creato: {port_id}")
        return port_id
    else:
        log_error(f"Errore creazione: {response.status_code}")
        return None

def connect_sp01_to_hitl(hitl_input_port_id):
    """Connette SP01 Success Output Port a HITL Input Port"""
    log_step("4️⃣", "Connessione SP01 → HITL")
    
    connection_data = {
        "revision": {"version": 0},
        "component": {
            "source": {
                "id": SP01_SUCCESS_PORT_ID,
                "groupId": SP01_PG_ID,
                "type": "OUTPUT_PORT"
            },
            "destination": {
                "id": hitl_input_port_id,
                "groupId": HITL_PG_ID,
                "type": "INPUT_PORT"
            },
            "selectedRelationships": [""]
        }
    }
    
    response = requests.post(
        f"{NIFI_API}/process-groups/root/connections",
        headers={"Content-Type": "application/json"},
        json=connection_data
    )
    
    if response.status_code == 201:
        conn_id = response.json()['id']
        log_success(f"Connessione creata: {conn_id}")
        log_info("SP01 Success → HITL From_SP01")
        return conn_id
    elif response.status_code == 409:
        log_info("Connessione già esistente")
        return True
    else:
        log_error(f"Errore connessione: {response.status_code}")
        log_error(f"Response: {response.text[:300]}")
        return None

def configure_hitl_workflow(hitl_input_port_id):
    """Configura il workflow interno di HITL"""
    log_step("5️⃣", "Configurazione Workflow HITL")
    
    # Trova il processor Call_SP11_Security_Audit
    response = requests.get(f"{NIFI_API}/process-groups/{HITL_PG_ID}/processors")
    processors = response.json().get('processors', [])
    
    hitl_call_proc_id = None
    for proc in processors:
        if 'Call_SP11' in proc['component']['name']:
            hitl_call_proc_id = proc['id']
            log_info(f"Trovato processor: {proc['component']['name']}")
            break
    
    if not hitl_call_proc_id:
        log_error("Processor Call_SP11 non trovato!")
        return False
    
    # Connetti Input Port → Call_SP11
    connection_data = {
        "revision": {"version": 0},
        "component": {
            "source": {
                "id": hitl_input_port_id,
                "groupId": HITL_PG_ID,
                "type": "INPUT_PORT"
            },
            "destination": {
                "id": hitl_call_proc_id,
                "groupId": HITL_PG_ID,
                "type": "PROCESSOR"
            },
            "selectedRelationships": [""]
        }
    }
    
    response = requests.post(
        f"{NIFI_API}/process-groups/{HITL_PG_ID}/connections",
        headers={"Content-Type": "application/json"},
        json=connection_data
    )
    
    if response.status_code in [201, 409]:
        log_success("Input Port connesso a Call_SP11")
    else:
        log_error(f"Errore connessione: {response.status_code}")
    
    # Configura Call_SP11 processor
    response = requests.get(f"{NIFI_API}/processors/{hitl_call_proc_id}")
    proc_data = response.json()
    
    update_data = {
        "revision": proc_data['revision'],
        "component": {
            "id": hitl_call_proc_id,
            "config": {
                "properties": {
                    "HTTP Method": "POST",
                    "Remote URL": "http://hitl:5009/hitl/review",
                    "Content-Type": "application/json"
                },
                "autoTerminatedRelationships": ["Original", "Retry", "No Retry", "Failure"]
            }
        }
    }
    
    response = requests.put(
        f"{NIFI_API}/processors/{hitl_call_proc_id}",
        headers={"Content-Type": "application/json"},
        json=update_data
    )
    
    if response.status_code == 200:
        log_success("Call_SP11 configurato")
        log_info("URL: http://hitl:5009/hitl/review")
    
    return True

def main():
    """Main execution"""
    print("=" * 70)
    print("  🚀 Completamento Workflow Ingress → SP01 → HITL")
    print("=" * 70)
    
    try:
        # Step 1: Fix SP01 Call Microservice
        if not fix_sp01_call_microservice():
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 2: Avvia processor SP01
        if not start_sp01_processors():
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 3: Crea Input Port in HITL
        hitl_input_port_id = create_hitl_input_port()
        if not hitl_input_port_id:
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 4: Connetti SP01 → HITL
        if not connect_sp01_to_hitl(hitl_input_port_id):
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 5: Configura workflow HITL
        if not configure_hitl_workflow(hitl_input_port_id):
            sys.exit(1)
        
        # Success!
        log_step("✅", "COMPLETATO!")
        print()
        print("🎯 Workflow Ingress → SP01 → HITL completato con successo!")
        print()
        print("📊 Flusso Dati:")
        print("   1. POST http://localhost:9099/contentListener/fascicolo")
        print("   2. Ingress_ContentListener elabora richiesta")
        print("   3. SP01 riceve .eml via Input Port 'From_Ingress'")
        print("   4. SP01 chiama http://sp01:5001/parse")
        print("   5. SP01 invia risultato via Output Port 'Success'")
        print("   6. HITL riceve via Input Port 'From_SP01'")
        print("   7. HITL chiama http://hitl:5009/hitl/review")
        print()
        print("🧪 Prossimo step: Test end-to-end!")
        print()
        
    except Exception as e:
        log_error(f"Errore imprevisto: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
