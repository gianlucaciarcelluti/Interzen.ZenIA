#!/usr/bin/env python3
"""
Script per connettere i processor audit ai flussi principali
"""

import requests
import json

NIFI_API = "http://localhost:8080/nifi-api"

def get_pg_id(name):
    """Get Process Group ID by name"""
    response = requests.get(f"{NIFI_API}/flow/process-groups/root")
    pgs = response.json()['processGroupFlow']['flow']['processGroups']
    for pg in pgs:
        if name in pg['component']['name']:
            return pg['id']
    return None

def get_processor_id(pg_id, name):
    """Get Processor ID by name within a PG"""
    response = requests.get(f"{NIFI_API}/process-groups/{pg_id}/processors")
    procs = response.json()['processors']
    for proc in procs:
        if name in proc['component']['name']:
            return proc['id']
    return None

def create_connection(pg_id, source_id, dest_id, relationships):
    """Create a connection"""
    connection_data = {
        "revision": {"version": 0},
        "component": {
            "source": {
                "id": source_id,
                "type": "PROCESSOR",
                "groupId": pg_id
            },
            "destination": {
                "id": dest_id,
                "type": "PROCESSOR",
                "groupId": pg_id
            },
            "selectedRelationships": relationships
        }
    }
    
    try:
        response = requests.post(
            f"{NIFI_API}/process-groups/{pg_id}/connections",
            json=connection_data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 409:
            return True  # Already exists
        print(f"Error: {e}")
        return False

def start_processor(proc_id):
    """Start a processor"""
    try:
        # Get current version
        response = requests.get(f"{NIFI_API}/processors/{proc_id}")
        version = response.json()['revision']['version']
        
        # Start processor
        requests.put(
            f"{NIFI_API}/processors/{proc_id}/run-status",
            json={
                "revision": {"version": version},
                "state": "RUNNING"
            },
            headers={"Content-Type": "application/json"}
        )
        return True
    except:
        return False

print("🔗 Connessione Audit Processors ai flussi principali\n")

# Ingress: HTTP → Audit
print("📦 Ingress_ContentListener")
ingress_pg = get_pg_id("Ingress")
if ingress_pg:
    http_id = get_processor_id(ingress_pg, "ContentListener_Fascicolo")
    audit_id = get_processor_id(ingress_pg, "Audit_HTTP_Endpoint")
    
    if http_id and audit_id:
        if create_connection(ingress_pg, http_id, audit_id, ["success"]):
            print("   ✅ HTTP → Audit")
            start_processor(audit_id)
        else:
            print("   ⚠️  Connessione già esistente")
    else:
        print(f"   ❌ Processor non trovati (HTTP:{http_id}, Audit:{audit_id})")

# SP01: Call_SP01 → Audit
print("\n📦 SP01_EML_Parser")
sp01_pg = get_pg_id("SP01")
if sp01_pg:
    call_sp01_id = get_processor_id(sp01_pg, "Call_SP01")
    audit_id = get_processor_id(sp01_pg, "Audit_Classification")
    
    if call_sp01_id and audit_id:
        if create_connection(sp01_pg, call_sp01_id, audit_id, ["Response"]):
            print("   ✅ Call_SP01 → Audit")
            start_processor(audit_id)
        else:
            print("   ⚠️  Connessione già esistente")
    else:
        print(f"   ❌ Processor non trovati")

print("\n✅ Completato!")
print("\n📋 Test:")
print("   curl -X POST http://localhost:9099/contentListener/fascicolo -d 'test'")
print("   docker exec postgres-db psql -U nifi -d nifi_audit -c 'SELECT * FROM workflow_executions ORDER BY started_at DESC LIMIT 3;'")
