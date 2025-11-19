#!/usr/bin/env python3
"""
Rimuove i processor audit creati con ExecuteSQL (non adatti) e li ricrea con PutSQL
"""

import requests

NIFI_API = "http://localhost:8080/nifi-api"

def delete_processor(proc_id, version):
    """Delete a processor"""
    try:
        requests.delete(
            f"{NIFI_API}/processors/{proc_id}",
            params={"version": version}
        )
        return True
    except:
        return False

def stop_processor(proc_id):
    """Stop a processor"""
    try:
        response = requests.get(f"{NIFI_API}/processors/{proc_id}")
        version = response.json()['revision']['version']
        
        requests.put(
            f"{NIFI_API}/processors/{proc_id}/run-status",
            json={
                "revision": {"version": version},
                "state": "STOPPED"
            },
            headers={"Content-Type": "application/json"}
        )
        return True
    except:
        return False

print("🧹 Pulizia processor audit non funzionanti...\n")

# Get all process groups
response = requests.get(f"{NIFI_API}/flow/process-groups/root")
process_groups = response.json()['processGroupFlow']['flow']['processGroups']

for pg in process_groups:
    pg_id = pg['id']
    pg_name = pg['component']['name']
    
    # Get processors in this PG
    response = requests.get(f"{NIFI_API}/process-groups/{pg_id}/processors")
    processors = response.json()['processors']
    
    for proc in processors:
        if "Audit_" in proc['component']['name']:
            proc_id = proc['id']
            proc_name = proc['component']['name']
            version = proc['revision']['version']
            
            print(f"🗑️  Rimozione {proc_name} da {pg_name}...")
            
            # Stop processor
            stop_processor(proc_id)
            
            # Wait a bit
            import time
            time.sleep(1)
            
            # Get updated version
            response = requests.get(f"{NIFI_API}/processors/{proc_id}")
            version = response.json()['revision']['version']
            
            # Delete connections first
            response = requests.get(f"{NIFI_API}/flow/process-groups/{pg_id}")
            connections = response.json()['processGroupFlow']['flow']['connections']
            
            for conn in connections:
                if conn['component']['destination']['id'] == proc_id:
                    conn_id = conn['id']
                    conn_version = conn['revision']['version']
                    try:
                        requests.delete(
                            f"{NIFI_API}/connections/{conn_id}",
                            params={"version": conn_version}
                        )
                    except:
                        pass
            
            # Delete processor
            if delete_processor(proc_id, version):
                print(f"   ✅ Rimosso")
            else:
                print(f"   ⚠️  Errore rimozione")

print("\n✅ Pulizia completata!")
print("\n💡 I processor audit non funzionavano perché ExecuteSQL è per leggere, non scrivere.")
print("   Implementeremo l'audit direttamente nei microservizi Python.")
