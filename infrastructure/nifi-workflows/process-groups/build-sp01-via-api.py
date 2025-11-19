#!/usr/bin/env python3
"""
Script per creare il flusso SP01 via API NiFi (senza template).
Questo è l'Opzione A - Infrastructure as Code via API REST.
"""

import requests
import json
import time
from typing import Dict, Any, Optional

NIFI_URL = "http://localhost:8080/nifi-api"

class NiFiFlowBuilder:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def create_process_group(self, name: str, parent_id: str = "root") -> Dict[str, Any]:
        """Crea un nuovo process group."""
        url = f"{self.base_url}/process-groups/{parent_id}/process-groups"
        payload = {
            "revision": {"version": 0},
            "component": {
                "name": name,
                "position": {"x": 0, "y": 0}
            }
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
    
    def create_processor(self, pg_id: str, proc_type: str, name: str, 
                        x: float = 0, y: float = 0, 
                        config: Optional[Dict] = None) -> Dict[str, Any]:
        """Crea un processore in un process group."""
        url = f"{self.base_url}/process-groups/{pg_id}/processors"
        payload = {
            "revision": {"version": 0},
            "component": {
                "type": proc_type,
                "bundle": {
                    "group": "org.apache.nifi",
                    "artifact": "nifi-standard-nar",
                    "version": "1.28.1"
                },
                "name": name,
                "position": {"x": x, "y": y}
            }
        }
        
        if config:
            payload["component"]["config"] = config
        
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
    
    def create_connection(self, pg_id: str, source_id: str, dest_id: str,
                         relationships: list, source_type: str = "PROCESSOR",
                         dest_type: str = "PROCESSOR") -> Dict[str, Any]:
        """Crea una connessione tra due componenti."""
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
    
    def create_input_port(self, pg_id: str, name: str = "In",
                         x: float = 0, y: float = 0) -> Dict[str, Any]:
        """Crea un input port."""
        url = f"{self.base_url}/process-groups/{pg_id}/input-ports"
        payload = {
            "revision": {"version": 0},
            "component": {
                "name": name,
                "position": {"x": x, "y": y}
            }
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
    
    def create_output_port(self, pg_id: str, name: str,
                          x: float = 0, y: float = 0) -> Dict[str, Any]:
        """Crea un output port."""
        url = f"{self.base_url}/process-groups/{pg_id}/output-ports"
        payload = {
            "revision": {"version": 0},
            "component": {
                "name": name,
                "position": {"x": x, "y": y}
            }
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


def build_sp01(builder: NiFiFlowBuilder):
    """
    Costruisce il flusso SP01 - EML Parser.
    
    Architettura:
    - ListenHTTP (porta 9091) -> riceve POST HTTP con .eml files
    - InvokeHTTP -> chiama microservizio SP01 su porta 5001
    - RouteOnAttribute -> separa success/failure
    - Output Port "Success" -> risultati OK
    - Output Port "Failure" -> errori
    """
    print("🏗️  Costruzione SP01 - EML Parser...")
    
    # 1. Crea Process Group
    pg = builder.create_process_group("SP01_EML_Parser")
    pg_id = pg["id"]
    print(f"  ✅ Process Group creato: {pg_id}")
    
    # 2. Crea ListenHTTP (endpoint HTTP per testing)
    listen_http = builder.create_processor(
        pg_id,
        "org.apache.nifi.processors.standard.ListenHTTP",
        "HTTP_Endpoint",
        x=100, y=100,
        config={
            "properties": {
                "Listening Port": "9091",
                "Base Path": "sp01"
            }
        }
    )
    listen_id = listen_http["id"]
    print(f"  ✅ ListenHTTP creato: {listen_id} (porta 9091)")
    
    # 3. Crea InvokeHTTP (chiama microservizio SP01)
    invoke_http = builder.create_processor(
        pg_id,
        "org.apache.nifi.processors.standard.InvokeHTTP",
        "Call_SP01_Microservice",
        x=300, y=100,
        config={
            "properties": {
                "HTTP Method": "POST",
                "Remote URL": "http://sp01-eml-parser:5001/parse",
                "Content-Type": "application/json"
            },
            "autoTerminatedRelationships": ["Retry", "No Retry"]
        }
    )
    invoke_id = invoke_http["id"]
    print(f"  ✅ InvokeHTTP creato: {invoke_id}")
    
    # 4. Crea RouteOnAttribute (separa success/failure)
    route_attr = builder.create_processor(
        pg_id,
        "org.apache.nifi.processors.standard.RouteOnAttribute",
        "Route_Success_Failure",
        x=500, y=100,
        config={
            "properties": {
                "Routing Strategy": "Route to Property name"
            },
            "autoTerminatedRelationships": ["unmatched"]
        }
    )
    route_id = route_attr["id"]
    print(f"  ✅ RouteOnAttribute creato: {route_id}")
    
    # 4.5. Crea Input Port per connessione da Ingress
    input_port = builder.create_input_port(pg_id, "From_Ingress", x=50, y=50)
    input_port_id = input_port["id"]
    print(f"  ✅ Input Port 'From_Ingress' creato: {input_port_id}")
    
    # 5. Crea Output Ports
    success_port = builder.create_output_port(pg_id, "Success", x=700, y=50)
    success_port_id = success_port["id"]
    print(f"  ✅ Output Port 'Success' creato: {success_port_id}")
    
    failure_port = builder.create_output_port(pg_id, "Failure", x=700, y=150)
    failure_port_id = failure_port["id"]
    print(f"  ✅ Output Port 'Failure' creato: {failure_port_id}")
    
    # 6. Crea Connessioni
    print("  🔗 Creazione connessioni...")
    
    # Input Port -> InvokeHTTP (bypass ListenHTTP quando arriva da Ingress)
    builder.create_connection(pg_id, input_port_id, invoke_id, [""],
                             source_type="INPUT_PORT")
    print("    ✅ From_Ingress → InvokeHTTP")
    
    # ListenHTTP -> InvokeHTTP
    builder.create_connection(pg_id, listen_id, invoke_id, ["success"])
    print("    ✅ ListenHTTP → InvokeHTTP")
    
    # InvokeHTTP -> RouteOnAttribute (success response)
    builder.create_connection(pg_id, invoke_id, route_id, ["Response"])
    print("    ✅ InvokeHTTP → RouteOnAttribute")
    
    # RouteOnAttribute -> Success Port
    builder.create_connection(pg_id, route_id, success_port_id, ["success"],
                             dest_type="OUTPUT_PORT")
    print("    ✅ RouteOnAttribute → Success")
    
    # InvokeHTTP -> Failure Port (failure relationship)
    builder.create_connection(pg_id, invoke_id, failure_port_id, ["Failure"],
                             dest_type="OUTPUT_PORT")
    print("    ✅ InvokeHTTP → Failure")
    
    print(f"\n🎉 SP01 costruito con successo! Process Group ID: {pg_id}")
    return pg_id


if __name__ == "__main__":
    print("=" * 60)
    print("NiFi Flow Builder - Opzione A (API-based)")
    print("=" * 60)
    print()
    
    builder = NiFiFlowBuilder(NIFI_URL)
    
    try:
        sp01_id = build_sp01(builder)
        
        print("\n" + "=" * 60)
        print("✅ COMPLETATO!")
        print("=" * 60)
        print(f"\nProcess Group SP01 ID: {sp01_id}")
        print("\nAccedi a NiFi UI: http://localhost:8080/nifi")
        print("Vedrai il process group 'SP01_EML_Parser' con:")
        print("  - ListenHTTP su porta 9091 (endpoint: POST http://localhost:9091/sp01)")
        print("  - InvokeHTTP per chiamare microservizio SP01")
        print("  - RouteOnAttribute per routing")
        print("  - Output Ports 'Success' e 'Failure'")
        print("\n📮 Test con Postman:")
        print("   POST http://localhost:9091/sp01")
        print("   Body: contenuto .eml file")

        
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
