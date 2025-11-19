#!/usr/bin/env python3
"""
Script per creare l'endpoint di ingresso /contentListener/fascicolo in NiFi.
Questo endpoint riceve i fascicoli email e avvia il workflow completo.
"""

import requests
import json
import time
from typing import Dict, Any, Optional

NIFI_URL = "http://localhost:8080/nifi-api"

class NiFiIngressBuilder:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_root_pg_id(self) -> str:
        """Ottieni l'ID del root process group."""
        url = f"{self.base_url}/flow/process-groups/root"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()["processGroupFlow"]["id"]
    
    def create_processor(self, pg_id: str, proc_type: str, name: str, 
                        x: float = 0, y: float = 0, 
                        config: Optional[Dict] = None) -> Dict[str, Any]:
        """Crea un processore."""
        url = f"{self.base_url}/process-groups/{pg_id}/processors"
        payload = {
            "revision": {"version": 0},
            "component": {
                "type": proc_type,
                "name": name,
                "position": {"x": x, "y": y}
            }
        }
        
        if config:
            payload["component"]["config"] = config
        
        print(f"   POST {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)[:200]}...")
        resp = self.session.post(url, json=payload)
        print(f"   Status: {resp.status_code}")
        if resp.status_code != 200 and resp.status_code != 201:
            print(f"   Response: {resp.text[:500]}")
        resp.raise_for_status()
        return resp.json()
    
    def create_connection(self, pg_id: str, source_id: str, dest_id: str,
                         relationships: list, source_type: str = "PROCESSOR",
                         dest_type: str = "PROCESSOR") -> Dict[str, Any]:
        """Crea una connessione tra componenti."""
        url = f"{self.base_url}/process-groups/{pg_id}/connections"
        payload = {
            "revision": {"version": 0},
            "component": {
                "source": {
                    "id": source_id,
                    "groupId": pg_id,
                    "type": source_type
                },
                "destination": {
                    "id": dest_id,
                    "groupId": pg_id,
                    "type": dest_type
                },
                "selectedRelationships": relationships
            }
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
    
    def get_process_group_by_name(self, name: str) -> Optional[str]:
        """Cerca un process group per nome."""
        root_id = self.get_root_pg_id()
        url = f"{self.base_url}/process-groups/{root_id}/process-groups"
        resp = self.session.get(url)
        resp.raise_for_status()
        
        for pg in resp.json().get("processGroups", []):
            if pg["component"]["name"] == name:
                return pg["id"]
        return None
    
    def create_ingress_endpoint(self):
        """Crea l'endpoint di ingresso /contentListener/fascicolo."""
        print("🔧 Creazione endpoint di ingresso /contentListener/fascicolo...")
        
        # Use "root" instead of the hex ID
        root_id = "root"
        print(f"✓ Using root Process Group")
        
        # 1. Crea HandleHttpRequest processor per ricevere richieste HTTP
        print("\n1️⃣ Creazione HandleHttpRequest processor...")
        http_listener = self.create_processor(
            pg_id=root_id,
            proc_type="org.apache.nifi.processors.standard.HandleHttpRequest",
            name="ContentListener_Fascicolo",
            x=100,
            y=100,
            config={
                "properties": {
                    "Listening Port": "9099",
                    "Allowed Paths": "/contentListener/fascicolo"
                },
                "autoTerminatedRelationships": []
            }
        )
        listener_id = http_listener["id"]
        print(f"✓ HandleHttpRequest creato: {listener_id}")
        
        # 2. Crea GenerateFlowFile per generare workflow_id
        print("\n2️⃣ Creazione UpdateAttribute per workflow_id...")
        generate_wf_id = self.create_processor(
            pg_id=root_id,
            proc_type="org.apache.nifi.processors.attributes.UpdateAttribute",
            name="Generate_Workflow_ID",
            x=100,
            y=250,
            config={
                "properties": {
                    "workflow_id": "WF-${now():format('yyyyMMdd-HHmmss')}-${UUID()}",
                    "workflow_status": "STARTED",
                    "timestamp_start": "${now():format('yyyy-MM-dd HH:mm:ss')}"
                },
                "autoTerminatedRelationships": []
            }
        )
        wf_id_gen_id = generate_wf_id["id"]
        print(f"✓ UpdateAttribute creato: {wf_id_gen_id}")
        
        # 3. Crea LogAttribute per debug
        print("\n3️⃣ Creazione LogAttribute per debugging...")
        log_processor = self.create_processor(
            pg_id=root_id,
            proc_type="org.apache.nifi.processors.standard.LogAttribute",
            name="Log_Incoming_Request",
            x=100,
            y=400,
            config={
                "properties": {
                    "Log Level": "info",
                    "Log Payload": "true",
                    "Attributes to Log": "workflow_id,http.request.uri,http.method",
                    "Log prefix": "INGRESS"
                },
                "autoTerminatedRelationships": []
            }
        )
        log_id = log_processor["id"]
        print(f"✓ LogAttribute creato: {log_id}")
        
        # 4. Crea RouteOnAttribute per routing verso SP01
        print("\n4️⃣ Creazione RouteOnAttribute per routing...")
        route_processor = self.create_processor(
            pg_id=root_id,
            proc_type="org.apache.nifi.processors.standard.RouteOnAttribute",
            name="Route_To_Workflow",
            x=100,
            y=550,
            config={
                "properties": {
                    "Routing Strategy": "Route to Property name",
                    "valid_request": "${http.request.uri:equals('/contentListener/fascicolo')}"
                },
                "autoTerminatedRelationships": ["unmatched"]
            }
        )
        route_id = route_processor["id"]
        print(f"✓ RouteOnAttribute creato: {route_id}")
        
        # 5. Connetti i processor
        print("\n5️⃣ Creazione connessioni tra processor...")
        
        # HandleHttpRequest -> UpdateAttribute
        conn1 = self.create_connection(
            pg_id=root_id,
            source_id=listener_id,
            dest_id=wf_id_gen_id,
            relationships=["success"]
        )
        print(f"✓ Connessione 1: HandleHttpRequest → UpdateAttribute")
        
        # UpdateAttribute -> LogAttribute
        conn2 = self.create_connection(
            pg_id=root_id,
            source_id=wf_id_gen_id,
            dest_id=log_id,
            relationships=["success"]
        )
        print(f"✓ Connessione 2: UpdateAttribute → LogAttribute")
        
        # LogAttribute -> RouteOnAttribute
        conn3 = self.create_connection(
            pg_id=root_id,
            source_id=log_id,
            dest_id=route_id,
            relationships=["success"]
        )
        print(f"✓ Connessione 3: LogAttribute → RouteOnAttribute")
        
        # 6. Cerca SP01 Process Group per connessione
        print("\n6️⃣ Ricerca SP01 Process Group...")
        sp01_pg_id = self.get_process_group_by_name("SP01_EML_Parser")
        
        if sp01_pg_id:
            print(f"✓ SP01 Process Group trovato: {sp01_pg_id}")
            print("   ℹ️  Per completare il collegamento a SP01, connetti manualmente")
            print(f"      RouteOnAttribute (relationship: valid_request) → SP01 Input Port")
        else:
            print("⚠️  SP01 Process Group non trovato - collegamento manuale richiesto")
        
        # 7. Crea HandleHttpResponse per rispondere al client
        print("\n7️⃣ Creazione HandleHttpResponse...")
        http_response = self.create_processor(
            pg_id=root_id,
            proc_type="org.apache.nifi.processors.standard.HandleHttpResponse",
            name="Send_Response_To_Client",
            x=400,
            y=550,
            config={
                "properties": {
                    "HTTP Status Code": "200"
                },
                "autoTerminatedRelationships": ["success", "failure"]
            }
        )
        response_id = http_response["id"]
        print(f"✓ HandleHttpResponse creato: {response_id}")
        
        # Connetti Route -> Response (per ora)
        conn4 = self.create_connection(
            pg_id=root_id,
            source_id=route_id,
            dest_id=response_id,
            relationships=["valid_request"]
        )
        print(f"✓ Connessione 4: RouteOnAttribute → HandleHttpResponse (temporanea)")
        
        print("\n" + "="*60)
        print("✅ ENDPOINT /contentListener/fascicolo CREATO CON SUCCESSO!")
        print("="*60)
        print(f"\n📡 Endpoint disponibile su:")
        print(f"   POST http://localhost:9099/contentListener/fascicolo")
        print(f"\n🔧 Componenti creati:")
        print(f"   • HandleHttpRequest: {listener_id}")
        print(f"   • UpdateAttribute (Workflow ID): {wf_id_gen_id}")
        print(f"   • LogAttribute: {log_id}")
        print(f"   • RouteOnAttribute: {route_id}")
        print(f"   • HandleHttpResponse: {response_id}")
        print(f"\n⚠️  PROSSIMI PASSI:")
        print(f"   1. Avviare tutti i processor creati")
        print(f"   2. Connettere RouteOnAttribute a SP01 Process Group")
        print(f"   3. Testare con: curl -X POST http://localhost:9099/contentListener/fascicolo")
        
        return {
            "listener_id": listener_id,
            "workflow_id_gen": wf_id_gen_id,
            "log_id": log_id,
            "route_id": route_id,
            "response_id": response_id,
            "sp01_pg_id": sp01_pg_id
        }


def main():
    print("🚀 Creazione Endpoint di Ingresso NiFi")
    print("="*60)
    
    builder = NiFiIngressBuilder(NIFI_URL)
    
    try:
        result = builder.create_ingress_endpoint()
        
        print("\n✅ Configurazione completata!")
        print("\n📋 IDs dei componenti creati:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"\n❌ Errore durante la creazione: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
