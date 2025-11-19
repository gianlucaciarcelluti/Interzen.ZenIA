#!/usr/bin/env python3
"""
Compact Process Groups Layout
==============================
Compacts the vertical spacing of Process Groups in the root canvas
to improve space utilization and readability.

Usage:
    python3 compact-pg-layout.py
"""

import requests
import sys
from typing import List, Dict

class CanvasCompactor:
    def __init__(self, nifi_url: str = "http://localhost:8080"):
        self.nifi_url = nifi_url
        self.api_url = f"{nifi_url}/nifi-api"
        self.session = requests.Session()
        
    def get_root_pg_id(self) -> str:
        """Get root process group ID"""
        response = self.session.get(f"{self.api_url}/flow/process-groups/root")
        response.raise_for_status()
        return response.json()['processGroupFlow']['id']
    
    def get_all_process_groups(self) -> List[Dict]:
        """Get all process groups in root"""
        root_id = self.get_root_pg_id()
        response = self.session.get(f"{self.api_url}/process-groups/{root_id}/process-groups")
        response.raise_for_status()
        return response.json()['processGroups']
    
    def update_pg_position(self, pg_id: str, revision: Dict, x: float, y: float) -> bool:
        """Update process group position"""
        try:
            update_data = {
                "revision": revision,
                "component": {
                    "id": pg_id,
                    "position": {"x": x, "y": y}
                }
            }
            
            response = self.session.put(
                f"{self.api_url}/process-groups/{pg_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore update: {e}")
            return False
    
    def compact_layout(self):
        """Compact Process Groups in a logical grid layout"""
        print("=" * 70)
        print("  📐 Compattazione Layout Process Groups")
        print("=" * 70)
        print()
        
        # Get all process groups
        print("[1/2] 🔍 Analisi Process Groups...")
        pgs = self.get_all_process_groups()
        print(f"   Trovati {len(pgs)} Process Groups")
        print()
        
        # Define logical order: Ingress + SP01 first, then others by number
        print("[2/2] 📦 Riposizionamento in griglia logica...")
        
        # Create name-to-PG mapping
        pg_map = {pg['component']['name']: pg for pg in pgs}
        
        # Define logical order
        priority_order = [
            'Ingress_ContentListener',
            'SP01_EML_Parser',
            'SP02_Document_Extractor',
            'SP03_Procedural_Classifier',
            'SP04_Knowledge_Base',
            'SP05_Template_Engine',
            'SP06_Validator',
            'SP07_Content_Classifier',
            'SP08_Quality_Checker',
            'SP11_Security_Audit',
        ]
        
        # Build ordered list
        pgs_ordered = []
        for name in priority_order:
            for pg_name, pg in pg_map.items():
                if name in pg_name:
                    pgs_ordered.append(pg)
                    break
        
        # Add any remaining PGs not in the list
        for pg in pgs:
            if pg not in pgs_ordered:
                pgs_ordered.append(pg)
        
        # Define grid layout: 4 columns x 3 rows
        COLUMN_WIDTH = 400  # Horizontal spacing (increased to avoid overlap)
        ROW_HEIGHT = 200    # Vertical spacing
        START_X = 100       # Left margin
        START_Y = 80        # Top margin
        COLUMNS = 4         # Number of columns
        
        updated = 0
        
        for idx, pg in enumerate(pgs_ordered):
            pg_id = pg['id']
            name = pg['component']['name']
            revision = pg['revision']
            
            # Calculate grid position
            col = idx % COLUMNS
            row = idx // COLUMNS
            
            new_x = START_X + (col * COLUMN_WIDTH)
            new_y = START_Y + (row * ROW_HEIGHT)
            
            current_x = pg['component']['position']['x']
            current_y = pg['component']['position']['y']
            
            # Update if position changed
            if current_x != new_x or current_y != new_y:
                if self.update_pg_position(pg_id, revision, new_x, new_y):
                    print(f"   📍 {name:35} ({current_x:4.0f}, {current_y:4.0f}) → ({new_x:4.0f}, {new_y:4.0f})")
                    updated += 1
        
        print()
        print(f"   ✅ Riposizionati {updated}/{len(pgs)} Process Groups")
        print()
        
        # Summary
        print("=" * 70)
        print("  ✅ Layout Logico Compattato")
        print("=" * 70)
        print()
        print("📊 Configurazione griglia:")
        print(f"   - Colonne: {COLUMNS}")
        print(f"   - Righe: {(len(pgs_ordered) + COLUMNS - 1) // COLUMNS}")
        print(f"   - Spaziatura verticale: {ROW_HEIGHT}px")
        print(f"   - Spaziatura orizzontale: {COLUMN_WIDTH}px")
        print()
        print("📦 Layout organizzato:")
        print()
        print("   Riga 1 (Ingress + Core):")
        
        # Show layout by rows
        rows_count = (len(pgs_ordered) + COLUMNS - 1) // COLUMNS
        for row in range(rows_count):
            if row == 0:
                pass  # Already printed header
            else:
                print(f"\n   Riga {row + 1}:")
            
            for col in range(COLUMNS):
                idx = row * COLUMNS + col
                if idx < len(pgs_ordered):
                    pg = pgs_ordered[idx]
                    name = pg['component']['name']
                    x = START_X + (col * COLUMN_WIDTH)
                    y = START_Y + (row * ROW_HEIGHT)
                    print(f"      Col {col + 1}: {name:35} @ ({x:4.0f}, {y:4.0f})")
        
        print()
        print("🔗 Connessioni principali:")
        print("   - Ingress_ContentListener → SP01_EML_Parser (porta .eml)")
        print()
        print(f"🌐 Visualizza risultato: {self.nifi_url}/nifi")
        print()
        print("💡 Suggerimento: Usa 'Fit to Screen' per vedere tutto il canvas")
        print()

def main():
    try:
        compactor = CanvasCompactor()
        compactor.compact_layout()
        
    except KeyboardInterrupt:
        print("\n\n❌ Operazione annullata")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
