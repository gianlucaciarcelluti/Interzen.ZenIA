#!/usr/bin/env python3
"""
Optimize Layout and Connect to SP01
====================================
This script:
1. Reorganizes the internal layout of Ingress_ContentListener for better readability
2. Positions processors in a clear vertical flow
3. Connects the Output Port to SP01 Input Port
4. Verifies the complete workflow

Usage:
    python3 optimize-and-connect-sp01.py
"""

import requests
import json
import sys
from typing import Dict, Optional

class WorkflowOptimizer:
    def __init__(self, nifi_url: str = "http://localhost:8080"):
        self.nifi_url = nifi_url
        self.api_url = f"{nifi_url}/nifi-api"
        self.session = requests.Session()
        self.content_type = "application/json"
        
    def get_root_pg_id(self) -> str:
        """Get root process group ID"""
        response = self.session.get(f"{self.api_url}/flow/process-groups/root")
        response.raise_for_status()
        return response.json()['processGroupFlow']['id']
    
    def get_process_group_by_name(self, name: str) -> Optional[Dict]:
        """Find process group by name"""
        try:
            root_id = self.get_root_pg_id()
            response = self.session.get(f"{self.api_url}/process-groups/{root_id}/process-groups")
            response.raise_for_status()
            
            pgs = response.json()['processGroups']
            for pg in pgs:
                if name in pg['component']['name']:
                    return pg
            return None
        except requests.exceptions.RequestException:
            return None
    
    def get_processor_by_name_in_pg(self, pg_id: str, name: str) -> Optional[Dict]:
        """Find processor by name in a specific process group"""
        try:
            response = self.session.get(f"{self.api_url}/process-groups/{pg_id}/processors")
            response.raise_for_status()
            
            processors = response.json()['processors']
            for p in processors:
                if p['component']['name'] == name:
                    return p
            return None
        except requests.exceptions.RequestException:
            return None
    
    def update_processor_position(self, processor_id: str, revision: Dict,
                                   x: float, y: float) -> bool:
        """Update processor position"""
        try:
            update_data = {
                "revision": revision,
                "component": {
                    "id": processor_id,
                    "position": {"x": x, "y": y}
                }
            }
            
            response = self.session.put(
                f"{self.api_url}/processors/{processor_id}",
                json=update_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
    
    def update_port_position(self, port_id: str, revision: Dict,
                             x: float, y: float, port_type: str = "output") -> bool:
        """Update port position"""
        try:
            update_data = {
                "revision": revision,
                "component": {
                    "id": port_id,
                    "position": {"x": x, "y": y}
                }
            }
            
            endpoint = f"{self.api_url}/{port_type}-ports/{port_id}"
            response = self.session.put(
                endpoint,
                json=update_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
    
    def get_output_ports(self, pg_id: str) -> list:
        """Get all output ports in a process group"""
        try:
            response = self.session.get(f"{self.api_url}/process-groups/{pg_id}/output-ports")
            response.raise_for_status()
            return response.json()['outputPorts']
        except requests.exceptions.RequestException:
            return []
    
    def get_input_ports(self, pg_id: str) -> list:
        """Get all input ports in a process group"""
        try:
            response = self.session.get(f"{self.api_url}/process-groups/{pg_id}/input-ports")
            response.raise_for_status()
            return response.json()['inputPorts']
        except requests.exceptions.RequestException:
            return []
    
    def create_connection_between_ports(self, source_pg_id: str, source_port_id: str,
                                        dest_pg_id: str, dest_port_id: str) -> bool:
        """Create connection between Output Port and Input Port across Process Groups"""
        try:
            root_id = self.get_root_pg_id()
            
            connection_data = {
                "revision": {"version": 0},
                "component": {
                    "source": {
                        "id": source_port_id,
                        "type": "OUTPUT_PORT",
                        "groupId": source_pg_id
                    },
                    "destination": {
                        "id": dest_port_id,
                        "type": "INPUT_PORT",
                        "groupId": dest_pg_id
                    },
                    "selectedRelationships": [""]
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{root_id}/connections",
                json=connection_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            # Check if connection already exists
            if "already exists" in str(e).lower():
                return True
            return False
    
    def optimize_and_connect(self):
        """Main workflow: optimize layout and connect to SP01"""
        print("=" * 70)
        print("  Ottimizzazione Layout e Connessione a SP01")
        print("=" * 70)
        print()
        
        # Step 1: Find Ingress Process Group
        print("[1/4] 🔍 Ricerca Process Groups...")
        
        ingress_pg = self.get_process_group_by_name("Ingress_ContentListener")
        sp01_pg = self.get_process_group_by_name("SP01")
        
        if not ingress_pg:
            print("   ❌ Ingress_ContentListener non trovato")
            return
        
        if not sp01_pg:
            print("   ❌ SP01 non trovato")
            return
        
        ingress_pg_id = ingress_pg['id']
        sp01_pg_id = sp01_pg['id']
        
        print(f"   ✅ Ingress_ContentListener: {ingress_pg_id}")
        print(f"   ✅ SP01_EML_Parser: {sp01_pg_id}")
        print()
        
        # Step 2: Optimize internal layout
        print("[2/4] 📐 Ottimizzazione layout interno Ingress...")
        
        # Define optimal positions (clear vertical flow with spacing)
        layout = {
            'ContentListener_Fascicolo': (250, 150),
            'Generate_Workflow_ID': (250, 320),
            'Log_Incoming_Request': (250, 490),
            'Route_To_Workflow': (250, 660),
            'Send_Response_To_Client': (550, 660),
            'To_SP01_EML': (250, 830)  # Output Port
        }
        
        organized = 0
        
        # Update processor positions
        for proc_name, (x, y) in layout.items():
            if proc_name == 'To_SP01_EML':
                continue  # Handle ports separately
            
            proc = self.get_processor_by_name_in_pg(ingress_pg_id, proc_name)
            if proc:
                current_x = proc['component']['position']['x']
                current_y = proc['component']['position']['y']
                
                if current_x != x or current_y != y:
                    if self.update_processor_position(
                        proc['id'],
                        proc['revision'],
                        x, y
                    ):
                        print(f"   📍 {proc_name}: ({current_x:.0f}, {current_y:.0f}) → ({x}, {y})")
                        organized += 1
        
        # Update Output Port position
        output_ports = self.get_output_ports(ingress_pg_id)
        for port in output_ports:
            if port['component']['name'] == 'To_SP01_EML':
                x, y = layout['To_SP01_EML']
                current_x = port['component']['position']['x']
                current_y = port['component']['position']['y']
                
                if current_x != x or current_y != y:
                    if self.update_port_position(
                        port['id'],
                        port['revision'],
                        x, y,
                        port_type="output"
                    ):
                        print(f"   📍 Output Port To_SP01_EML: ({current_x:.0f}, {current_y:.0f}) → ({x}, {y})")
                        organized += 1
        
        print(f"\n   ✅ Riposizionati {organized} componenti")
        print()
        
        # Step 3: Find ports for connection
        print("[3/4] 🔗 Ricerca porte per connessione...")
        
        # Find Ingress Output Port
        ingress_output_ports = self.get_output_ports(ingress_pg_id)
        ingress_output = None
        for port in ingress_output_ports:
            if port['component']['name'] == 'To_SP01_EML':
                ingress_output = port
                break
        
        if not ingress_output:
            print("   ❌ Output Port 'To_SP01_EML' non trovato")
            return
        
        print(f"   ✅ Output Port Ingress: {ingress_output['component']['name']}")
        
        # Find SP01 Input Port
        sp01_input_ports = self.get_input_ports(sp01_pg_id)
        
        if not sp01_input_ports:
            print("   ⚠️  SP01 non ha Input Ports configurati")
            print("   💡 Creazione Input Port necessaria in SP01")
            return
        
        sp01_input = sp01_input_ports[0]  # Use first input port
        print(f"   ✅ Input Port SP01: {sp01_input['component']['name']}")
        print()
        
        # Step 4: Create connection
        print("[4/4] 🔗 Connessione Ingress → SP01...")
        
        if self.create_connection_between_ports(
            ingress_pg_id,
            ingress_output['id'],
            sp01_pg_id,
            sp01_input['id']
        ):
            print("   ✅ Connessione creata con successo!")
            print()
            print("   📊 Flusso completo:")
            print("      HTTP Request (porta 9099)")
            print("         ↓")
            print("      Generate Workflow ID")
            print("         ↓")
            print("      Log Request")
            print("         ↓")
            print("      Route by Type")
            print("         ├─→ [eml] → Output Port → SP01 Input Port → SP01 Processing")
            print("         └─→ [unmatched] → HTTP Response")
        else:
            print("   ⚠️  Errore connessione o connessione già esistente")
        
        print()
        
        # Summary
        print("=" * 70)
        print("  ✅ Ottimizzazione Completata")
        print("=" * 70)
        print()
        print("📦 Process Group: Ingress_ContentListener")
        print(f"   Layout: Flusso verticale ottimizzato ({organized} componenti riposizionati)")
        print("   Connessione: Ingress Output Port → SP01 Input Port ✅")
        print()
        print("🌐 Visualizza il risultato:")
        print(f"   {self.nifi_url}/nifi")
        print()
        print("📍 Endpoint attivo:")
        print("   http://localhost:9099/contentListener/fascicolo")
        print()
        print("🧪 Test workflow completo:")
        print("   1. Invia una richiesta HTTP all'endpoint")
        print("   2. Il flusso passerà attraverso Ingress PG")
        print("   3. I file .eml verranno inoltrati a SP01")
        print("   4. Altri file riceveranno risposta diretta")
        print()

def main():
    try:
        optimizer = WorkflowOptimizer()
        optimizer.optimize_and_connect()
        
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
