#!/usr/bin/env python3
"""
Add audit logging processors to existing NiFi workflows
This script adds PutDatabaseRecord processors to track workflow executions
"""

import requests
import json
import time
import uuid
from typing import Dict, List, Optional

NIFI_URL = "http://localhost:8080/nifi-api"

# Workflow configurations
WORKFLOWS = [
    "SP01_EML_Parser",
    "SP02_Document_Extractor", 
    "SP03_Procedural_Classifier",
    "SP04_Knowledge_Base",
    "SP05_Template_Engine",
    "SP06_Validator",
    "SP07_Content_Classifier",
    "SP08_Quality_Checker",
    "SP11_Security_Audit"
]


def get_process_groups() -> List[Dict]:
    """Get all process groups from root"""
    response = requests.get(f"{NIFI_URL}/process-groups/root/process-groups")
    response.raise_for_status()
    return response.json()["processGroups"]


def get_processors_in_group(pg_id: str) -> List[Dict]:
    """Get all processors in a process group"""
    response = requests.get(f"{NIFI_URL}/process-groups/{pg_id}/processors")
    response.raise_for_status()
    return response.json()["processors"]


def get_connections_in_group(pg_id: str) -> List[Dict]:
    """Get all connections in a process group"""
    response = requests.get(f"{NIFI_URL}/process-groups/{pg_id}/connections")
    response.raise_for_status()
    return response.json()["connections"]


def create_audit_processor(pg_id: str, workflow_name: str, position: Dict) -> Dict:
    """Create a PutDatabaseRecord processor for audit logging"""
    
    processor_config = {
        "revision": {
            "version": 0
        },
        "component": {
            "type": "org.apache.nifi.processors.standard.PutDatabaseRecord",
            "name": f"Audit_Log_{workflow_name}",
            "position": position,
            "config": {
                "properties": {
                    "put-db-record-record-reader-factory": None,  # Will be set to JsonTreeReader
                    "put-db-record-dcbp-service": None,  # Will be set to PostgreSQL pool
                    "put-db-record-statement-type": "INSERT",
                    "put-db-record-catalog-name": None,
                    "put-db-record-schema-name": "public",
                    "put-db-record-table-name": "workflow_executions",
                    "put-db-record-translate-field-names": "true",
                    "put-db-record-unmatched-field-behavior": "Ignore Unmatched Fields",
                    "put-db-record-unmatched-column-behavior": "Fail on Unmatched Columns",
                    "put-db-record-update-keys": None,
                    "put-db-record-field-containing-sql": None,
                    "put-db-record-allow-multiple-statements": "false",
                    "put-db-record-quote-identifiers": "false",
                    "put-db-record-quote-table-identifier": "false",
                    "put-db-record-query-timeout": "0 seconds",
                    "put-db-record-rollback-on-failure": "false",
                    "put-db-record-table-schema-cache-size": "100",
                    "put-db-record-max-batch-size": "0"
                },
                "schedulingPeriod": "0 sec",
                "schedulingStrategy": "TIMER_DRIVEN",
                "executionNode": "ALL",
                "penaltyDuration": "30 sec",
                "yieldDuration": "1 sec",
                "bulletinLevel": "WARN",
                "runDurationMillis": 0,
                "concurrentlySchedulableTaskCount": 1,
                "autoTerminatedRelationships": ["success", "retry", "failure"],
                "comments": f"Logs workflow execution to nifi_audit database for {workflow_name}"
            }
        }
    }
    
    response = requests.post(
        f"{NIFI_URL}/process-groups/{pg_id}/processors",
        headers={"Content-Type": "application/json"},
        data=json.dumps(processor_config)
    )
    response.raise_for_status()
    return response.json()


def create_update_attribute_processor(pg_id: str, workflow_name: str, position: Dict) -> Dict:
    """Create UpdateAttribute processor to add audit metadata"""
    
    processor_config = {
        "revision": {
            "version": 0
        },
        "component": {
            "type": "org.apache.nifi.processors.attributes.UpdateAttribute",
            "name": f"Add_Audit_Metadata_{workflow_name}",
            "position": position,
            "config": {
                "properties": {
                    "Delete Attributes Expression": None,
                    "Store State": "Do not store state",
                    "Stateful Variables Initial Value": None,
                    # Custom attributes for audit logging
                    "execution_id": "${UUID()}",
                    "workflow_name": workflow_name,
                    "started_at": "${now():format('yyyy-MM-dd HH:mm:ss')}",
                    "status": "RUNNING",
                    "flowfile_id": "${uuid}"
                },
                "schedulingPeriod": "0 sec",
                "schedulingStrategy": "TIMER_DRIVEN",
                "executionNode": "ALL",
                "penaltyDuration": "30 sec",
                "yieldDuration": "1 sec",
                "bulletinLevel": "WARN",
                "runDurationMillis": 0,
                "concurrentlySchedulableTaskCount": 1,
                "autoTerminatedRelationships": [],
                "comments": f"Adds audit metadata attributes for {workflow_name}"
            }
        }
    }
    
    response = requests.post(
        f"{NIFI_URL}/process-groups/{pg_id}/processors",
        headers={"Content-Type": "application/json"},
        data=json.dumps(processor_config)
    )
    response.raise_for_status()
    return response.json()


def create_attribute_to_json_processor(pg_id: str, workflow_name: str, position: Dict) -> Dict:
    """Create AttributesToJSON processor to convert attributes to JSON for logging"""
    
    processor_config = {
        "revision": {
            "version": 0
        },
        "component": {
            "type": "org.apache.nifi.processors.standard.AttributesToJSON",
            "name": f"Prepare_Audit_JSON_{workflow_name}",
            "position": position,
            "config": {
                "properties": {
                    "Attributes List": "execution_id,workflow_name,started_at,status,flowfile_id",
                    "Attributes Regular Expression": None,
                    "Destination": "flowfile-content",
                    "Include Core Attributes": "false",
                    "Null Value": "false"
                },
                "schedulingPeriod": "0 sec",
                "schedulingStrategy": "TIMER_DRIVEN",
                "executionNode": "ALL",
                "penaltyDuration": "30 sec",
                "yieldDuration": "1 sec",
                "bulletinLevel": "WARN",
                "runDurationMillis": 0,
                "concurrentlySchedulableTaskCount": 1,
                "autoTerminatedRelationships": [],
                "comments": f"Converts audit attributes to JSON for database insertion"
            }
        }
    }
    
    response = requests.post(
        f"{NIFI_URL}/process-groups/{pg_id}/processors",
        headers={"Content-Type": "application/json"},
        data=json.dumps(processor_config)
    )
    response.raise_for_status()
    return response.json()


def create_connection(pg_id: str, source_id: str, dest_id: str, relationships: List[str]) -> Dict:
    """Create a connection between processors"""
    
    connection_config = {
        "revision": {
            "version": 0
        },
        "component": {
            "source": {
                "id": source_id,
                "type": "PROCESSOR"
            },
            "destination": {
                "id": dest_id,
                "type": "PROCESSOR"
            },
            "selectedRelationships": relationships,
            "backPressureDataSizeThreshold": "1 GB",
            "backPressureObjectThreshold": "10000",
            "flowFileExpiration": "0 sec",
            "prioritizers": []
        }
    }
    
    response = requests.post(
        f"{NIFI_URL}/process-groups/{pg_id}/connections",
        headers={"Content-Type": "application/json"},
        data=json.dumps(connection_config)
    )
    response.raise_for_status()
    return response.json()


def add_audit_to_workflow(pg_id: str, workflow_name: str):
    """Add audit logging chain to a workflow"""
    
    print(f"\n🔍 Processing workflow: {workflow_name}")
    
    # Get existing processors
    processors = get_processors_in_group(pg_id)
    
    # Find HTTP_Endpoint processor (entry point)
    http_endpoint = None
    for proc in processors:
        if proc["component"]["name"] == "HTTP_Endpoint":
            http_endpoint = proc
            break
    
    if not http_endpoint:
        print(f"  ⚠️  HTTP_Endpoint not found in {workflow_name}, skipping")
        return
    
    # Check if audit processors already exist
    existing_audit = any(
        "Audit" in proc["component"]["name"] or "Add_Audit_Metadata" in proc["component"]["name"]
        for proc in processors
    )
    
    if existing_audit:
        print(f"  ✅ Audit processors already exist in {workflow_name}")
        return
    
    # Calculate positions for new processors
    http_pos = http_endpoint["component"]["position"]
    
    # Positions: UpdateAttribute -> AttributesToJSON -> PutDatabaseRecord
    update_attr_pos = {"x": http_pos["x"], "y": http_pos["y"] + 200}
    attr_to_json_pos = {"x": http_pos["x"], "y": http_pos["y"] + 350}
    audit_log_pos = {"x": http_pos["x"], "y": http_pos["y"] + 500}
    
    print(f"  📝 Creating UpdateAttribute processor...")
    update_attr_proc = create_update_attribute_processor(pg_id, workflow_name, update_attr_pos)
    
    print(f"  📝 Creating AttributesToJSON processor...")
    attr_to_json_proc = create_attribute_to_json_processor(pg_id, workflow_name, attr_to_json_pos)
    
    print(f"  📝 Creating PutDatabaseRecord audit processor...")
    audit_proc = create_audit_processor(pg_id, workflow_name, audit_log_pos)
    
    # Create connections
    print(f"  🔗 Creating connections...")
    
    # HTTP_Endpoint -> UpdateAttribute (clone the original success relationship)
    create_connection(pg_id, http_endpoint["id"], update_attr_proc["id"], ["Response"])
    
    # UpdateAttribute -> AttributesToJSON
    create_connection(pg_id, update_attr_proc["id"], attr_to_json_proc["id"], ["success"])
    
    # AttributesToJSON -> PutDatabaseRecord
    create_connection(pg_id, attr_to_json_proc["id"], audit_proc["id"], ["success"])
    
    print(f"  ✅ Audit chain added to {workflow_name}")


def main():
    """Main execution"""
    print("=" * 60)
    print("🔧 Adding Audit Logging to NiFi Workflows")
    print("=" * 60)
    
    # Get all process groups
    process_groups = get_process_groups()
    
    # Process each workflow
    for workflow_name in WORKFLOWS:
        # Find matching process group
        pg = next((pg for pg in process_groups if pg["component"]["name"] == workflow_name), None)
        
        if not pg:
            print(f"\n⚠️  Workflow {workflow_name} not found, skipping")
            continue
        
        try:
            add_audit_to_workflow(pg["id"], workflow_name)
        except Exception as e:
            print(f"  ❌ Error processing {workflow_name}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("✅ Audit logging setup complete!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("  1. Configure JsonTreeReader controller service")
    print("  2. Link PutDatabaseRecord processors to PostgreSQL pool")
    print("  3. Start the audit processors")
    print("  4. Test with sample requests")
    print("\n💡 Note: You'll need to manually configure controller services")
    print("   via NiFi UI at http://localhost:8080/nifi")


if __name__ == "__main__":
    main()
