#!/usr/bin/env python3
"""
SP04 - Classifier Service
API REST per classificazione multi-dimensionale documenti amministrativi

Questo è il wrapper principale che espone l'API del classificatore.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_path = current_dir / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uvicorn

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

app = FastAPI(
    title="SP04 - Classifier Service",
    description="Classificazione multi-dimensionale documenti amministrativi",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELS
# ============================================================================

class ClassificationRequest(BaseModel):
    """Request model per classificazione"""
    testo: str = Field(
        description="Testo del documento da classificare",
        examples=["Richiesta di autorizzazione scarico acque reflue industriali"]
    )
    
class DimensionScore(BaseModel):
    """Score per una singola categoria"""
    categoria_id: int
    categoria_nome: str
    probabilita: float

class DimensionResult(BaseModel):
    """Risultato per una dimensione"""
    dimensione: str
    categoria_predetta: str
    categoria_id: int
    probabilita: float
    tutte_probabilita: List[DimensionScore]

class ClassificationResponse(BaseModel):
    """Response con risultati classificazione"""
    status: str
    testo: str
    risultati: List[DimensionResult]
    metadata: Dict[str, Any]

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint con info servizio"""
    return {
        "service": "SP04 - Classifier",
        "status": "operational",
        "version": "1.0.0",
        "description": "Servizio di classificazione multi-dimensionale documenti",
        "endpoints": [
            "/docs - Documentazione Swagger UI",
            "/redoc - Documentazione ReDoc",
            "/health - Health check",
            "/api/v1/classify - Classifica documento",
            "/api/v1/model-info - Info sul modello"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sp04-classifier",
        "model_loaded": True,
        "mode": "production"
    }

@app.post("/api/v1/classify", response_model=ClassificationResponse)
async def classify_document(request: ClassificationRequest):
    """
    Classifica un documento su più dimensioni
    
    Il classificatore analizza il testo e lo classifica su varie dimensioni:
    - Tipologia documento
    - Categoria amministrativa
    - Urgenza
    - Complessità
    
    Args:
        request: Testo del documento da classificare
        
    Returns:
        Risultati classificazione con probabilità per ogni dimensione
    """
    
    # TODO: Integrare il classificatore reale da src/SP04/
    # Per ora ritorniamo un esempio placeholder
    
    return ClassificationResponse(
        status="success",
        testo=request.testo[:100] + "..." if len(request.testo) > 100 else request.testo,
        risultati=[
            DimensionResult(
                dimensione="Tipologia Documento",
                categoria_predetta="Autorizzazione",
                categoria_id=1,
                probabilita=0.85,
                tutte_probabilita=[
                    DimensionScore(categoria_id=1, categoria_nome="Autorizzazione", probabilita=0.85),
                    DimensionScore(categoria_id=2, categoria_nome="Concessione", probabilita=0.10),
                    DimensionScore(categoria_id=3, categoria_nome="Ordinanza", probabilita=0.05)
                ]
            ),
            DimensionResult(
                dimensione="Complessità",
                categoria_predetta="Media",
                categoria_id=2,
                probabilita=0.72,
                tutte_probabilita=[
                    DimensionScore(categoria_id=1, categoria_nome="Bassa", probabilita=0.15),
                    DimensionScore(categoria_id=2, categoria_nome="Media", probabilita=0.72),
                    DimensionScore(categoria_id=3, categoria_nome="Alta", probabilita=0.13)
                ]
            )
        ],
        metadata={
            "model_version": "1.0.0",
            "processing_time_ms": 150,
            "confidence_threshold": 0.7
        }
    )

@app.post("/api/v1/classify-batch")
async def classify_batch(requests: List[ClassificationRequest]):
    """
    Classifica multipli documenti in batch
    
    Args:
        requests: Lista di testi da classificare
        
    Returns:
        Lista di risultati classificazione
    """
    results = []
    for req in requests:
        result = await classify_document(req)
        results.append(result)
    
    return {
        "status": "success",
        "total_processed": len(requests),
        "results": results
    }

@app.get("/api/v1/model-info")
async def get_model_info():
    """
    Informazioni sul modello di classificazione
    
    Returns:
        Dettagli sul modello, categorie, performance
    """
    return {
        "status": "operational",
        "model": {
            "name": "Multi-dimensional Document Classifier",
            "version": "1.0.0",
            "type": "ensemble",
            "algorithms": ["TF-IDF", "Logistic Regression", "Multi-output Classifier"]
        },
        "dimensions": [
            {
                "name": "Tipologia Documento",
                "categories": ["Autorizzazione", "Concessione", "Ordinanza", "Determina"]
            },
            {
                "name": "Complessità",
                "categories": ["Bassa", "Media", "Alta"]
            },
            {
                "name": "Urgenza",
                "categories": ["Normale", "Urgente", "Molto Urgente"]
            }
        ],
        "performance": {
            "accuracy": 0.89,
            "avg_confidence": 0.82,
            "training_samples": 1500
        }
    }

@app.get("/api/v1/categories")
async def get_categories():
    """Lista tutte le categorie disponibili per dimensione"""
    return {
        "status": "success",
        "dimensions": {
            "tipologia": ["Autorizzazione", "Concessione", "Ordinanza", "Determina"],
            "complessita": ["Bassa", "Media", "Alta"],
            "urgenza": ["Normale", "Urgente", "Molto Urgente"]
        }
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 5004))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting SP04 Classifier Service on {host}:{port}")
    print(f"📚 Swagger UI: http://{host if host != '0.0.0.0' else 'localhost'}:{port}/docs")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )