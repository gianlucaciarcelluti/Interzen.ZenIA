#!/usr/bin/env python3
"""
Script per organizzare il layout interno dei processor all'interno dei process group.
Organizza i componenti in un flusso visuale chiaro da sinistra a destra.
"""

import requests
import json
from typing import Dict, List, Any

NIFI_URL = "http://localhost:8080/nifi-api"

def get_process_groups():
    """Ottiene tutti i process group root."""
    response = requests.get(f"{NIFI_URL}/process-groups/root/process-groups")
    response.raise_for_status()
    return response.json()['processGroups']

def get_pg_components(pg_id: str):
    """Ottiene tutti i componenti di un process group."""
    components = {}
    
    # Get processors
    resp = requests.get(f"{NIFI_URL}/process-groups/{pg_id}/processors")
    if resp.ok:
        components['processors'] = resp.json().get('processors', [])
    
    # Get input ports
    resp = requests.get(f"{NIFI_URL}/process-groups/{pg_id}/input-ports")
    if resp.ok:
        components['inputPorts'] = resp.json().get('inputPorts', [])
    
    # Get output ports
    resp = requests.get(f"{NIFI_URL}/process-groups/{pg_id}/output-ports")
    if resp.ok:
        components['outputPorts'] = resp.json().get('outputPorts', [])
    
    return components

def update_component_position(component_type: str, component_id: str, x: float, y: float, version: int):
    """Aggiorna la posizione di un componente."""
    
    endpoint_map = {
        'processor': 'processors',
        'input-port': 'input-ports',
        'output-port': 'output-ports'
    }
    
    endpoint = endpoint_map.get(component_type)
    if not endpoint:
        return False
    
    payload = {
        "revision": {"version": version},
        "component": {
            "id": component_id,
            "position": {"x": x, "y": y}
        }
    }
    
    response = requests.put(
        f"{NIFI_URL}/{endpoint}/{component_id}",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    return response.ok

def organize_pg_layout(pg_id: str, pg_name: str):
    """Organizza il layout interno di un process group."""
    
    print(f"\n🎨 Organizzazione layout: {pg_name}")
    
    components = get_pg_components(pg_id)
    
    # Layout configuration
    START_X = 100
    START_Y = 100
    SPACING_X = 350
    SPACING_Y = 150
    PORT_OFFSET_X = 50
    
    # Sort processors by current X position (mantiene l'ordine del flusso)
    processors = sorted(
        components.get('processors', []),
        key=lambda p: p['position']['x']
    )
    
    input_ports = components.get('inputPorts', [])
    output_ports = components.get('outputPorts', [])
    
    # Position input ports
    for i, port in enumerate(input_ports):
        x = START_X - PORT_OFFSET_X
        y = START_Y + (i * SPACING_Y)
        
        success = update_component_position(
            'input-port',
            port['id'],
            x, y,
            port['revision']['version']
        )
        
        if success:
            print(f"  ✅ Input Port '{port['component']['name']}' → ({x}, {y})")
    
    # Position processors in a horizontal flow
    for i, proc in enumerate(processors):
        x = START_X + (i * SPACING_X)
        y = START_Y
        
        success = update_component_position(
            'processor',
            proc['id'],
            x, y,
            proc['revision']['version']
        )
        
        if success:
            proc_name = proc['component']['name']
            # Truncate long names for display
            display_name = proc_name[:30] + '...' if len(proc_name) > 30 else proc_name
            print(f"  ✅ Processor '{display_name}' → ({x}, {y})")
    
    # Position output ports (vertically stacked on the right)
    output_start_x = START_X + (len(processors) * SPACING_X)
    
    for i, port in enumerate(output_ports):
        x = output_start_x
        y = START_Y + (i * SPACING_Y) - (SPACING_Y // 2 if len(output_ports) > 1 else 0)
        
        success = update_component_position(
            'output-port',
            port['id'],
            x, y,
            port['revision']['version']
        )
        
        if success:
            print(f"  ✅ Output Port '{port['component']['name']}' → ({x}, {y})")

def main():
    print("=" * 70)
    print("🎨 Organizzazione Layout Interno Process Groups")
    print("=" * 70)
    
    try:
        process_groups = get_process_groups()
        
        if not process_groups:
            print("\n⚠️  Nessun process group trovato")
            return
        
        print(f"\n📊 Trovati {len(process_groups)} process group\n")
        
        for pg in process_groups:
            pg_id = pg['id']
            pg_name = pg['component']['name']
            
            organize_pg_layout(pg_id, pg_name)
        
        print("\n" + "=" * 70)
        print("✅ Layout interno organizzato per tutti i process group!")
        print("=" * 70)
        print("\n💡 Apri NiFi UI e fai doppio click su un process group per vedere il layout")
        print("   URL: http://localhost:8080/nifi")
        
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
