#!/usr/bin/env python3
"""
Create Ingress Process Group
=============================
This script organizes the ingress endpoint workflow into a clean Process Group:
1. Creates "Ingress_ContentListener" Process Group
2. Moves all ingress processors into the PG
3. Creates Output Port for SP01 integration
4. Organizes internal layout
5. Creates connections

Usage:
    python3 create-ingress-process-group.py
"""

import requests
import json
import sys
from typing import Dict, List, Optional

class IngressProcessGroupBuilder:
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
    
    def create_process_group(self, name: str, x: float = 100, y: float = 100) -> Optional[str]:
        """Create a new Process Group"""
        try:
            root_id = self.get_root_pg_id()
            
            pg_data = {
                "revision": {"version": 0},
                "component": {
                    "name": name,
                    "position": {
                        "x": x,
                        "y": y
                    }
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{root_id}/process-groups",
                json=pg_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            
            pg_id = response.json()['id']
            print(f"✅ Process Group creato: {name} ({pg_id})")
            return pg_id
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Errore creazione Process Group: {e}")
            return None
    
    def get_processor_by_name(self, name: str, pg_id: Optional[str] = None) -> Optional[Dict]:
        """Find processor by name"""
        try:
            if not pg_id:
                pg_id = self.get_root_pg_id()
            
            response = self.session.get(f"{self.api_url}/process-groups/{pg_id}/processors")
            response.raise_for_status()
            
            processors = response.json()['processors']
            for p in processors:
                if p['component']['name'] == name:
                    return p
            return None
            
        except requests.exceptions.RequestException:
            return None
    
    def get_all_connections(self, pg_id: str) -> List[Dict]:
        """Get all connections in a process group"""
        try:
            response = self.session.get(f"{self.api_url}/process-groups/{pg_id}/connections")
            response.raise_for_status()
            return response.json()['connections']
        except requests.exceptions.RequestException:
            return []
    
    def delete_connection(self, connection_id: str, revision: Dict) -> bool:
        """Delete a connection"""
        try:
            params = {
                'version': revision['version'],
                'clientId': revision.get('clientId', 'script')
            }
            
            response = self.session.delete(
                f"{self.api_url}/connections/{connection_id}",
                params=params
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException:
            return False
    
    def create_processor_in_pg(self, pg_id: str, name: str, processor_type: str,
                                x: float, y: float, config: Optional[Dict] = None) -> Optional[str]:
        """Create a processor inside a Process Group"""
        try:
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
                f"{self.api_url}/process-groups/{pg_id}/processors",
                json=processor_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            
            return response.json()['id']
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore creazione {name}: {e}")
            return None
    
    def create_output_port(self, pg_id: str, name: str, x: float = 400, y: float = 600) -> Optional[str]:
        """Create an Output Port in a Process Group"""
        try:
            port_data = {
                "revision": {"version": 0},
                "component": {
                    "name": name,
                    "position": {"x": x, "y": y}
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{pg_id}/output-ports",
                json=port_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            
            return response.json()['id']
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore creazione Output Port: {e}")
            return None
    
    def create_controller_service(self, pg_id: str, name: str, service_type: str) -> Optional[str]:
        """Create a Controller Service or return existing one"""
        try:
            # Check if service already exists
            response = self.session.get(f"{self.api_url}/flow/process-groups/{pg_id}/controller-services")
            response.raise_for_status()
            
            for service in response.json()['controllerServices']:
                if service['component']['name'] == name:
                    print(f"   ✅ Controller Service già esistente: {name}")
                    return service['id']
            
            # Create new service
            service_data = {
                "revision": {"version": 0},
                "component": {
                    "name": name,
                    "type": service_type,
                    "bundle": {
                        "group": "org.apache.nifi",
                        "artifact": "nifi-http-context-map-nar",
                        "version": "1.28.1"
                    }
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{pg_id}/controller-services",
                json=service_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            
            return response.json()['id']
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore creazione controller service: {e}")
            return None
    
    def enable_controller_service(self, service_id: str) -> bool:
        """Enable a Controller Service"""
        try:
            # Get current revision
            response = self.session.get(f"{self.api_url}/controller-services/{service_id}")
            response.raise_for_status()
            revision = response.json()['revision']['version']
            
            # Enable service
            enable_data = {
                "revision": {"version": revision},
                "state": "ENABLED"
            }
            
            response = self.session.put(
                f"{self.api_url}/controller-services/{service_id}/run-status",
                json=enable_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException:
            return False
    
    def auto_terminate_relationships(self, processor_id: str, relationships: List[str]) -> bool:
        """Auto-terminate relationships on a processor"""
        try:
            # Get current processor config
            response = self.session.get(f"{self.api_url}/processors/{processor_id}")
            response.raise_for_status()
            processor_data = response.json()
            
            revision = processor_data['revision']['version']
            auto_terminated = list(set(processor_data['component'].get('config', {}).get('autoTerminatedRelationships', []) + relationships))
            
            # Update processor with auto-terminated relationships
            update_data = {
                "revision": {"version": revision},
                "component": {
                    "id": processor_id,
                    "config": {
                        "autoTerminatedRelationships": auto_terminated
                    }
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
    
    def create_connection_in_pg(self, pg_id: str, source_id: str, dest_id: str,
                                 relationships: List[str], source_type: str = "PROCESSOR",
                                 dest_type: str = "PROCESSOR") -> bool:
        """Create connection inside a Process Group"""
        try:
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
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException:
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
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException:
            return False
    
    def get_sp01_input_port(self) -> Optional[str]:
        """Find SP01 Input Port"""
        try:
            root_id = self.get_root_pg_id()
            response = self.session.get(f"{self.api_url}/process-groups/{root_id}/process-groups")
            response.raise_for_status()
            
            process_groups = response.json()['processGroups']
            for pg in process_groups:
                if 'SP01' in pg['component']['name']:
                    sp01_id = pg['id']
                    
                    response = self.session.get(f"{self.api_url}/process-groups/{sp01_id}/input-ports")
                    response.raise_for_status()
                    
                    input_ports = response.json()['inputPorts']
                    if input_ports:
                        return input_ports[0]['id']
            return None
            
        except requests.exceptions.RequestException:
            return None
    
    def create_connection_between_pgs(self, source_pg_id: str, source_port_id: str,
                                       dest_pg_id: str, dest_port_id: str) -> bool:
        """Create connection between Process Groups (via ports)"""
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
            print(f"   ⚠️  Errore connessione tra PG: {e}")
            return False
    
    def _get_or_create_process_group(self):
        """Get existing Process Group or create new one"""
        print("[1/6] 🔍 Verifica Process Group esistente...")
        root_id = self.get_root_pg_id()

        try:
            response = self.session.get(f"{self.api_url}/process-groups/{root_id}/process-groups")
            process_groups = response.json()['processGroups']

            existing_pg = None
            for pg in process_groups:
                if pg['component']['name'] == 'Ingress_ContentListener':
                    existing_pg = pg
                    break

            if existing_pg:
                print(f"   ⚠️  Process Group già esistente: {existing_pg['id']}")
                print("   Uso Process Group esistente...")
                return existing_pg['id']
            else:
                print("   📦 Creazione nuovo Process Group...")
                ingress_pg_id = self.create_process_group("Ingress_ContentListener", x=100, y=100)
                if not ingress_pg_id:
                    print("   ❌ Impossibile creare Process Group")
                    return None
                return ingress_pg_id

        except requests.exceptions.RequestException as e:
            print(f"   ❌ Errore: {e}")
            return None

    def _get_or_create_processors(self, ingress_pg_id):
        """Get existing processors or create new ones"""
        print("[2/6] 🔧 Creazione processors interni...")

        existing_http = self.get_processor_by_name("ContentListener_Fascicolo", ingress_pg_id)

        if existing_http:
            print("   ✅ Processors già esistenti nel PG")
            http_proc = self.get_processor_by_name("ContentListener_Fascicolo", ingress_pg_id)
            gen_proc = self.get_processor_by_name("Generate_Workflow_ID", ingress_pg_id)
            log_proc = self.get_processor_by_name("Log_Incoming_Request", ingress_pg_id)
            duplicate_proc = self.get_processor_by_name("Duplicate_For_Response", ingress_pg_id)
            route_proc = self.get_processor_by_name("Route_By_Copy_Index", ingress_pg_id)
            resp_proc = self.get_processor_by_name("Send_Response_To_Client", ingress_pg_id)

            return {
                'http_id': http_proc['id'] if http_proc else None,
                'gen_id': gen_proc['id'] if gen_proc else None,
                'log_id': log_proc['id'] if log_proc else None,
                'duplicate_id': duplicate_proc['id'] if duplicate_proc else None,
                'route_id': route_proc['id'] if route_proc else None,
                'resp_id': resp_proc['id'] if resp_proc else None,
                'context_map_id': None  # Already exists
            }
        else:
            print("   📌 Creazione nuovi processors...")
            
            # First create HTTP Context Map controller service
            print("   🔧 Creazione HTTP Context Map...")
            context_map_id = self.create_controller_service(
                ingress_pg_id,
                "HTTP-Context-Map-Ingress",
                "org.apache.nifi.http.StandardHttpContextMap"
            )
            
            if context_map_id:
                print(f"   ✅ HTTP Context Map creato: {context_map_id}")
                # Enable the controller service
                if self.enable_controller_service(context_map_id):
                    print("   ✅ HTTP Context Map abilitato")
                else:
                    print("   ⚠️  HTTP Context Map non abilitato (sarà abilitato automaticamente)")
            else:
                print("   ❌ Impossibile creare HTTP Context Map")
                return None

            http_id = self.create_processor_in_pg(
                ingress_pg_id,
                "ContentListener_Fascicolo",
                "org.apache.nifi.processors.standard.HandleHttpRequest",
                x=200, y=100,
                config={
                    "properties": {
                        "Listening Port": "9099",
                        "Allowed Paths": "/contentListener/fascicolo",
                        "HTTP Context Map": context_map_id
                    }
                }
            )

            gen_id = self.create_processor_in_pg(
                ingress_pg_id,
                "Generate_Workflow_ID",
                "org.apache.nifi.processors.attributes.UpdateAttribute",
                x=200, y=250,
                config={
                    "properties": {
                        "workflow_id": "${UUID()}"
                    }
                }
            )

            log_id = self.create_processor_in_pg(
                ingress_pg_id,
                "Log_Incoming_Request",
                "org.apache.nifi.processors.standard.LogAttribute",
                x=200, y=400,
                config={
                    "properties": {
                        "Log Level": "info",
                        "Log Payload": "true"
                    }
                }
            )

            # DuplicateFlowFile - crea 1 copia (totale 2 FlowFiles)
            duplicate_id = self.create_processor_in_pg(
                ingress_pg_id,
                "Duplicate_For_Response",
                "org.apache.nifi.processors.standard.DuplicateFlowFile",
                x=200, y=550,
                config={
                    "properties": {
                        "Number of Copies": "1"  # Crea 1 copia dell'originale
                    }
                }
            )

            # RouteOnAttribute - separa originale (copy.index=0) da copia (copy.index=1)
            route_id = self.create_processor_in_pg(
                ingress_pg_id,
                "Route_By_Copy_Index",
                "org.apache.nifi.processors.standard.RouteOnAttribute",
                x=200, y=700,
                config={
                    "properties": {
                        "Routing Strategy": "Route to Property name",
                        "original": "${copy.index:equals('0')}",  # Originale ha copy.index=0
                        "duplicate": "${copy.index:equals('1')}"  # Copia ha copy.index=1
                    },
                    "autoTerminatedRelationships": ["unmatched"]
                }
            )

            resp_id = self.create_processor_in_pg(
                ingress_pg_id,
                "Send_Response_To_Client",
                "org.apache.nifi.processors.standard.HandleHttpResponse",
                x=500, y=700,
                config={
                    "properties": {
                        "HTTP Status Code": "200",
                        "HTTP Context Map": context_map_id
                    }
                }
            )

            processors = {
                'http_id': http_id,
                'gen_id': gen_id,
                'log_id': log_id,
                'duplicate_id': duplicate_id,
                'route_id': route_id,
                'resp_id': resp_id,
                'context_map_id': context_map_id
            }

            print(f"   ✅ Creati {len([p for p in processors.values() if p])} processors")
            return processors

    def _get_or_create_output_port(self, ingress_pg_id):
        """Get existing output port or create new one"""
        print("[3/6] 📤 Creazione Output Port per SP01...")

        try:
            response = self.session.get(f"{self.api_url}/process-groups/{ingress_pg_id}/output-ports")
            output_ports = response.json()['outputPorts']

            eml_port = None
            for port in output_ports:
                if port['component']['name'] == 'To_SP01_EML':
                    eml_port = port
                    break

            if eml_port:
                print(f"   ✅ Output Port già esistente: {eml_port['id']}")
                return eml_port['id']
            else:
                eml_port_id = self.create_output_port(ingress_pg_id, "To_SP01_EML", x=200, y=700)
                if eml_port_id:
                    print(f"   ✅ Output Port creato: {eml_port_id}")
                return eml_port_id

        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore gestione Output Port: {e}")
            return None

    def _create_single_connection(self, ingress_pg_id, source_id, dest_id, relationships, dest_type="PROCESSOR"):
        """Create a single connection between processors"""
        if dest_type == "OUTPUT_PORT":
            return self.create_connection_in_pg(ingress_pg_id, source_id, dest_id, relationships, dest_type=dest_type)
        else:
            return self.create_connection_in_pg(ingress_pg_id, source_id, dest_id, relationships)

    def _create_internal_connections(self, ingress_pg_id, processor_ids, eml_port_id):
        """Create internal connections between processors"""
        print("[4/6] 🔗 Creazione connessioni interne...")

        # Delete existing connections first
        existing_connections = self.get_all_connections(ingress_pg_id)
        for conn in existing_connections:
            self.delete_connection(conn['id'], conn['revision'])

        http_id = processor_ids.get('http_id')
        gen_id = processor_ids.get('gen_id')
        log_id = processor_ids.get('log_id')
        duplicate_id = processor_ids.get('duplicate_id')
        route_id = processor_ids.get('route_id')
        resp_id = processor_ids.get('resp_id')

        connections_created = 0

        # Only create connections if all required processors exist
        if not all([http_id, gen_id, log_id, duplicate_id, route_id, resp_id]):
            print("   ⚠️  Alcuni processors mancanti, skip creazione connessioni")
            return 0

        # Create connections - Flusso con DuplicateFlowFile + RouteOnAttribute
        connection_specs = [
            (http_id, gen_id, ["success"], "HTTP Request → Generate ID"),
            (gen_id, log_id, ["success"], "Generate ID → Log"),
            (log_id, duplicate_id, ["success"], "Log → Duplicate (crea copia)"),
            (duplicate_id, route_id, ["success"], "Duplicate → Route (separa original/duplicate)"),
            (route_id, resp_id, ["duplicate"], "Route → Response (solo duplicates)"),
        ]

        for source_id, dest_id, relationships, description in connection_specs:
            if self._create_single_connection(ingress_pg_id, source_id, dest_id, relationships):
                print(f"   ✅ {description}")
                connections_created += 1
        
        # Auto-terminate success and failure on HandleHttpResponse
        if resp_id:
            self.auto_terminate_relationships(resp_id, ["success", "failure"])
            print("   ✅ HandleHttpResponse auto-terminate success/failure")

        # Route → Output Port (original) - Per SP01
        if eml_port_id and route_id and self._create_single_connection(
            ingress_pg_id, route_id, eml_port_id, ["original"], "OUTPUT_PORT"
        ):
            print("   ✅ Route → Output Port (original)")
            connections_created += 1

        print(f"\n   📊 Connessioni create: {connections_created}")
        return connections_created

    def _connect_to_sp01(self, ingress_pg_id, eml_port_id):
        """Connect Ingress PG to SP01"""
        print("[5/6] 🔗 Connessione a SP01...")

        sp01_port = self.get_sp01_input_port()
        if not sp01_port or not eml_port_id:
            print("   ⚠️  SP01 Input Port non disponibile, skip connessione")
            return False

        root_id = self.get_root_pg_id()
        response = self.session.get(f"{self.api_url}/process-groups/{root_id}/process-groups")
        pgs = response.json()['processGroups']
        sp01_pg_id = None
        for pg in pgs:
            if 'SP01' in pg['component']['name']:
                sp01_pg_id = pg['id']
                break

        if not sp01_pg_id:
            print("   ⚠️  SP01 PG non trovato")
            return False

        if self.create_connection_between_pgs(
            ingress_pg_id,
            eml_port_id,
            sp01_pg_id,
            sp01_port
        ):
            print("   ✅ Ingress Output Port → SP01 Input Port")
            return True
        else:
            print("   ⚠️  Connessione già esistente o errore")
            return False

    def _start_processors(self, processor_ids):
        """Start all processors"""
        print("[6/6] 🚀 Avvio processors...")

        started = 0
        all_ids = [processor_ids.get('http_id'), processor_ids.get('gen_id'),
                  processor_ids.get('log_id'), processor_ids.get('route_id'),
                  processor_ids.get('resp_id')]

        for proc_id in all_ids:
            if proc_id and self.start_processor(proc_id):
                started += 1

        print(f"   ✅ Avviati {started}/{len([i for i in all_ids if i])} processors")
        return started

    def build_ingress_process_group(self):
        """Build complete Ingress Process Group with workflow"""
        print("=" * 70)
        print("  Creazione Process Group: Ingress_ContentListener")
        print("=" * 70)
        print()

        # Step 1: Get or create Process Group
        ingress_pg_id = self._get_or_create_process_group()
        if not ingress_pg_id:
            return

        print()

        # Step 2: Get or create processors
        processor_ids = self._get_or_create_processors(ingress_pg_id)

        print()

        # Step 3: Get or create output port
        eml_port_id = self._get_or_create_output_port(ingress_pg_id)

        print()

        # Step 4: Create internal connections
        connections_created = self._create_internal_connections(ingress_pg_id, processor_ids, eml_port_id)

        print()

        # Step 5: Connect to SP01
        self._connect_to_sp01(ingress_pg_id, eml_port_id)

        print()

        # Step 6: Start processors
        self._start_processors(processor_ids)

        print()

        # Summary
        print("=" * 70)
        print("  ✅ Process Group Completato")
        print("=" * 70)
        print()
        print("📦 Process Group: Ingress_ContentListener")
        print(f"   ID: {ingress_pg_id}")
        print()
        print("📊 Componenti:")
        print("   - 5 Processors interni")
        print("   - 1 Output Port (To_SP01_EML)")
        print(f"   - {connections_created} Connessioni interne")
        print()
        print("📍 Endpoint disponibile:")
        print("   http://localhost:9099/contentListener/fascicolo")
        print()
        print("🎨 Canvas organizzato:")
        print(f"   {self.nifi_url}/nifi")
        print()

def main():
    try:
        builder = IngressProcessGroupBuilder()
        builder.build_ingress_process_group()
        
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
