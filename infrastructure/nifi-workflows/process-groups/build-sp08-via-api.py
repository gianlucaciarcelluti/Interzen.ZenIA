#!/usr/bin/env python3
"""
Script per creare il flusso SP08 via API NiFi (senza template).
SP08 - Quality Checker
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

def build_sp08(builder: NiFiFlowBuilder):
    print("🏗️  Costruzione SP08 - Quality Checker...")
    pg = builder.create_process_group("SP08_Quality_Checker")
    pg_id = pg["id"]
    print(f"  ✅ Process Group creato: {pg_id}")

    listen_http = builder.create_processor(pg_id, "org.apache.nifi.processors.standard.ListenHTTP", "HTTP_Endpoint", 100, 100, {
        "properties": {"Listening Port": "9098", "Base Path": "sp08"}
    })
    listen_id = listen_http["id"]
    print(f"  ✅ ListenHTTP creato: {listen_id} (porta 9098)")

    invoke_http = builder.create_processor(pg_id, "org.apache.nifi.processors.standard.InvokeHTTP", "Call_SP08_Quality_Checker", 300, 100, {
        "properties": {"HTTP Method": "POST", "Remote URL": "http://sp08-quality-checker:5008/check", "Content-Type": "application/json"},
        "autoTerminatedRelationships": ["Failure", "Retry", "No Retry", "Original"]
    })
    invoke_id = invoke_http["id"]
    print(f"  ✅ InvokeHTTP creato: {invoke_id}")

    success_port = builder.create_output_port(pg_id, "Success", 500, 100)
    success_port_id = success_port["id"]
    print(f"  ✅ Output Port 'Success' creato: {success_port_id}")

    builder.create_connection(pg_id, listen_id, invoke_id, ["success"])
    builder.create_connection(pg_id, invoke_id, success_port_id, ["Response"], dest_type="OUTPUT_PORT")
    print("  🔗 Connessioni create")

    print(f"\n🎉 SP08 costruito con successo! Process Group ID: {pg_id}")
    return pg_id

if __name__ == "__main__":
    print("NiFi Flow Builder - SP08 Quality Checker")
    builder = NiFiFlowBuilder(NIFI_URL)
    try:
        sp08_id = build_sp08(builder)
        print(f"\n✅ COMPLETATO! Process Group SP08 ID: {sp08_id}")
        print("Endpoint: POST http://localhost:9098/sp08")
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")