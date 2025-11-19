#!/usr/bin/env python3
"""
Script per creare il flusso SP05 via API NiFi (senza template).
SP05 - Template Engine (usa Groq per generazione documenti)
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


def build_sp05(builder: NiFiFlowBuilder):
    """
    Costruisce il flusso SP05 - Template Engine.

    Architettura semplificata:
    - ListenHTTP (porta 9095) -> riceve POST HTTP con metadati documento
    - InvokeHTTP -> chiama servizio template engine (placeholder per ora)
    - Output Port "Success" -> documento generato (auto-terminated)
    """
    print("🏗️  Costruzione SP05 - Template Engine...")

    # 1. Crea Process Group
    pg = builder.create_process_group("SP05_Template_Engine")
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
                "Listening Port": "9095",
                "Base Path": "sp05"
            }
        }
    )
    listen_id = listen_http["id"]
    print(f"  ✅ ListenHTTP creato: {listen_id} (porta 9095)")

    # 3. Crea InvokeHTTP (chiama servizio template engine - placeholder)
    # Nota: Per ora punta a un servizio placeholder, in produzione userà Groq
    invoke_http = builder.create_processor(
        pg_id,
        "org.apache.nifi.processors.standard.InvokeHTTP",
        "Call_SP05_Template_Engine",
        x=300, y=100,
        config={
            "properties": {
                "HTTP Method": "POST",
                "Remote URL": "http://sp05-template-engine:5005/generate",  # Placeholder
                "Content-Type": "application/json"
            },
            "autoTerminatedRelationships": ["Failure", "Retry", "No Retry", "Original"]
        }
    )
    invoke_id = invoke_http["id"]
    print(f"  ✅ InvokeHTTP creato: {invoke_id} (placeholder)")

    # 4. Crea Output Port "Success" (auto-terminated)
    success_port = builder.create_output_port(pg_id, "Success", x=500, y=100)
    success_port_id = success_port["id"]
    print(f"  ✅ Output Port 'Success' creato: {success_port_id}")

    # 5. Crea Connessioni
    print("  🔗 Creazione connessioni...")

    # ListenHTTP -> InvokeHTTP
    builder.create_connection(pg_id, listen_id, invoke_id, ["success"])
    print("    ✅ ListenHTTP → InvokeHTTP")

    # InvokeHTTP -> Success Port (Response relationship)
    builder.create_connection(pg_id, invoke_id, success_port_id, ["Response"],
                             dest_type="OUTPUT_PORT")
    print("    ✅ InvokeHTTP → Success (auto-terminated)")

    print(f"\n🎉 SP05 costruito con successo! Process Group ID: {pg_id}")
    print("   ⚠️  Nota: Servizio SP05 è placeholder - implementare con Groq API")
    return pg_id


if __name__ == "__main__":
    print("=" * 60)
    print("NiFi Flow Builder - SP05 Template Engine")
    print("=" * 60)
    print()

    builder = NiFiFlowBuilder(NIFI_URL)

    try:
        sp05_id = build_sp05(builder)

        print("\n" + "=" * 60)
        print("✅ COMPLETATO!")
        print("=" * 60)
        print(f"\nProcess Group SP05 ID: {sp05_id}")
        print("\nAccedi a NiFi UI: http://localhost:8080/nifi")
        print("Vedrai il process group 'SP05_Template_Engine' con:")
        print("  - ListenHTTP su porta 9095 (endpoint: POST http://localhost:9095/sp05)")
        print("  - InvokeHTTP per chiamare servizio template (placeholder)")
        print("  - Output Port 'Success' (auto-terminated)")
        print("\n⚠️  ATTENZIONE:")
        print("   Il servizio SP05 deve essere implementato per usare Groq API")
        print("   per generazione documenti basata su template.")


    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()