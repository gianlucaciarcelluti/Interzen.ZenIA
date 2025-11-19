#!/usr/bin/env python3
"""Quick status check of NiFi canvas"""

import requests

api = "http://localhost:8080/nifi-api"

# Get root process groups
resp = requests.get(f"{api}/flow/process-groups/root")
flow_data = resp.json()

print("=" * 70)
print("  📊 NiFi Canvas - Riepilogo")
print("=" * 70)
print()

# Get process groups
resp = requests.get(f"{api}/process-groups/root/process-groups")
pgs = resp.json()['processGroups']

print(f"📦 Process Groups Totali: {len(pgs)}")
print()

for pg in pgs:
    name = pg['component']['name']
    pg_id = pg['id']
    running = pg.get('runningCount', 0)
    stopped = pg.get('stoppedCount', 0)
    invalid = pg.get('invalidCount', 0)
    
    print(f"✅ {name}")
    print(f"   ID: {pg_id}")
    print(f"   Running: {running}, Stopped: {stopped}, Invalid: {invalid}")
    
    # Get processors in this PG
    try:
        proc_resp = requests.get(f"{api}/process-groups/{pg_id}/processors")
        procs = proc_resp.json()['processors']
        if procs:
            print(f"   Processors ({len(procs)}):")
            for p in procs[:5]:  # Show first 5
                p_name = p['component']['name']
                p_state = p['component']['state']
                print(f"      - {p_name}: {p_state}")
            if len(procs) > 5:
                print(f"      ... e altri {len(procs)-5}")
    except:
        pass
    
    print()

print("=" * 70)
print()
print("🌐 NiFi UI: http://localhost:8080/nifi")
print()
