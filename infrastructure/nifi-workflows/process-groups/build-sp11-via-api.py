#!/usr/bin/env python3
"""
Script per creare il flusso SP11 via API NiFi (senza template).
SP11 - Security Audit
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
        url = f"{self.base_url}/process-groups/{parent_id}/process-groups"
        payload = {"revision": {"version": 0}, "component": {"name": name, "position": {"x": 0, "y": 0}}}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def create_processor(self, pg_id: str, proc_type: str, name: str, x: float = 0, y: float = 0, config: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/process-groups/{pg_id}/processors"
        payload = {
            "revision": {"version": 0},
            "component": {
                "type": proc_type,
                "bundle": {"group": "org.apache.nifi", "artifact": "nifi-standard-nar", "version": "1.28.1"},
                "name": name, "position": {"x": x, "y": y}
            }
        }
        if config: payload["component"]["config"] = config
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def create_connection(self, pg_id: str, source_id: str, dest_id: str, relationships: list, source_type: str = "PROCESSOR", dest_type: str = "PROCESSOR") -> Dict[str, Any]:
        url = f"{self.base_url}/process-groups/{pg_id}/connections"
        payload = {
            "revision": {"version": 0},
            "component": {
                "source": {"id": source_id, "groupId": pg_id, "type": source_type},
                "destination": {"id": dest_id, "groupId": pg_id, "type": dest_type},
                "selectedRelationships": relationships
            }
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def create_output_port(self, pg_id: str, name: str, x: float = 0, y: float = 0) -> Dict[str, Any]:
        url = f"{self.base_url}/process-groups/{pg_id}/output-ports"
        payload = {"revision": {"version": 0}, "component": {"name": name, "position": {"x": x, "y": y}}}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def create_input_port(self, pg_id: str, name: str, x: float = 0, y: float = 0) -> Dict[str, Any]:
        url = f"{self.base_url}/process-groups/{pg_id}/input-ports"
        payload = {"revision": {"version": 0}, "component": {"name": name, "position": {"x": x, "y": y}}}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

def build_sp11(builder: NiFiFlowBuilder):
    print("🏗️  Costruzione SP11 - Security Audit...")
    pg = builder.create_process_group("SP11_Security_Audit")
    pg_id = pg["id"]
    print(f"  ✅ Process Group creato: {pg_id}")

    # Create Input Port for connection from SP01
    input_port = builder.create_input_port(pg_id, "From_SP01", 50, 100)
    input_port_id = input_port["id"]
    print(f"  ✅ Input Port 'From_SP01' creato: {input_port_id}")

    listen_http = builder.create_processor(pg_id, "org.apache.nifi.processors.standard.ListenHTTP", "HTTP_Endpoint", 150, 100, {
        "properties": {"Listening Port": "9101", "Base Path": "sp11"}
    })
    listen_id = listen_http["id"]
    print(f"  ✅ ListenHTTP creato: {listen_id} (porta 9101)")

    invoke_http = builder.create_processor(pg_id, "org.apache.nifi.processors.standard.InvokeHTTP", "Call_SP11_Security_Audit", 350, 100, {
        "properties": {"HTTP Method": "POST", "Remote URL": "http://sp11-security-audit:5011/audit", "Content-Type": "application/json"},
        "autoTerminatedRelationships": ["Failure", "Retry", "No Retry", "Original"]
    })
    invoke_id = invoke_http["id"]
    print(f"  ✅ InvokeHTTP creato: {invoke_id}")

    success_port = builder.create_output_port(pg_id, "Success", 550, 100)
    success_port_id = success_port["id"]
    print(f"  ✅ Output Port 'Success' creato: {success_port_id}")

    # Connect Input Port to InvokeHTTP
    builder.create_connection(pg_id, input_port_id, invoke_id, [""], source_type="INPUT_PORT")
    print("  🔗 From_SP01 → Call_SP11_Security_Audit")
    
    builder.create_connection(pg_id, listen_id, invoke_id, ["success"])
    print("  🔗 HTTP_Endpoint → Call_SP11_Security_Audit")
    
    builder.create_connection(pg_id, invoke_id, success_port_id, ["Response"], dest_type="OUTPUT_PORT")
    print("  🔗 Call_SP11_Security_Audit → Success")

    print(f"\n🎉 SP11 costruito con successo! Process Group ID: {pg_id}")
    return pg_id

if __name__ == "__main__":
    print("NiFi Flow Builder - SP11 Security Audit")
    builder = NiFiFlowBuilder(NIFI_URL)
    try:
        sp11_id = build_sp11(builder)
        print(f"\n✅ COMPLETATO! Process Group SP11 ID: {sp11_id}")
        print("Endpoint: POST http://localhost:9101/sp11")
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")