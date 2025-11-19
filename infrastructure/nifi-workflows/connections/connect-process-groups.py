#!/usr/bin/env python3
"""
Connect Process Groups - Inter-PG Workflow Connections
=======================================================
This script creates connections between Process Groups to enable the complete workflow:
1. Ingress_ContentListener → SP01_EML_Parser
2. SP01_EML_Parser (Success) → SP11_Security_Audit (HITL)

Usage:
    python3 connect-process-groups.py
"""

import requests
import json
import sys
from typing import Dict, List, Optional

NIFI_API = "http://localhost:8080/nifi-api"


def get_root_pg_id() -> str:
    """Get root process group ID"""
    response = requests.get(f"{NIFI_API}/flow/process-groups/root")
    response.raise_for_status()
    return response.json()['processGroupFlow']['id']


def get_process_group_by_name(name: str) -> Optional[Dict]:
    """Find a process group by name"""
    try:
        root_id = get_root_pg_id()
        response = requests.get(f"{NIFI_API}/process-groups/{root_id}/process-groups")
        response.raise_for_status()
        
        pgs = response.json()['processGroups']
        for pg in pgs:
            if pg['component']['name'] == name:
                return pg
        return None
    except Exception as e:
        print(f"❌ Errore ricerca Process Group {name}: {e}")
        return None


def get_output_ports(pg_id: str) -> List[Dict]:
    """Get output ports of a process group"""
    try:
        response = requests.get(f"{NIFI_API}/process-groups/{pg_id}/output-ports")
        response.raise_for_status()
        return response.json()['outputPorts']
    except Exception:
        return []


def get_input_ports(pg_id: str) -> List[Dict]:
    """Get input ports of a process group"""
    try:
        response = requests.get(f"{NIFI_API}/process-groups/{pg_id}/input-ports")
        response.raise_for_status()
        return response.json()['inputPorts']
    except Exception:
        return []


def connection_exists(source_id: str, dest_id: str) -> bool:
    """Check if a connection already exists between two components"""
    try:
        root_id = get_root_pg_id()
        response = requests.get(f"{NIFI_API}/process-groups/{root_id}/connections")
        response.raise_for_status()
        
        connections = response.json()['connections']
        for conn in connections:
            src = conn['component']['source']['id']
            dst = conn['component']['destination']['id']
            if src == source_id and dst == dest_id:
                return True
        return False
    except Exception:
        return False


def create_connection(source_id: str, source_type: str, source_group_id: str,
                     dest_id: str, dest_type: str, dest_group_id: str,
                     relationships: List[str] = None) -> bool:
    """Create a connection between two components"""
    try:
        root_id = get_root_pg_id()
        
        # Default relationships if not specified
        if relationships is None:
            relationships = [""]
        
        connection_data = {
            "revision": {"version": 0},
            "component": {
                "source": {
                    "id": source_id,
                    "type": source_type,
                    "groupId": source_group_id
                },
                "destination": {
                    "id": dest_id,
                    "type": dest_type,
                    "groupId": dest_group_id
                },
                "selectedRelationships": relationships
            }
        }
        
        response = requests.post(
            f"{NIFI_API}/process-groups/{root_id}/connections",
            json=connection_data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return True
        
    except Exception as e:
        print(f"   ❌ Errore creazione connessione: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"   Dettagli: {error_detail}")
            except:
                print(f"   Response: {e.response.text[:200]}")
        return False


def connect_ingress_to_sp01():
    """Connect Ingress_ContentListener output to SP01_EML_Parser input"""
    print("\n🔗 [1/2] Connessione Ingress_ContentListener → SP01_EML_Parser")
    
    # Get Ingress PG
    ingress_pg = get_process_group_by_name("Ingress_ContentListener")
    if not ingress_pg:
        print("   ⚠️  Process Group Ingress_ContentListener non trovato")
        return False
    
    ingress_id = ingress_pg['id']
    print(f"   ✓ Trovato Ingress_ContentListener: {ingress_id}")
    
    # Get SP01 PG
    sp01_pg = get_process_group_by_name("SP01_EML_Parser")
    if not sp01_pg:
        print("   ⚠️  Process Group SP01_EML_Parser non trovato")
        return False
    
    sp01_id = sp01_pg['id']
    print(f"   ✓ Trovato SP01_EML_Parser: {sp01_id}")
    
    # Get Ingress output ports
    ingress_outputs = get_output_ports(ingress_id)
    if not ingress_outputs:
        print("   ⚠️  Ingress non ha Output Ports configurati")
        print("   💡 Crea manualmente un Output Port 'To_SP01' in Ingress_ContentListener")
        return False
    
    # Get first output port (should be "To_SP01" or similar)
    ingress_output = ingress_outputs[0]
    print(f"   ✓ Trovato Output Port: {ingress_output['component']['name']}")
    
    # Get SP01 input ports
    sp01_inputs = get_input_ports(sp01_id)
    if not sp01_inputs:
        print("   ⚠️  SP01 non ha Input Ports configurati")
        print("   💡 Crea manualmente un Input Port 'From_Ingress' in SP01_EML_Parser")
        return False
    
    # Get first input port (should be "From_Ingress" or similar)
    sp01_input = sp01_inputs[0]
    print(f"   ✓ Trovato Input Port: {sp01_input['component']['name']}")
    
    # Check if connection already exists
    if connection_exists(ingress_output['id'], sp01_input['id']):
        print("   ✅ Connessione già esistente")
        return True
    
    # Create connection
    print("   🔧 Creazione connessione...")
    success = create_connection(
        source_id=ingress_output['id'],
        source_type="OUTPUT_PORT",
        source_group_id=ingress_id,
        dest_id=sp01_input['id'],
        dest_type="INPUT_PORT",
        dest_group_id=sp01_id
    )
    
    if success:
        print("   ✅ Connessione Ingress → SP01 creata con successo!")
        return True
    else:
        print("   ❌ Errore nella creazione della connessione")
        return False


def connect_sp01_to_hitl():
    """Connect SP01_EML_Parser success output to SP11_Security_Audit input"""
    print("\n🔗 [2/2] Connessione SP01_EML_Parser → SP11_Security_Audit (HITL)")
    
    # Get SP01 PG
    sp01_pg = get_process_group_by_name("SP01_EML_Parser")
    if not sp01_pg:
        print("   ⚠️  Process Group SP01_EML_Parser non trovato")
        return False
    
    sp01_id = sp01_pg['id']
    print(f"   ✓ Trovato SP01_EML_Parser: {sp01_id}")
    
    # Get SP11 PG (HITL Manager)
    sp11_pg = get_process_group_by_name("SP11_Security_Audit")
    if not sp11_pg:
        print("   ⚠️  Process Group SP11_Security_Audit non trovato")
        print("   💡 Questa connessione è opzionale per il POC base")
        return False
    
    sp11_id = sp11_pg['id']
    print(f"   ✓ Trovato SP11_Security_Audit: {sp11_id}")
    
    # Get SP01 output ports
    sp01_outputs = get_output_ports(sp01_id)
    if not sp01_outputs:
        print("   ⚠️  SP01 non ha Output Ports configurati")
        print("   💡 Crea manualmente un Output Port 'Success' in SP01_EML_Parser")
        return False
    
    # Find "Success" output port
    success_port = None
    for port in sp01_outputs:
        if 'Success' in port['component']['name'] or 'success' in port['component']['name'].lower():
            success_port = port
            break
    
    if not success_port:
        success_port = sp01_outputs[0]  # Fallback to first port
    
    print(f"   ✓ Trovato Output Port: {success_port['component']['name']}")
    
    # Get SP11 input ports
    sp11_inputs = get_input_ports(sp11_id)
    if not sp11_inputs:
        print("   ⚠️  SP11 non ha Input Ports configurati")
        print("   💡 Crea manualmente un Input Port 'From_SP01' in SP11_Security_Audit")
        return False
    
    # Get first input port
    sp11_input = sp11_inputs[0]
    print(f"   ✓ Trovato Input Port: {sp11_input['component']['name']}")
    
    # Check if connection already exists
    if connection_exists(success_port['id'], sp11_input['id']):
        print("   ✅ Connessione già esistente")
        return True
    
    # Create connection
    print("   🔧 Creazione connessione...")
    success = create_connection(
        source_id=success_port['id'],
        source_type="OUTPUT_PORT",
        source_group_id=sp01_id,
        dest_id=sp11_input['id'],
        dest_type="INPUT_PORT",
        dest_group_id=sp11_id
    )
    
    if success:
        print("   ✅ Connessione SP01 → HITL creata con successo!")
        return True
    else:
        print("   ❌ Errore nella creazione della connessione")
        return False


def main():
    print("=" * 70)
    print("  Connessione Process Groups - Workflow Completo")
    print("=" * 70)
    
    try:
        # Test NiFi connection
        print("\n🔍 Verifica connessione a NiFi...")
        response = requests.get(f"{NIFI_API}/system-diagnostics", timeout=5)
        response.raise_for_status()
        print("   ✅ NiFi API disponibile")
        
        # Connect Ingress to SP01
        ingress_connected = connect_ingress_to_sp01()
        
        # Connect SP01 to HITL
        hitl_connected = connect_sp01_to_hitl()
        
        # Summary
        print("\n" + "=" * 70)
        print("  📊 Riepilogo Connessioni")
        print("=" * 70)
        
        if ingress_connected:
            print("✅ Ingress_ContentListener → SP01_EML_Parser")
        else:
            print("⚠️  Ingress_ContentListener → SP01_EML_Parser (da creare manualmente)")
        
        if hitl_connected:
            print("✅ SP01_EML_Parser → SP11_Security_Audit (HITL)")
        else:
            print("⚠️  SP01_EML_Parser → SP11_Security_Audit (opzionale)")
        
        print("\n" + "=" * 70)
        
        if ingress_connected:
            print("✅ Workflow base configurato!")
            print("\n🧪 Test endpoint:")
            print("   curl -X POST http://localhost:9099/contentListener/fascicolo \\")
            print("        -H 'Content-Type: message/rfc822' \\")
            print("        -d '@test-email.eml'")
        else:
            print("⚠️  Configurazione incompleta - verifica i log sopra")
        
        print("=" * 70)
        
        # Exit code based on success
        sys.exit(0 if ingress_connected else 1)
        
    except KeyboardInterrupt:
        print("\n\n❌ Operazione annullata dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
