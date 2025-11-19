#!/usr/bin/env python3
"""
Complete Ingress Endpoint Setup
================================
This script completes the setup of the /contentListener/fascicolo ingress endpoint by:
1. Starting all created processors
2. Connecting RouteOnAttribute to SP01 Input Port
3. Verifying the complete workflow

Usage:
    python3 complete-ingress-setup.py
"""

import requests
import json
import sys
from typing import Dict, List, Optional

class NiFiWorkflowCompleter:
    def __init__(self, nifi_url: str = "http://localhost:8080"):
        self.nifi_url = nifi_url
        self.api_url = f"{nifi_url}/nifi-api"
        self.session = requests.Session()
        
    def get_root_pg_id(self) -> str:
        """Get root process group ID"""
        response = self.session.get(f"{self.api_url}/flow/process-groups/root")
        response.raise_for_status()
        return response.json()['processGroupFlow']['id']
    
    def get_processors_by_name(self, processor_name: str) -> List[Dict]:
        """Find processors by name pattern"""
        root_id = self.get_root_pg_id()
        response = self.session.get(f"{self.api_url}/process-groups/{root_id}/processors")
        response.raise_for_status()
        
        processors = response.json()['processors']
        return [p for p in processors if processor_name in p['component']['name']]
    
    def get_processor_by_name(self, processor_name: str) -> Optional[Dict]:
        """Find a single processor by exact name"""
        processors = self.get_processors_by_name(processor_name)
        if not processors:
            return None
        return processors[0]
    
    def start_processor(self, processor_id: str) -> bool:
        """Start a processor"""
        try:
            # Get current processor state
            response = self.session.get(f"{self.api_url}/processors/{processor_id}")
            response.raise_for_status()
            processor_data = response.json()
            
            # Check if already running
            if processor_data['component']['state'] == 'RUNNING':
                print(f"✅ Processor {processor_data['component']['name']} già in esecuzione")
                return True
            
            # Update to RUNNING state
            update_data = {
                "revision": processor_data['revision'],
                "component": {
                    "id": processor_id,
                    "state": "RUNNING"
                }
            }
            
            response = self.session.put(
                f"{self.api_url}/processors/{processor_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            print(f"✅ Avviato processor: {processor_data['component']['name']}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Errore avvio processor {processor_id}: {e}")
            return False
    
    def get_sp01_input_port(self) -> Optional[Dict]:
        """Find SP01 Process Group Input Port"""
        try:
            # First find SP01 Process Group
            root_id = self.get_root_pg_id()
            response = self.session.get(f"{self.api_url}/process-groups/{root_id}/process-groups")
            response.raise_for_status()
            
            process_groups = response.json()['processGroups']
            sp01_pg = None
            for pg in process_groups:
                if 'SP01' in pg['component']['name']:
                    sp01_pg = pg
                    break
            
            if not sp01_pg:
                print("❌ Process Group SP01 non trovato")
                return None
            
            sp01_id = sp01_pg['id']
            print(f"✅ Trovato SP01 Process Group: {sp01_id}")
            
            # Get input ports of SP01
            response = self.session.get(f"{self.api_url}/process-groups/{sp01_id}/input-ports")
            response.raise_for_status()
            
            input_ports = response.json()['inputPorts']
            if not input_ports:
                print("⚠️  SP01 non ha Input Ports configurati")
                return None
            
            # Return the first input port (usually there's only one)
            input_port = input_ports[0]
            print(f"✅ Trovato Input Port: {input_port['component']['name']} ({input_port['id']})")
            return input_port
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Errore ricerca Input Port SP01: {e}")
            return None
    
    def create_connection(self, source_id: str, source_type: str, 
                          destination_id: str, destination_type: str,
                          relationships: List[str]) -> bool:
        """Create connection between processors/ports"""
        try:
            root_id = self.get_root_pg_id()
            
            connection_data = {
                "revision": {"version": 0},
                "component": {
                    "source": {
                        "id": source_id,
                        "type": source_type,
                        "groupId": root_id
                    },
                    "destination": {
                        "id": destination_id,
                        "type": destination_type,
                        "groupId": root_id
                    },
                    "selectedRelationships": relationships
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{root_id}/connections",
                json=connection_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            print(f"✅ Connessione creata: {source_type} → {destination_type}")
            return True
            
        except requests.exceptions.RequestException as e:
            error_detail = ""
            if e.response is not None and hasattr(e.response, 'text'):
                error_detail = e.response.text
            print(f"❌ Errore creazione connessione: {e}")
            print(f"   Dettagli: {error_detail}")
            return False
    
    def check_existing_connection(self, source_id: str, destination_id: str) -> bool:
        """Check if connection already exists"""
        try:
            root_id = self.get_root_pg_id()
            response = self.session.get(f"{self.api_url}/process-groups/{root_id}/connections")
            response.raise_for_status()
            
            connections = response.json()['connections']
            for conn in connections:
                if (conn['component']['source']['id'] == source_id and 
                    conn['component']['destination']['id'] == destination_id):
                    return True
            return False
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Errore verifica connessioni esistenti: {e}")
            return False

    def complete_setup(self):
        """Complete the ingress endpoint setup"""
        print("=" * 60)
        print("  Completamento Setup Ingress Endpoint")
        print("=" * 60)
        print()
        
        # Step 1: Find all ingress processors
        print("[1/3] 🔍 Ricerca processors creati...")
        
        processor_names = [
            "HTTP Request Handler",
            "Add Workflow ID",
            "Log Request",
            "Route by Type",
            "HTTP Response"
        ]
        
        processors_to_start = []
        for name in processor_names:
            processor = self.get_processor_by_name(name)
            if processor:
                processors_to_start.append(processor)
                print(f"   ✅ Trovato: {name}")
            else:
                print(f"   ⚠️  Non trovato: {name}")
        
        print()
        
        # Step 2: Start all processors
        print("[2/3] 🚀 Avvio processors...")
        started = 0
        for processor in processors_to_start:
            if self.start_processor(processor['id']):
                started += 1
        
        print(f"\n   ✅ Avviati {started}/{len(processors_to_start)} processors")
        print()
        
        # Step 3: Connect RouteOnAttribute to SP01
        print("[3/3] 🔗 Connessione RouteOnAttribute → SP01...")
        
        route_processor = self.get_processor_by_name("Route by Type")
        sp01_input_port = self.get_sp01_input_port()
        
        if route_processor and sp01_input_port:
            # Check if connection already exists
            if self.check_existing_connection(route_processor['id'], sp01_input_port['id']):
                print("   ✅ Connessione già esistente")
            else:
                # Create connection for 'eml' relationship
                success = self.create_connection(
                    source_id=route_processor['id'],
                    source_type="PROCESSOR",
                    destination_id=sp01_input_port['id'],
                    destination_type="INPUT_PORT",
                    relationships=["eml"]
                )
                
                if success:
                    print("   ✅ Connessione creata con successo")
                else:
                    print("   ❌ Errore nella creazione della connessione")
                    print()
                    print("   💡 Connessione manuale richiesta:")
                    print("      1. Apri NiFi UI: http://localhost:8080/nifi")
                    print("      2. Trascina una connessione da 'Route by Type'")
                    print("      3. Seleziona relationship: 'eml'")
                    print("      4. Collega a SP01 Input Port")
        else:
            if not route_processor:
                print("   ❌ RouteOnAttribute processor non trovato")
            if not sp01_input_port:
                print("   ❌ SP01 Input Port non trovato")
            print()
            print("   💡 Verifica che SP01 Process Group sia stato creato correttamente")
        
        print()
        print("=" * 60)
        print("  ✅ Setup Completato")
        print("=" * 60)
        print()
        print("📊 Riepilogo:")
        print(f"   - Processors avviati: {started}/{len(processors_to_start)}")
        print("   - Endpoint disponibile: http://localhost:9099/contentListener/fascicolo")
        print()
        print("🧪 Test workflow:")
        print('   curl -X POST http://localhost:9099/contentListener/fascicolo \\')
        print('        -H "Content-Type: application/json" \\')
        print('        -d \'{"test": "ingress endpoint"}\'')
        print()

def main():
    try:
        completer = NiFiWorkflowCompleter()
        completer.complete_setup()
        
    except KeyboardInterrupt:
        print("\n\n❌ Operazione annullata dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
