#!/usr/bin/env python3
"""
Add Input Port to SP01 Process Group
=====================================
Creates an Input Port in SP01_EML_Parser to receive files from Ingress

Usage:
    python3 add-sp01-input-port.py
"""

import requests
import sys
from typing import Optional, List

class SP01InputPortCreator:
    def __init__(self, nifi_url: str = "http://localhost:8080"):
        self.nifi_url = nifi_url
        self.api_url = f"{nifi_url}/nifi-api"
        self.session = requests.Session()
        
    def get_root_pg_id(self) -> str:
        """Get root process group ID"""
        response = self.session.get(f"{self.api_url}/flow/process-groups/root")
        response.raise_for_status()
        return response.json()['processGroupFlow']['id']
    
    def get_sp01_pg(self):
        """Find SP01 Process Group"""
        root_id = self.get_root_pg_id()
        response = self.session.get(f"{self.api_url}/process-groups/{root_id}/process-groups")
        response.raise_for_status()
        
        pgs = response.json()['processGroups']
        for pg in pgs:
            if 'SP01' in pg['component']['name']:
                return pg
        return None
    
    def create_input_port(self, pg_id: str, name: str = "From_Ingress", x: float = 100, y: float = 100):
        """Create Input Port in Process Group"""
        try:
            port_data = {
                "revision": {"version": 0},
                "component": {
                    "name": name,
                    "position": {"x": x, "y": y}
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{pg_id}/input-ports",
                json=port_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Errore creazione Input Port: {e}")
            return None
    
    def get_processor_by_name(self, pg_id: str, name_pattern: str):
        """Find processor by name pattern"""
        response = self.session.get(f"{self.api_url}/process-groups/{pg_id}/processors")
        response.raise_for_status()
        
        processors = response.json()['processors']
        for p in processors:
            if name_pattern.lower() in p['component']['name'].lower():
                return p
        return None
    def create_connection(self, pg_id: str, source_id: str, dest_id: str,
                          source_type: str = "INPUT_PORT", dest_type: str = "PROCESSOR",
                          relationships: Optional[List[str]] = None):
        """Create connection inside Process Group"""
        try:
            if relationships is None:
                relationships = [""]
                relationships = [""]
            
            connection_data = {
                "revision": {"version": 0},
                "component": {
                    "source": {
                        "id": source_id,
                        "type": source_type,
                        "groupId": pg_id
                    },
                    "destination": {
                        "id": dest_id,
                        "type": dest_type,
                        "groupId": pg_id
                    },
                    "selectedRelationships": relationships
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{pg_id}/connections",
                json=connection_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore connessione: {e}")
            return False
    
    def setup_sp01_input(self):
        """Setup Input Port in SP01 and connect to HTTP_Endpoint"""
        print("=" * 70)
        print("  Configurazione Input Port per SP01")
        print("=" * 70)
        print()
        
        # Find SP01
        print("[1/3] 🔍 Ricerca SP01 Process Group...")
        sp01_pg = self.get_sp01_pg()
        
        if not sp01_pg:
            print("   ❌ SP01_EML_Parser non trovato")
            return
        
        sp01_id = sp01_pg['id']
        sp01_name = sp01_pg['component']['name']
        print(f"   ✅ Trovato: {sp01_name}")
        print(f"   ID: {sp01_id}")
        print()
        
        # Check if Input Port already exists
        print("[2/3] 📥 Verifica/creazione Input Port...")
        
        response = self.session.get(f"{self.api_url}/process-groups/{sp01_id}/input-ports")
        input_ports = response.json()['inputPorts']
        
        input_port = None
        for port in input_ports:
            if 'Ingress' in port['component']['name'] or 'From' in port['component']['name']:
                input_port = port
                break
        
        if input_port:
            print(f"   ✅ Input Port già esistente: {input_port['component']['name']}")
            input_port_id = input_port['id']
        else:
            # Create new Input Port
            print("   📌 Creazione nuovo Input Port...")
            result = self.create_input_port(sp01_id, "From_Ingress", x=100, y=100)
            
            if result:
                input_port_id = result['id']
                print(f"   ✅ Input Port creato: From_Ingress")
                print(f"   ID: {input_port_id}")
            else:
                print("   ❌ Impossibile creare Input Port")
                return
        
        print()
        
        # Connect Input Port to first processor (HTTP_Endpoint or Call_SP01)
        print("[3/3] 🔗 Connessione Input Port → Processor...")
        
        # Try to find Call_SP01_Microservice or HTTP_Endpoint
        http_endpoint = self.get_processor_by_name(sp01_id, "HTTP_Endpoint")
        call_sp01 = self.get_processor_by_name(sp01_id, "Call_SP01")
        
        target_processor = call_sp01 if call_sp01 else http_endpoint
        
        if target_processor:
            target_name = target_processor['component']['name']
            target_id = target_processor['id']
            
            print(f"   🎯 Target processor: {target_name}")
            
            # Create connection
            if self.create_connection(
                sp01_id,
                input_port_id,
                target_id,
                source_type="INPUT_PORT",
                dest_type="PROCESSOR",
                relationships=[""]
            ):
                print(f"   ✅ Input Port → {target_name}")
            else:
                print("   ⚠️  Connessione già esistente o errore")
        else:
            print("   ⚠️  Nessun processor target trovato in SP01")
            print("   💡 Connetti manualmente Input Port al primo processor")
        
        print()
        
        # Summary
        print("=" * 70)
        print("  ✅ Input Port Configurato")
        print("=" * 70)
        print()
        print("📥 SP01 Input Port: From_Ingress")
        print(f"   Process Group: {sp01_name}")
        print("   Pronto per ricevere dati da Ingress_ContentListener")
        print()
        print("🔗 Prossimo passo:")
        print("   Esegui: python3 optimize-and-connect-sp01.py")
        print("   per completare la connessione Ingress → SP01")
        print()

def main():
    try:
        creator = SP01InputPortCreator()
        creator.setup_sp01_input()
        
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
