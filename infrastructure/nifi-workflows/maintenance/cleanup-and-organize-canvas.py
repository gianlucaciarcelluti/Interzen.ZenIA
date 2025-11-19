#!/usr/bin/env python3
"""
Cleanup and Organize NiFi Canvas
=================================
This script:
1. Removes duplicate processors
2. Stops and removes old ListenHTTP processors
3. Organizes the canvas layout in a clean flow
4. Keeps only the newest version of each processor

Usage:
    python3 cleanup-and-organize-canvas.py
"""

import requests
import json
import sys
from typing import Dict, List, Tuple
from collections import defaultdict

class NiFiCanvasOrganizer:
    def __init__(self, nifi_url: str = "http://localhost:8080"):
        self.nifi_url = nifi_url
        self.api_url = f"{nifi_url}/nifi-api"
        self.session = requests.Session()
        
    def get_root_pg_id(self) -> str:
        """Get root process group ID"""
        response = self.session.get(f"{self.api_url}/flow/process-groups/root")
        response.raise_for_status()
        return response.json()['processGroupFlow']['id']
    
    def get_all_processors(self) -> List[Dict]:
        """Get all processors in root process group"""
        root_id = self.get_root_pg_id()
        response = self.session.get(f"{self.api_url}/process-groups/{root_id}/processors")
        response.raise_for_status()
        return response.json()['processors']
    
    def stop_processor(self, processor_id: str, revision: Dict) -> bool:
        """Stop a processor"""
        try:
            update_data = {
                "revision": revision,
                "component": {
                    "id": processor_id,
                    "state": "STOPPED"
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
            print(f"   ⚠️  Errore stop processor: {e}")
            return False
    
    def delete_processor(self, processor_id: str, revision: Dict) -> bool:
        """Delete a processor"""
        try:
            params = {
                'version': revision['version'],
                'clientId': revision.get('clientId', 'cleanup-script')
            }
            
            response = self.session.delete(
                f"{self.api_url}/processors/{processor_id}",
                params=params
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore cancellazione processor: {e}")
            return False
    
    def get_connections_for_processor(self, processor_id: str) -> List[Dict]:
        """Get all connections involving a processor"""
        try:
            root_id = self.get_root_pg_id()
            response = self.session.get(f"{self.api_url}/process-groups/{root_id}/connections")
            response.raise_for_status()
            
            connections = response.json()['connections']
            return [
                conn for conn in connections
                if (conn['component']['source']['id'] == processor_id or
                    conn['component']['destination']['id'] == processor_id)
            ]
        except requests.exceptions.RequestException:
            return []
    
    def delete_connection(self, connection_id: str, revision: Dict) -> bool:
        """Delete a connection"""
        try:
            params = {
                'version': revision['version'],
                'clientId': revision.get('clientId', 'cleanup-script')
            }
            
            response = self.session.delete(
                f"{self.api_url}/connections/{connection_id}",
                params=params
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore cancellazione connessione: {e}")
            return False
    
    def update_processor_position(self, processor_id: str, revision: Dict, 
                                   x: float, y: float) -> bool:
        """Update processor position"""
        try:
            update_data = {
                "revision": revision,
                "component": {
                    "id": processor_id,
                    "position": {
                        "x": x,
                        "y": y
                    }
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
            print(f"   ⚠️  Errore update posizione: {e}")
            return False
    
    def find_duplicates(self, processors: List[Dict]) -> Dict[str, List[Dict]]:
        """Group processors by name to find duplicates"""
        groups = defaultdict(list)
        for p in processors:
            name = p['component']['name']
            groups[name].append(p)
        return dict(groups)
    
    def cleanup_and_organize(self):
        """Main cleanup and organization logic"""
        print("=" * 70)
        print("  Cleanup e Organizzazione Canvas NiFi")
        print("=" * 70)
        print()
        
        # Step 1: Get all processors
        print("[1/4] 🔍 Analisi canvas...")
        processors = self.get_all_processors()
        print(f"   Trovati {len(processors)} processors totali")
        print()
        
        # Step 2: Find and remove duplicates
        print("[2/4] 🧹 Rimozione duplicati...")
        duplicates = self.find_duplicates(processors)
        
        removed_count = 0
        kept_processors = []
        
        for name, proc_list in duplicates.items():
            if len(proc_list) > 1:
                print(f"\n   📌 {name}: {len(proc_list)} istanze trovate")
                
                # Keep the newest one (highest version)
                proc_list_sorted = sorted(
                    proc_list, 
                    key=lambda x: x['revision']['version'], 
                    reverse=True
                )
                
                to_keep = proc_list_sorted[0]
                to_remove = proc_list_sorted[1:]
                
                kept_processors.append(to_keep)
                print(f"      ✅ Mantengo versione {to_keep['revision']['version']}")
                
                # Remove duplicates
                for proc in to_remove:
                    proc_id = proc['id']
                    proc_rev = proc['revision']
                    
                    # First stop if running
                    if proc['component']['state'] == 'RUNNING':
                        print(f"      🛑 Stop processor...")
                        self.stop_processor(proc_id, proc_rev)
                        # Re-fetch revision after stop
                        updated = self.session.get(f"{self.api_url}/processors/{proc_id}")
                        proc_rev = updated.json()['revision']
                    
                    # Delete connections
                    connections = self.get_connections_for_processor(proc_id)
                    for conn in connections:
                        self.delete_connection(conn['id'], conn['revision'])
                    
                    # Delete processor
                    if self.delete_processor(proc_id, proc_rev):
                        print(f"      🗑️  Rimosso duplicato versione {proc_rev['version']}")
                        removed_count += 1
            else:
                kept_processors.append(proc_list[0])
        
        print(f"\n   ✅ Rimossi {removed_count} duplicati")
        print()
        
        # Step 3: Remove old ListenHTTP processors
        print("[3/4] 🧹 Rimozione processors obsoleti...")
        
        listen_http_removed = 0
        for proc in kept_processors[:]:  # Copy list to allow modification
            if proc['component']['type'] == 'org.apache.nifi.processors.standard.ListenHTTP':
                proc_id = proc['id']
                proc_name = proc['component']['name']
                proc_rev = proc['revision']
                
                print(f"   🔍 Trovato ListenHTTP obsoleto: {proc_name}")
                
                # Stop if running
                if proc['component']['state'] == 'RUNNING':
                    print(f"      🛑 Stop processor...")
                    self.stop_processor(proc_id, proc_rev)
                    # Re-fetch revision
                    updated = self.session.get(f"{self.api_url}/processors/{proc_id}")
                    proc_rev = updated.json()['revision']
                
                # Delete connections
                connections = self.get_connections_for_processor(proc_id)
                for conn in connections:
                    self.delete_connection(conn['id'], conn['revision'])
                
                # Delete processor
                if self.delete_processor(proc_id, proc_rev):
                    print(f"      🗑️  Rimosso ListenHTTP")
                    listen_http_removed += 1
                    kept_processors.remove(proc)
        
        print(f"   ✅ Rimossi {listen_http_removed} processors obsoleti")
        print()
        
        # Step 4: Organize layout
        print("[4/4] 📐 Organizzazione layout canvas...")
        
        # Define clean layout positions (vertical flow)
        layout = {
            'ContentListener_Fascicolo': (200, 100),    # HandleHttpRequest
            'Generate_Workflow_ID': (200, 250),         # UpdateAttribute
            'Log_Incoming_Request': (200, 400),         # LogAttribute
            'Route_To_Workflow': (200, 550),            # RouteOnAttribute
            'Send_Response_To_Client': (200, 700),      # HandleHttpResponse
            'Test_HTTP_Endpoint': (600, 100),           # HandleHttpRequest (test)
        }
        
        organized = 0
        for proc in kept_processors:
            name = proc['component']['name']
            if name in layout:
                x, y = layout[name]
                current_x = proc['component']['position']['x']
                current_y = proc['component']['position']['y']
                
                # Only update if position is different
                if current_x != x or current_y != y:
                    if self.update_processor_position(
                        proc['id'], 
                        proc['revision'], 
                        x, 
                        y
                    ):
                        print(f"   📍 {name}: ({current_x}, {current_y}) → ({x}, {y})")
                        organized += 1
        
        print(f"\n   ✅ Organizzati {organized} processors")
        print()
        
        # Summary
        print("=" * 70)
        print("  ✅ Cleanup Completato")
        print("=" * 70)
        print()
        print("📊 Riepilogo:")
        print(f"   - Duplicati rimossi: {removed_count}")
        print(f"   - Processors obsoleti rimossi: {listen_http_removed}")
        print(f"   - Processors riorganizzati: {organized}")
        print(f"   - Processors rimanenti: {len(kept_processors)}")
        print()
        print("🎨 Canvas organizzato con layout pulito!")
        print(f"   Visualizza: {self.nifi_url}/nifi")
        print()

def main():
    try:
        organizer = NiFiCanvasOrganizer()
        organizer.cleanup_and_organize()
        
    except KeyboardInterrupt:
        print("\n\n❌ Operazione annullata dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
