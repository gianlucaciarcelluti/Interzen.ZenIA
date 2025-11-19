from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ProcedimentoType(str, Enum):
    AUTORIZZAZIONE = "autorizzazione"
    CONCESSIONE = "concessione"
    LICENZA = "licenza"
    NULLA_OSTA = "nulla_osta"
    PERMESSO = "permesso"


class DocumentType(str, Enum):
    ISTANZA = "istanza"
    ALLEGATO_TECNICO = "allegato_tecnico"
    DOCUMENTO_IDENTITA = "documento_identita"
    CERTIFICAZIONE = "certificazione"
    COMUNICAZIONE = "comunicazione"


class ValidationLevel(str, Enum):
    BASIC = "basic"
    FULL = "full"
    EXPERT = "expert"


class GenerationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    GENERATED = "generated"
    PARTIAL = "partial"
    ERROR = "error"


class AnagraficaRichiedente(BaseModel):
    """Dati anagrafici del richiedente"""
    nome: str
    cognome: str
    codice_fiscale: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    indirizzo: Optional[str] = None
    citta: Optional[str] = None
    cap: Optional[str] = None
    provincia: Optional[str] = None


class DocumentReference(BaseModel):
    """Riferimento a un documento nel fascicolo"""
    id: str
    nome: str
    tipo: DocumentType
    percorso: str
    dimensione: int
    data_caricamento: datetime
    contenuto_estratto: Optional[str] = None


class FascicoloData(BaseModel):
    """Dati completi del fascicolo procedimentale"""
    id: str
    numero_protocollo: Optional[str] = None
    data_apertura: datetime
    procedimento_type: ProcedimentoType
    richiedente: AnagraficaRichiedente
    documenti: List[DocumentReference]
    note: Optional[str] = None
    urgente: bool = False


class ValidationResult(BaseModel):
    """Risultato di validazione"""
    section: str
    issue: Optional[str] = None
    severity: str = Field(..., pattern="^(error|warning|info)$")
    suggestion: Optional[str] = None
    passed: bool


class DeterminaContent(BaseModel):
    """Contenuto strutturato della determina"""
    premesse: str
    motivazione: str
    dispositivo: str
    allegati: List[str]
    riferimenti_normativi: List[str]
    data_efficacia: Optional[str] = None


class GenerationMetadata(BaseModel):
    """Metadati del processo di generazione"""
    generated_at: datetime
    ai_model: str
    processing_time_seconds: float
    tokens_used: int
    version: str = "1.0"


class DeterminaGenerationRequest(BaseModel):
    """Richiesta di generazione determina"""
    fascicolo_id: str
    procedimento_config: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None


class DeterminaGenerationResponse(BaseModel):
    """Risposta con determina generata"""
    determina_id: str
    status: GenerationStatus
    content: Optional[DeterminaContent] = None
    validation_results: List[ValidationResult] = []
    metadata: Optional[GenerationMetadata] = None
    error_message: Optional[str] = None


class MCPToolRequest(BaseModel):
    """Richiesta per un tool MCP"""
    tool_name: str
    parameters: Dict[str, Any]


class MCPToolResponse(BaseModel):
    """Risposta da un tool MCP"""
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float
