#!/usr/bin/env python3
"""
Script per aggiungere processor di audit a tutti i Process Groups
Ogni PG scriverà nel database nifi_audit per tracciare l'esecuzione del workflow
"""

import requests
import json
import time
from typing import Optional, Dict

class AuditInjector:
    def __init__(self, nifi_url="http://localhost:8080"):
        self.api_url = f"{nifi_url}/nifi-api"
        self.session = requests.Session()
        self.content_type = "application/json"
        
        # Get PostgreSQL Controller Service ID
        self.pg_pool_id = self._get_controller_service_id("PostgreSQL-Connection-Pool")
        
    def _get_controller_service_id(self, name: str) -> Optional[str]:
        """Get Controller Service ID by name"""
        try:
            response = self.session.get(
                f"{self.api_url}/flow/process-groups/root/controller-services"
            )
            response.raise_for_status()
            services = response.json()['controllerServices']
            
            for service in services:
                if service['component']['name'] == name:
                    return service['id']
            
            print(f"   ⚠️  Controller Service '{name}' non trovato")
            return None
            
        except Exception as e:
            print(f"   ❌ Errore recupero Controller Service: {e}")
            return None
    
    def create_audit_processor(self, pg_id: str, step_name: str, 
                                x: float = 800, y: float = 300) -> Optional[str]:
        """
        Crea un processor PutSQL per scrivere nel database audit
        
        Parametri SQL (in ordine):
        1. execution_id (da attribute workflow_id)
        2. workflow_name (da attribute workflow_name) 
        3. step_name (passato come parametro)
        4. output_data (da content del FlowFile)
        """
        
        if not self.pg_pool_id:
            print("   ⚠️  PostgreSQL Pool non disponibile, skip audit")
            return None
        
        try:
            sql_statement = """
INSERT INTO workflow_executions (
    execution_id, workflow_name, step_name, 
    status, output_data, started_at
) VALUES (
    ?, ?, ?, 'SUCCESS', ?, CURRENT_TIMESTAMP
) ON CONFLICT (execution_id, workflow_name, step_name) DO UPDATE SET
    completed_at = CURRENT_TIMESTAMP,
    status = EXCLUDED.status,
    output_data = EXCLUDED.output_data,
    duration_ms = EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - workflow_executions.started_at)) * 1000;
            """.strip()
            
            processor_data = {
                "revision": {"version": 0},
                "component": {
                    "type": "org.apache.nifi.processors.standard.PutSQL",
                    "name": f"Audit_{step_name}",
                    "position": {"x": x, "y": y},
                    "config": {
                        "properties": {
                            "Database Connection Pooling Service": self.pg_pool_id,
                            "SQL Statement": sql_statement,
                            "Support Fragmented Transactions": "false",
                            "Batch Size": "1"
                        },
                        "autoTerminatedRelationships": ["success", "failure"]
                    }
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{pg_id}/processors",
                json=processor_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            
            processor_id = response.json()['id']
            print(f"   ✅ Audit processor creato: Audit_{step_name}")
            return processor_id
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                print("   📌 Audit processor già esistente")
                return self._get_existing_audit_processor(pg_id, f"Audit_{step_name}")
            else:
                print(f"   ❌ Errore creazione audit: {e}")
                return None
        except Exception as e:
            print(f"   ❌ Errore: {e}")
            return None
    
    def _get_existing_audit_processor(self, pg_id: str, name: str) -> Optional[str]:
        """Get existing audit processor ID"""
        try:
            response = self.session.get(
                f"{self.api_url}/process-groups/{pg_id}/processors"
            )
            response.raise_for_status()
            processors = response.json()['processors']
            
            for proc in processors:
                if proc['component']['name'] == name:
                    return proc['id']
            
            return None
        except Exception:
            return None
    
    def add_connection(self, pg_id: str, source_id: str, dest_id: str, 
                      relationships: list, source_type="PROCESSOR", dest_type="PROCESSOR") -> bool:
        """Create connection between processors"""
        try:
            connection_data = {
                "revision": {"version": 0},
                "component": {
                    "source": {
                        "id": source_id,
                        "type": source_type,
                        "groupId": pg_id
                    },
                    "destination": {
                        "id": dest_id,
                        "type": dest_type,
                        "groupId": pg_id
                    },
                    "selectedRelationships": relationships
                }
            }
            
            response = self.session.post(
                f"{self.api_url}/process-groups/{pg_id}/connections",
                json=connection_data,
                headers={"Content-Type": self.content_type}
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                return True  # Already exists
            print(f"   ⚠️  Connessione già esistente o errore: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Errore connessione: {e}")
            return False

def main():
    print("="*70)
    print("  Aggiunta Audit Tracking ai Process Groups")
    print("="*70)
    
    injector = AuditInjector()
    
    if not injector.pg_pool_id:
        print("\n❌ PostgreSQL Connection Pool non trovato!")
        print("   Esegui prima: ./enable-controller-services.sh")
        return
    
    # Get all Process Groups
    response = requests.get(f"{injector.api_url}/flow/process-groups/root")
    process_groups = response.json()['processGroupFlow']['flow']['processGroups']
    
    print(f"\n📦 Trovati {len(process_groups)} Process Groups\n")
    
    for pg in process_groups:
        pg_id = pg['id']
        pg_name = pg['component']['name']
        
        print(f"🔧 {pg_name}")
        
        # Define audit points based on PG name
        if "Ingress" in pg_name:
            injector.create_audit_processor(pg_id, "HTTP_Endpoint", x=600, y=100)
        elif "SP01" in pg_name:
            injector.create_audit_processor(pg_id, "Classification_Result", x=600, y=300)
        elif "SP11" in pg_name:
            injector.create_audit_processor(pg_id, "HITL_Decision", x=600, y=300)
        else:
            # Generic audit for other PGs
            injector.create_audit_processor(pg_id, "Processing_Complete", x=600, y=300)
        
        print()
    
    print("="*70)
    print("  ✅ Audit Tracking Configurato")
    print("="*70)
    print("\n📋 Prossimi passi:")
    print("   1. Connetti manualmente gli audit processor ai flussi principali")
    print("   2. Testa inviando un'email: curl -X POST http://localhost:9099/contentListener/fascicolo")
    print("   3. Verifica il database: SELECT * FROM workflow_executions;")

if __name__ == "__main__":
    main()
