import requests
import json

response = requests.get("http://localhost:8080/nifi-api/process-groups/root")
data = response.json()
flow = data["processGroupFlow"]["flow"]

print("=" * 70)
print("  📊 Canvas Root - Stato Finale")
print("=" * 70)
print()

# Process Groups
pgs = flow.get("processGroups", [])
print(f"📦 Process Groups ({len(pgs)}):")
for pg in pgs:
    name = pg["component"]["name"]
    count = pg["runningCount"]
    stopped = pg["stoppedCount"]
    print(f"   ✅ {name}")
    print(f"      Running: {count}, Stopped: {stopped}")
print()

# Processors
processors = flow.get("processors", [])
print(f"⚙️  Processors nel root: {len(processors)}")
if processors:
    for p in processors:
        print(f"   - {p['component']['name']}")
else:
    print("   ✅ Nessun processor loose (tutto organizzato in PG!)")
print()

print("🎨 Canvas organizzato con Process Groups modulari!")
print("   Visualizza: http://localhost:8080/nifi")
