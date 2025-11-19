#!/usr/bin/env python3
"""
Rebuild and Complete Ingress Endpoint
======================================
This script rebuilds the complete ingress endpoint workflow:
1. Creates HandleHttpRequest listener on port 9099
2. Connects all processors in the correct flow
3. Starts all processors
4. Connects to SP01 Process Group

Flow: HTTP Request → Generate ID → Log → Route → [SP01 / Response]
"""

import requests
import json
import sys
from typing import Dict, Optional

class NiFiWorkflowBuilder:
    def __init__(self, nifi_url: str = "http://localhost:8080"):
        self.nifi_url = nifi_url
        self.api_url = f"{nifi_url}/nifi-api"
        self.session = requests.Session()
        
    def get_root_pg_id(self) -> str:
        """Get root process group ID"""
        response = self.session.get(f"{self.api_url}/flow/process-groups/root")
        response.raise_for_status()
        return response.json()['processGroupFlow']['id']
    
    def create_processor(self, name: str, processor_type: str, 
                         x: float, y: float, config: Optional[Dict] = None) -> Optional[str]:
        """Create a processor"""
        try:
            root_id = self.get_root_pg_id()
            
            processor_data = {
                "revision": {"version": 0},
                "component": {
                    "type": processor_type,
                    "name": name,
                    "position": {"x": x, "y": y},
                    "config": config or {}
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{root_id}/processors",
                json=processor_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            processor_id = response.json()['id']
            print(f"   ✅ Creato: {name} ({processor_id})")
            return processor_id
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Errore creazione {name}: {e}")
            return None
    
    def get_processor_by_name(self, name: str) -> Optional[Dict]:
        """Find processor by name"""
        try:
            root_id = self.get_root_pg_id()
            response = self.session.get(f"{self.api_url}/process-groups/{root_id}/processors")
            response.raise_for_status()
            
            processors = response.json()['processors']
            for p in processors:
                if p['component']['name'] == name:
                    return p
            return None
            
        except requests.exceptions.RequestException:
            return None
    
    def create_connection(self, source_id: str, dest_id: str, 
                          relationships: list, source_type: str = "PROCESSOR",
                          dest_type: str = "PROCESSOR") -> bool:
        """Create connection between processors"""
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
                        "id": dest_id,
                        "type": dest_type,
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
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Connessione già esistente o errore: {e}")
            return False
    
    def start_processor(self, processor_id: str) -> bool:
        """Start a processor"""
        try:
            response = self.session.get(f"{self.api_url}/processors/{processor_id}")
            response.raise_for_status()
            processor_data = response.json()
            
            if processor_data['component']['state'] == 'RUNNING':
                return True
            
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
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore avvio processor: {e}")
            return False
    
    def get_sp01_input_port(self) -> Optional[str]:
        """Find SP01 Process Group Input Port ID"""
        try:
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
                return None
            
            sp01_id = sp01_pg['id']
            response = self.session.get(f"{self.api_url}/process-groups/{sp01_id}/input-ports")
            response.raise_for_status()
            
            input_ports = response.json()['inputPorts']
            if input_ports:
                return input_ports[0]['id']
            return None
            
        except requests.exceptions.RequestException:
            return None
    
    def rebuild_workflow(self):
        """Rebuild complete ingress endpoint workflow"""
        print("=" * 70)
        print("  Ricostruzione Completa Ingress Endpoint")
        print("=" * 70)
        print()
        
        # Step 1: Create HandleHttpRequest if missing
        print("[1/4] 🔧 Verifica/creazione HandleHttpRequest...")
        
        http_listener = self.get_processor_by_name("ContentListener_Fascicolo")
        
        if not http_listener:
            print("   📌 HandleHttpRequest non trovato, creo nuovo...")
            http_listener_id = self.create_processor(
                name="ContentListener_Fascicolo",
                processor_type="org.apache.nifi.processors.standard.HandleHttpRequest",
                x=200.0,
                y=100.0,
                config={
                    "properties": {
                        "Listening Port": "9099",
                        "Allowed Paths": "/contentListener/fascicolo"
                    }
                }
            )
            if not http_listener_id:
                print("   ❌ Impossibile creare HandleHttpRequest")
                return
        else:
            http_listener_id = http_listener['id']
            print(f"   ✅ HandleHttpRequest esistente: {http_listener_id}")
        
        print()
        
        # Step 2: Get all other processors
        print("[2/4] 🔍 Ricerca altri processors...")
        
        processors = {
            'generate_id': self.get_processor_by_name("Generate_Workflow_ID"),
            'log': self.get_processor_by_name("Log_Incoming_Request"),
            'route': self.get_processor_by_name("Route_To_Workflow"),
            'response': self.get_processor_by_name("Send_Response_To_Client")
        }
        
        all_found = all(processors.values())
        
        if all_found:
            print("   ✅ Tutti i processors trovati")
        else:
            print("   ❌ Alcuni processors mancano:")
            for key, proc in processors.items():
                if not proc:
                    print(f"      - {key}")
            return
        
        print()
        
        # Step 3: Create connections
        print("[3/4] 🔗 Creazione connessioni workflow...")
        
        connections_created = 0
        
        # Safely extract processor objects
        gen = processors.get('generate_id')
        log = processors.get('log')
        route = processors.get('route')
        resp = processors.get('response')
        
        # HTTP Request → Generate ID
        if gen and self.create_connection(http_listener_id, gen['id'], ["success"]):
            print("   ✅ HTTP Request → Generate ID")
            connections_created += 1
        
        # Generate ID → Log
        if gen and log and self.create_connection(gen['id'], log['id'], ["success"]):
            print("   ✅ Generate ID → Log")
            connections_created += 1
        
        # Log → Route
        if log and route and self.create_connection(log['id'], route['id'], ["success"]):
            print("   ✅ Log → Route")
            connections_created += 1
        
        # Route → Response (unmatched)
        if route and resp and self.create_connection(route['id'], resp['id'], ["unmatched"]):
            print("   ✅ Route → Response (unmatched)")
            connections_created += 1
        
        # Response → HTTP Request (completion)
        if resp and self.create_connection(resp['id'], http_listener_id, ["success"]):
            print("   ✅ Response → HTTP Request (completion)")
            connections_created += 1
        
        # Route → SP01 (if exists)
        sp01_port = self.get_sp01_input_port()
        if sp01_port:
            if route and self.create_connection(
                route['id'], 
                sp01_port, 
                ["eml"],
                source_type="PROCESSOR",
                dest_type="INPUT_PORT"
            ):
                print("   ✅ Route → SP01 Input Port (eml)")
                connections_created += 1
        else:
            print("   ⚠️  SP01 Input Port non trovato, skip connessione")
        
        # Start processors that exist (guard against None values)
        started = 0
        all_processor_ids = [http_listener_id] + [
            p['id'] for p in processors.values() if p and isinstance(p, dict) and 'id' in p
        ]
        
        for proc_id in all_processor_ids:
            if self.start_processor(proc_id):
                started += 1
        
        print(f"   ✅ Avviati {started}/{len(all_processor_ids)} processors")
        print()
        
        # Summary
        print("=" * 70)
        print("  ✅ Workflow Completo e Attivo")
        print("=" * 70)
        print()
        print("📊 Endpoint disponibile:")
        print("   http://localhost:9099/contentListener/fascicolo")
        print()
        print("🧪 Test:")
        print('   curl -X POST http://localhost:9099/contentListener/fascicolo \\')
        print('        -H "Content-Type: application/json" \\')
        print('        -d \'{"test": "workflow completo"}\'')
        print()

def main():
    try:
        builder = NiFiWorkflowBuilder()
        builder.rebuild_workflow()
        
    except KeyboardInterrupt:
        print("\n\n❌ Operazione annullata")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
