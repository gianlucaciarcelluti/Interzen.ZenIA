"""
SP03 - Procedural Classifier Service
Classificazione iniziale del procedimento amministrativo da istanza di parte
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import os
from datetime import datetime

app = FastAPI(
    title="SP03 - Procedural Classifier",
    description="Servizio di classificazione procedimenti amministrativi",
    version="1.0.0"
)


class Richiedente(BaseModel):
    tipo: str  # PERSONA_FISICA, PERSONA_GIURIDICA
    denominazione: Optional[str] = None
    partita_iva: Optional[str] = None
    codice_fiscale: Optional[str] = None
    sede_legale: Optional[str] = None


class IstanzaMetadata(BaseModel):
    oggetto: str
    richiedente: Richiedente
    riferimenti_normativi_citati: Optional[List[str]] = []
    descrizione_istanza: str
    data_presentazione: str
    urgenza: str = "NORMALE"


class AllegatiInfo(BaseModel):
    count: int
    types: List[str]
    total_size_mb: float


class ProcedureClassificationRequest(BaseModel):
    workflow_id: str
    istanza_metadata: IstanzaMetadata
    allegati_info: AllegatiInfo
    context: Optional[Dict[str, Any]] = {}


class ProcedimentoInfo(BaseModel):
    codice: str
    denominazione: str
    categoria: str
    sottocategoria: Optional[str]
    confidence: float


class TipoProvvedimentoInfo(BaseModel):
    codice: str
    denominazione: str
    autorita_competente: str
    confidence: float


class TerminiProcedimento(BaseModel):
    giorni_max: int
    silenzio_assenso: bool
    possibilita_proroga: bool
    termini_urgenti: Optional[int]


class ResponsabileProcedimento(BaseModel):
    ruolo_richiesto: str
    competenze_necessarie: List[str]


class ProcedimentoDetails(BaseModel):
    normativa_base: List[Dict[str, str]]
    termini_procedimento: TerminiProcedimento
    responsabile_procedimento: ResponsabileProcedimento
    fasi_procedurali: List[str]


class MetadataRequired(BaseModel):
    obbligatori: List[str]
    opzionali: List[str]
    missing: List[str]


class EnteCoinvolto(BaseModel):
    ente: str
    tipo_coinvolgimento: str
    termini_risposta: int


class ClassificationResult(BaseModel):
    procedimento: ProcedimentoInfo
    tipo_provvedimento: TipoProvvedimentoInfo
    procedimento_details: ProcedimentoDetails
    metadata_required: MetadataRequired
    enti_coinvolti: List[EnteCoinvolto]


class MetadataExtracted(BaseModel):
    entita_richiedente: Richiedente
    oggetto_istanza: str
    riferimenti_normativi_rilevati: List[Dict[str, str]]
    keywords_chiave: List[str]
    settore_economico: Optional[str]


class SimilarityScore(BaseModel):
    procedimento_id: str
    similarity: float
    tipo: str
    esito: str
    data: str


class TemplateSuggerito(BaseModel):
    template_id: str
    nome: str
    versione: str
    ultima_modifica: str


class ProcedureClassificationResponse(BaseModel):
    classification: ClassificationResult
    metadata_extracted: MetadataExtracted
    similarity_scores: List[SimilarityScore]
    template_suggerito: TemplateSuggerito
    processing_time_ms: int
    cached: bool


@app.get("/")
async def root():
    return {
        "service": "SP03 - Procedural Classifier",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": [
            "/classify-procedure",
            "/health"
        ]
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/classify-procedure", response_model=ProcedureClassificationResponse)
async def classify_procedure(request: ProcedureClassificationRequest):
    """
    Classifica il procedimento amministrativo a partire dall'istanza di parte.
    
    Il servizio:
    1. Analizza semanticamente l'istanza
    2. Estrae entità rilevanti (NER)
    3. Recupera procedimenti simili dalla KB
    4. Determina il tipo di provvedimento da generare
    5. Restituisce normativa applicabile e metadata richiesti
    """
    
    start_time = datetime.now()
    
    try:
        # Simulazione classificazione (da sostituire con modello reale)
        # In produzione: DistilBERT + NER + KB Integration
        
        # Esempio: Autorizzazione scarico acque
        if "scarico" in request.istanza_metadata.oggetto.lower() and "acque" in request.istanza_metadata.oggetto.lower():
            result = ProcedureClassificationResponse(
                classification=ClassificationResult(
                    procedimento=ProcedimentoInfo(
                        codice="PROC_AMB_001",
                        denominazione="AUTORIZZAZIONE_SCARICO_ACQUE_REFLUE",
                        categoria="AMBIENTE",
                        sottocategoria="TUTELA_ACQUE",
                        confidence=0.96
                    ),
                    tipo_provvedimento=TipoProvvedimentoInfo(
                        codice="PROV_DET_DIR",
                        denominazione="DETERMINAZIONE_DIRIGENZIALE",
                        autorita_competente="DIRIGENTE_SETTORE_AMBIENTE",
                        confidence=0.94
                    ),
                    procedimento_details=ProcedimentoDetails(
                        normativa_base=[
                            {
                                "tipo": "DECRETO_LEGISLATIVO",
                                "numero": "152/2006",
                                "articolo": "124",
                                "descrizione": "Disciplina degli scarichi"
                            },
                            {
                                "tipo": "LEGGE_REGIONALE",
                                "numero": "62/1998",
                                "articolo": "8",
                                "descrizione": "Norme regionali tutela acque"
                            }
                        ],
                        termini_procedimento=TerminiProcedimento(
                            giorni_max=90,
                            silenzio_assenso=False,
                            possibilita_proroga=True,
                            termini_urgenti=None
                        ),
                        responsabile_procedimento=ResponsabileProcedimento(
                            ruolo_richiesto="FUNZIONARIO_SETTORE_AMBIENTE",
                            competenze_necessarie=["TUTELA_ACQUE", "DIRITTO_AMBIENTALE"]
                        ),
                        fasi_procedurali=[
                            "VERIFICA_COMPLETEZZA_ISTANZA",
                            "ISTRUTTORIA_TECNICA",
                            "PARERI_ENTI_ESTERNI",
                            "CONFERENZA_SERVIZI",
                            "DETERMINAZIONE_FINALE"
                        ]
                    ),
                    metadata_required=MetadataRequired(
                        obbligatori=[
                            "dati_identificativi_richiedente",
                            "localizzazione_scarico",
                            "caratteristiche_scarico",
                            "relazione_tecnica",
                            "planimetria",
                            "certificato_iscrizione_cciaa"
                        ],
                        opzionali=[
                            "studio_impatto_ambientale",
                            "documentazione_fotografica"
                        ],
                        missing=[]
                    ),
                    enti_coinvolti=[
                        EnteCoinvolto(
                            ente="ARPA",
                            tipo_coinvolgimento="PARERE_OBBLIGATORIO",
                            termini_risposta=30
                        ),
                        EnteCoinvolto(
                            ente="ASL",
                            tipo_coinvolgimento="PARERE_FACOLTATIVO",
                            termini_risposta=15
                        )
                    ]
                ),
                metadata_extracted=MetadataExtracted(
                    entita_richiedente=request.istanza_metadata.richiedente,
                    oggetto_istanza=request.istanza_metadata.oggetto,
                    riferimenti_normativi_rilevati=[
                        {"tipo": "DECRETO_LEGISLATIVO", "numero": "152/2006"}
                    ],
                    keywords_chiave=["scarico", "acque reflue", "industriali", "autorizzazione"],
                    settore_economico="INDUSTRIA_TESSILE"
                ),
                similarity_scores=[
                    SimilarityScore(
                        procedimento_id="PROC-2024-00567",
                        similarity=0.91,
                        tipo="AUTORIZZAZIONE_SCARICO_ACQUE",
                        esito="ACCOGLIMENTO",
                        data="2024-08-15"
                    ),
                    SimilarityScore(
                        procedimento_id="PROC-2024-00234",
                        similarity=0.87,
                        tipo="AUTORIZZAZIONE_SCARICO_ACQUE",
                        esito="DINIEGO",
                        data="2024-03-22"
                    )
                ],
                template_suggerito=TemplateSuggerito(
                    template_id="TPL_DET_AMB_001",
                    nome="Determinazione Dirigenziale - Autorizzazione Scarico Acque",
                    versione="2.1",
                    ultima_modifica="2025-06-15"
                ),
                processing_time_ms=int((datetime.now() - start_time).total_seconds() * 1000),
                cached=False
            )
        else:
            # Fallback generico
            result = ProcedureClassificationResponse(
                classification=ClassificationResult(
                    procedimento=ProcedimentoInfo(
                        codice="PROC_GEN_001",
                        denominazione="PROCEDIMENTO_GENERICO",
                        categoria="GENERALE",
                        sottocategoria=None,
                        confidence=0.65
                    ),
                    tipo_provvedimento=TipoProvvedimentoInfo(
                        codice="PROV_DET_GEN",
                        denominazione="DETERMINAZIONE_GENERICA",
                        autorita_competente="DIRIGENTE_SETTORE_COMPETENTE",
                        confidence=0.60
                    ),
                    procedimento_details=ProcedimentoDetails(
                        normativa_base=[
                            {
                                "tipo": "LEGGE",
                                "numero": "241/1990",
                                "articolo": "2",
                                "descrizione": "Norme generali procedimento amministrativo"
                            }
                        ],
                        termini_procedimento=TerminiProcedimento(
                            giorni_max=30,
                            silenzio_assenso=False,
                            possibilita_proroga=True,
                            termini_urgenti=None
                        ),
                        responsabile_procedimento=ResponsabileProcedimento(
                            ruolo_richiesto="FUNZIONARIO_COMPETENTE",
                            competenze_necessarie=[]
                        ),
                        fasi_procedurali=[
                            "VERIFICA_COMPLETEZZA_ISTANZA",
                            "ISTRUTTORIA",
                            "DETERMINAZIONE_FINALE"
                        ]
                    ),
                    metadata_required=MetadataRequired(
                        obbligatori=["dati_identificativi_richiedente"],
                        opzionali=[],
                        missing=[]
                    ),
                    enti_coinvolti=[]
                ),
                metadata_extracted=MetadataExtracted(
                    entita_richiedente=request.istanza_metadata.richiedente,
                    oggetto_istanza=request.istanza_metadata.oggetto,
                    riferimenti_normativi_rilevati=[],
                    keywords_chiave=[],
                    settore_economico=None
                ),
                similarity_scores=[],
                template_suggerito=TemplateSuggerito(
                    template_id="TPL_DET_GEN_001",
                    nome="Determinazione Generica",
                    versione="1.0",
                    ultima_modifica="2025-01-01"
                ),
                processing_time_ms=int((datetime.now() - start_time).total_seconds() * 1000),
                cached=False
            )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nella classificazione: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "5003"))
    uvicorn.run(app, host="0.0.0.0", port=port)
