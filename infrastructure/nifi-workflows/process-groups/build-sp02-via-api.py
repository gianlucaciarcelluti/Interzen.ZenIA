#!/usr/bin/env python3
"""
Script per creare il flusso SP02 via API NiFi (senza template).
SP02 - Document Extractor & Attachment Classifier
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


def build_sp02(builder: NiFiFlowBuilder):
    """
    Costruisce il flusso SP02 - Document Extractor & Attachment Classifier.

    Architettura semplificata (come SP01 dopo simplify):
    - ListenHTTP (porta 9092) -> riceve POST HTTP con documenti
    - ReplaceText -> wrap content in JSON per microservizio
    - InvokeHTTP -> chiama microservizio SP02 su porta 5002
    - Output Port "Success" -> risultati OK (auto-terminated)
    """
    print("🏗️  Costruzione SP02 - Document Extractor...")

    # 1. Crea Process Group
    pg = builder.create_process_group("SP02_Document_Extractor")
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
                "Listening Port": "9092",
                "Base Path": "sp02"
            }
        }
    )
    listen_id = listen_http["id"]
    print(f"  ✅ ListenHTTP creato: {listen_id} (porta 9092)")

    # 3. Crea ReplaceText (wrap content in JSON)
    replace_text = builder.create_processor(
        pg_id,
        "org.apache.nifi.processors.standard.ReplaceText",
        "Wrap_Document_JSON",
        x=300, y=100,
        config={
            "properties": {
                "Search Value": "(.*)",
                "Replacement Value": '{"document_content": "$1", "filename": "${filename}"}',
                "Replacement Strategy": "Regex Replace",
                "Evaluation Mode": "Entire text"
            }
        }
    )
    replace_id = replace_text["id"]
    print(f"  ✅ ReplaceText creato: {replace_id}")

    # 4. Crea InvokeHTTP (chiama microservizio SP02)
    invoke_http = builder.create_processor(
        pg_id,
        "org.apache.nifi.processors.standard.InvokeHTTP",
        "Call_SP02_Microservice",
        x=500, y=100,
        config={
            "properties": {
                "HTTP Method": "POST",
                "Remote URL": "http://sp02-document-extractor:5002/extract",
                "Content-Type": "application/json"
            },
            "autoTerminatedRelationships": ["Failure", "Retry", "No Retry", "Original"]
        }
    )
    invoke_id = invoke_http["id"]
    print(f"  ✅ InvokeHTTP creato: {invoke_id}")

    # 5. Crea Output Port "Success" (auto-terminated)
    success_port = builder.create_output_port(pg_id, "Success", x=700, y=100)
    success_port_id = success_port["id"]
    print(f"  ✅ Output Port 'Success' creato: {success_port_id}")

    # 6. Crea Connessioni
    print("  🔗 Creazione connessioni...")

    # ListenHTTP -> ReplaceText
    builder.create_connection(pg_id, listen_id, replace_id, ["success"])
    print("    ✅ ListenHTTP → ReplaceText")

    # ReplaceText -> InvokeHTTP
    builder.create_connection(pg_id, replace_id, invoke_id, ["success"])
    print("    ✅ ReplaceText → InvokeHTTP")

    # InvokeHTTP -> Success Port (Response relationship)
    builder.create_connection(pg_id, invoke_id, success_port_id, ["Response"],
                             dest_type="OUTPUT_PORT")
    print("    ✅ InvokeHTTP → Success (auto-terminated)")

    print(f"\n🎉 SP02 costruito con successo! Process Group ID: {pg_id}")
    return pg_id


if __name__ == "__main__":
    print("=" * 60)
    print("NiFi Flow Builder - SP02 Document Extractor")
    print("=" * 60)
    print()

    builder = NiFiFlowBuilder(NIFI_URL)

    try:
        sp02_id = build_sp02(builder)

        print("\n" + "=" * 60)
        print("✅ COMPLETATO!")
        print("=" * 60)
        print(f"\nProcess Group SP02 ID: {sp02_id}")
        print("\nAccedi a NiFi UI: http://localhost:8080/nifi")
        print("Vedrai il process group 'SP02_Document_Extractor' con:")
        print("  - ListenHTTP su porta 9092 (endpoint: POST http://localhost:9092/sp02)")
        print("  - ReplaceText per wrapping JSON")
        print("  - InvokeHTTP per chiamare microservizio SP02")
        print("  - Output Port 'Success' (auto-terminated)")
        print("\n📮 Test con Postman:")
        print("   POST http://localhost:9092/sp02")
        print("   Body: file documento (PDF, DOC, etc.)")


    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()