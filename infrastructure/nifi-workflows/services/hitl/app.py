"""
HITL Manager Service - Human in the Loop
Gestisce i punti di decisione umana nel workflow
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import hashlib
import json

app = FastAPI(title="HITL Manager Service", version="1.0.0")

# Database configuration
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "database": os.getenv("POSTGRES_DB", "provvedimenti"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "port": int(os.getenv("POSTGRES_PORT", 5432))
}


class HITLCheckpoint(BaseModel):
    workflow_id: str
    checkpoint_name: str
    ai_suggestion: Dict[str, Any]
    ai_confidence: Optional[float] = None
    timeout_minutes: Optional[int] = None


class HITLDecision(BaseModel):
    action: str  # CONFIRMED, MODIFIED, REJECTED
    user_changes: Optional[Dict[str, Any]] = None
    modification_reason: Optional[str] = None
    session_id: Optional[str] = None


class DocumentVersion(BaseModel):
    workflow_id: str
    content: str
    created_by: str
    is_ai_generated: bool
    hitl_interaction_id: Optional[int] = None


def get_db_connection():
    """Crea connessione al database"""
    return psycopg2.connect(**DB_CONFIG)


def calculate_content_hash(content: str) -> str:
    """Calcola SHA256 hash del contenuto"""
    return hashlib.sha256(content.encode()).hexdigest()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "hitl-manager",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/hitl/checkpoint/create")
async def create_checkpoint(checkpoint: HITLCheckpoint):
    """
    Crea un nuovo checkpoint HITL
    
    Il workflow si fermerà qui fino a che l'utente non prende una decisione
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Calcola timeout se specificato
        timeout_at = None
        if checkpoint.timeout_minutes:
            timeout_at = datetime.now() + timedelta(minutes=checkpoint.timeout_minutes)
        
        # Inserisci checkpoint
        cur.execute("""
            INSERT INTO hitl_checkpoints 
            (workflow_id, checkpoint_name, status, data, timeout_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            checkpoint.workflow_id,
            checkpoint.checkpoint_name,
            'WAITING_USER',
            json.dumps({
                'ai_suggestion': checkpoint.ai_suggestion,
                'ai_confidence': checkpoint.ai_confidence
            }),
            timeout_at
        ))
        
        checkpoint_id = cur.fetchone()['id']
        
        # Pubblica evento Kafka (simulato)
        # TODO: Integrare con Kafka reale
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "checkpoint_id": checkpoint_id,
            "status": "WAITING_USER",
            "workflow_id": checkpoint.workflow_id,
            "timeout_at": timeout_at.isoformat() if timeout_at else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/hitl/checkpoint/{workflow_id}/{checkpoint_name}")
async def get_checkpoint(workflow_id: str, checkpoint_name: str):
    """
    Recupera i dati di un checkpoint per mostrare all'utente
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT * FROM hitl_checkpoints
            WHERE workflow_id = %s 
            AND checkpoint_name = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (workflow_id, checkpoint_name))
        
        checkpoint = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not checkpoint:
            raise HTTPException(status_code=404, detail="Checkpoint not found")
        
        return {
            "checkpoint_id": checkpoint['id'],
            "workflow_id": checkpoint['workflow_id'],
            "checkpoint_name": checkpoint['checkpoint_name'],
            "status": checkpoint['status'],
            "ai_suggestion": checkpoint['data'].get('ai_suggestion'),
            "ai_confidence": checkpoint['data'].get('ai_confidence'),
            "created_at": checkpoint['created_at'].isoformat(),
            "timeout_at": checkpoint['timeout_at'].isoformat() if checkpoint['timeout_at'] else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/hitl/checkpoint/{checkpoint_id}/decision")
async def submit_decision(
    checkpoint_id: int,
    decision: HITLDecision,
    user_id: str,
    background_tasks: BackgroundTasks
):
    """
    Utente invia la sua decisione su un checkpoint
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Recupera checkpoint
        cur.execute("""
            SELECT * FROM hitl_checkpoints
            WHERE id = %s
        """, (checkpoint_id,))
        
        checkpoint = cur.fetchone()
        
        if not checkpoint:
            raise HTTPException(status_code=404, detail="Checkpoint not found")
        
        if checkpoint['status'] != 'WAITING_USER':
            raise HTTPException(
                status_code=400,
                detail=f"Checkpoint already resolved with status: {checkpoint['status']}"
            )
        
        # Calcola tempo di decisione
        time_to_decision = datetime.now() - checkpoint['created_at']
        
        # Inserisci interazione HITL
        cur.execute("""
            INSERT INTO hitl_interactions
            (workflow_id, hitl_point, ai_suggestion, ai_confidence,
             user_action, user_id, user_changes, modification_reason,
             time_to_decision, session_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            checkpoint['workflow_id'],
            checkpoint['checkpoint_name'],
            json.dumps(checkpoint['data'].get('ai_suggestion')),
            checkpoint['data'].get('ai_confidence'),
            decision.action,
            user_id,
            json.dumps(decision.user_changes) if decision.user_changes else None,
            decision.modification_reason,
            time_to_decision,
            decision.session_id
        ))
        
        interaction_id = cur.fetchone()['id']
        
        # Aggiorna checkpoint
        new_status = 'CONFIRMED' if decision.action == 'CONFIRMED' else 'REJECTED'
        
        cur.execute("""
            UPDATE hitl_checkpoints
            SET status = %s,
                resolved_at = NOW(),
                updated_at = NOW()
            WHERE id = %s
        """, (new_status, checkpoint_id))
        
        # Audit log
        cur.execute("""
            INSERT INTO audit_logs
            (workflow_id, user_id, action, resource, details)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            checkpoint['workflow_id'],
            user_id,
            f"HITL_DECISION_{decision.action}",
            f"checkpoint/{checkpoint_id}",
            json.dumps({
                'checkpoint_name': checkpoint['checkpoint_name'],
                'action': decision.action,
                'time_to_decision_seconds': time_to_decision.total_seconds()
            })
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Notifica workflow engine (in background)
        background_tasks.add_task(
            notify_workflow_engine,
            checkpoint['workflow_id'],
            checkpoint['checkpoint_name'],
            decision.action
        )
        
        return {
            "interaction_id": interaction_id,
            "checkpoint_id": checkpoint_id,
            "workflow_id": checkpoint['workflow_id'],
            "action": decision.action,
            "status": "decision_recorded"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/hitl/document/version")
async def save_document_version(version: DocumentVersion):
    """
    Salva una nuova versione del documento con tracking completo
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Calcola hash del contenuto
        content_hash = calculate_content_hash(version.content)
        
        # Conta versioni esistenti per determinare numero versione
        cur.execute("""
            SELECT COUNT(*) as count FROM document_versions
            WHERE workflow_id = %s
        """, (version.workflow_id,))
        
        count = cur.fetchone()['count']
        version_number = f"{count + 1}.0-{'AI' if version.is_ai_generated else 'HUMAN'}"
        
        # Calcola statistiche
        word_count = len(version.content.split())
        section_count = version.content.count('\n\n') + 1  # Stima semplice
        
        # Recupera versione precedente per diff
        cur.execute("""
            SELECT content FROM document_versions
            WHERE workflow_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (version.workflow_id,))
        
        previous = cur.fetchone()
        diff_from_previous = None
        
        if previous:
            # Calcola diff semplificato (in produzione usare libreria diff)
            diff_from_previous = {
                'previous_length': len(previous['content']),
                'current_length': len(version.content),
                'change_percentage': abs(len(version.content) - len(previous['content'])) / len(previous['content']) * 100
            }
        
        # Inserisci nuova versione
        cur.execute("""
            INSERT INTO document_versions
            (workflow_id, version, content, content_hash, created_by,
             is_ai_generated, hitl_interaction_id, word_count, section_count,
             diff_from_previous)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            version.workflow_id,
            version_number,
            version.content,
            content_hash,
            version.created_by,
            version.is_ai_generated,
            version.hitl_interaction_id,
            word_count,
            section_count,
            json.dumps(diff_from_previous) if diff_from_previous else None
        ))
        
        version_id = cur.fetchone()['id']
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "version_id": version_id,
            "version": version_number,
            "content_hash": content_hash,
            "word_count": word_count,
            "section_count": section_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/hitl/workflow/{workflow_id}/modifications")
async def get_modifications_history(workflow_id: str):
    """
    Recupera storico completo modifiche HITL per un workflow
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                hi.*,
                u.username as user_name
            FROM hitl_interactions hi
            LEFT JOIN users u ON hi.user_id = u.id
            WHERE hi.workflow_id = %s
            ORDER BY hi.timestamp ASC
        """, (workflow_id,))
        
        modifications = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return {
            "workflow_id": workflow_id,
            "total_modifications": len(modifications),
            "modifications": [
                {
                    "hitl_point": m['hitl_point'],
                    "user": m['user_name'],
                    "action": m['user_action'],
                    "timestamp": m['timestamp'].isoformat(),
                    "time_to_decision": str(m['time_to_decision']) if m['time_to_decision'] else None,
                    "changes": m['user_changes'],
                    "reason": m['modification_reason']
                }
                for m in modifications
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/hitl/workflow/{workflow_id}/versions")
async def get_document_versions(workflow_id: str):
    """
    Recupera storico versioni documento
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                id, version, content_hash, created_by, created_at,
                is_ai_generated, word_count, section_count,
                ai_content_percentage, human_content_percentage
            FROM document_versions
            WHERE workflow_id = %s
            ORDER BY created_at ASC
        """, (workflow_id,))
        
        versions = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return {
            "workflow_id": workflow_id,
            "current_version": versions[-1]['version'] if versions else None,
            "total_versions": len(versions),
            "versions": [
                {
                    "version": v['version'],
                    "created_at": v['created_at'].isoformat(),
                    "created_by": v['created_by'],
                    "is_ai_generated": v['is_ai_generated'],
                    "word_count": v['word_count'],
                    "ai_content": v['ai_content_percentage'],
                    "human_content": v['human_content_percentage']
                }
                for v in versions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def notify_workflow_engine(workflow_id: str, checkpoint_name: str, action: str):
    """
    Notifica il workflow engine che l'utente ha preso una decisione
    In produzione, questo pubblicherebbe su Kafka
    """
    # TODO: Implementare pubblicazione Kafka
    print(f"[KAFKA] Publishing: workflow.hitl.decision.{action}")
    print(f"  workflow_id: {workflow_id}")
    print(f"  checkpoint: {checkpoint_name}")
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5009)
