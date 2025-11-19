"""
API REST per Classificazione Multi-Dimensionale di Email
Espone endpoint per classificazione sinistri medical malpractice
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Import del dataset mock
from mock_email_multidimensional_dataset import (
    create_mock_dataset,
    get_category_names
)


# ============================================================================
# MODELLI PYDANTIC
# ============================================================================

class ClassificationRequest(BaseModel):
    """Request model per classificazione"""
    testo: str = Field(
        description="Testo dell'email da classificare",
        examples=["Mio padre è morto a causa di una trasfusione errata. Voglio risarcimento."]
    )
    
    @validator('testo')
    def validate_testo(cls, v):
        """Valida che il testo non sia vuoto e abbia lunghezza minima"""
        if not v or not v.strip():
            raise ValueError("Il testo non può essere vuoto")
        if len(v.strip()) < 10:
            raise ValueError("Il testo deve contenere almeno 10 caratteri")
        return v


class DimensionScore(BaseModel):
    """Score per una singola categoria"""
    categoria_id: int = Field(description="ID numerico della categoria")
    categoria_nome: str = Field(description="Nome descrittivo della categoria")
    probabilita: float = Field(ge=0.0, le=1.0, description="Probabilità (0-1)")
    percentuale: float = Field(ge=0.0, le=100.0, description="Percentuale (0-100)")


class DimensionClassification(BaseModel):
    """Classificazione per una dimensione"""
    predizione_id: int = Field(description="ID della categoria predetta")
    predizione_nome: str = Field(description="Nome della categoria predetta")
    confidenza: float = Field(ge=0.0, le=1.0, description="Confidenza della predizione")
    confidenza_percentuale: float = Field(ge=0.0, le=100.0, description="Confidenza in percentuale")
    scores: List[DimensionScore] = Field(description="Score di tutte le categorie")


class ClassificationResponse(BaseModel):
    """Response model per classificazione"""
    successo: bool = Field(description="Indica se la classificazione è avvenuta con successo")
    tipologia: Optional[DimensionClassification] = Field(default=None, description="Classificazione dimensione Tipologia")
    riferimento_temporale: Optional[DimensionClassification] = Field(default=None, description="Classificazione dimensione Riferimento Temporale")
    confidenza_media: float = Field(ge=0.0, le=1.0, description="Confidenza media tra le due dimensioni")
    confidenza_media_percentuale: float = Field(ge=0.0, le=100.0, description="Confidenza media in percentuale")
    raccomandazione: str = Field(description="Raccomandazione basata sulla confidenza")
    statistiche_testo: Dict[str, int] = Field(default_factory=dict, description="Statistiche del testo analizzato")
    errore: Optional[str] = Field(default=None, description="Messaggio di errore se presente")


class ModelInfo(BaseModel):
    """Informazioni sul modello"""
    algoritmo: str
    architettura: str
    dataset_size: int
    features: int
    ngram_range: str
    categorie: Dict[str, Dict[int, str]]


class HealthResponse(BaseModel):
    """Response per health check"""
    status: str
    modello_caricato: bool
    versione: str


# ============================================================================
# INIZIALIZZAZIONE APPLICAZIONE
# ============================================================================

app = FastAPI(
    title="API Classificatore Multi-Dimensionale Email Sinistri",
    description="API REST per classificazione automatica di email relative a sinistri medical malpractice su due dimensioni: Tipologia e Riferimento Temporale",
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

# Variabili globali per modello e vectorizer (caricati al primo utilizzo)
_model = None
_vectorizer = None
_category_names = None
_dataset_size = None


# ============================================================================
# FUNZIONI HELPER
# ============================================================================

def load_model():
    """
    Carica e allena il modello multi-output.
    Viene eseguito una sola volta al primo utilizzo.
    """
    global _model, _vectorizer, _category_names, _dataset_size
    
    if _model is not None:
        return _model, _vectorizer, _category_names, _dataset_size
    
    # Carica dataset
    df = create_mock_dataset()
    
    # Prepara features e target
    X = df['testo']
    y_multi = df[['tipologia', 'riferimento_temporale']].values
    
    # Crea label combinata per stratificazione
    df['combined_label'] = df['tipologia'].astype(str) + '_' + df['riferimento_temporale'].astype(str)
    
    # Split train/test
    X_train, _, y_train, _ = train_test_split(
        X, y_multi,
        test_size=0.2,
        random_state=42,
        stratify=df['combined_label']
    )
    
    # Vettorizzazione TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.8,
        strip_accents='unicode',
        lowercase=True
    )
    
    x_train_tfidf = vectorizer.fit_transform(X_train)
    
    # Training modello multi-output
    lr_base = LogisticRegression(
        max_iter=1000,
        C=1.0,
        random_state=42,
        solver='lbfgs'
    )
    model = MultiOutputClassifier(lr_base)
    model.fit(x_train_tfidf, y_train)
    
    # Ottieni nomi categorie
    category_names = get_category_names()
    
    # Salva nelle variabili globali
    _model = model
    _vectorizer = vectorizer
    _category_names = category_names
    _dataset_size = len(df)
    
    return _model, _vectorizer, _category_names, _dataset_size


def get_raccomandazione(confidenza_media: float) -> str:
    """Genera raccomandazione basata sulla confidenza media"""
    if confidenza_media >= 0.9:
        return "Alta confidenza - Classificazione automatica affidabile"
    elif confidenza_media >= 0.7:
        return "Media confidenza - Classificazione valida, monitoraggio consigliato"
    else:
        return "Bassa confidenza - Revisione manuale fortemente raccomandata"


def classify_text(text: str) -> ClassificationResponse:
    """
    Classifica un testo su entrambe le dimensioni.
    
    Args:
        text: Testo da classificare
        
    Returns:
        ClassificationResponse con tutti gli score
    """
    # Carica modello
    model, vectorizer, category_names, _ = load_model()
    
    # Type guards per type checker
    if model is None or vectorizer is None or category_names is None:
        raise RuntimeError("Modello non caricato correttamente")
    
    # Vettorizza il testo
    text_vector = vectorizer.transform([text])
    
    # Predizione
    prediction = model.predict(text_vector)  # type: ignore
    pred_tip = int(prediction[0][0])  # type: ignore
    pred_rif = int(prediction[0][1])  # type: ignore
    
    # Probabilità per entrambe le dimensioni
    # Type ignore per limitazioni inference sklearn
    prob_tip = model.estimators_[0].predict_proba(text_vector)[0]  # type: ignore
    prob_rif = model.estimators_[1].predict_proba(text_vector)[0]  # type: ignore
    
    # Costruisci scores per Tipologia
    scores_tipologia = [
        DimensionScore(
            categoria_id=cat_id,
            categoria_nome=cat_name,
            probabilita=float(prob_tip[cat_id]),
            percentuale=float(prob_tip[cat_id] * 100)
        )
        for cat_id, cat_name in category_names['tipologia'].items()
    ]
    
    # Costruisci scores per Riferimento Temporale
    scores_riferimento = [
        DimensionScore(
            categoria_id=cat_id,
            categoria_nome=cat_name,
            probabilita=float(prob_rif[cat_id]),
            percentuale=float(prob_rif[cat_id] * 100)
        )
        for cat_id, cat_name in category_names['riferimento_temporale'].items()
    ]
    
    # Confidenze
    confidenza_tip = float(prob_tip[pred_tip])
    confidenza_rif = float(prob_rif[pred_rif])
    confidenza_media = (confidenza_tip + confidenza_rif) / 2
    
    # Statistiche testo
    statistiche = {
        "lunghezza_caratteri": len(text),
        "numero_parole": len(text.split()),
        "numero_righe": len(text.split('\n'))
    }
    
    # Costruisci response
    response = ClassificationResponse(
        successo=True,
        tipologia=DimensionClassification(
            predizione_id=int(pred_tip),
            predizione_nome=category_names['tipologia'][pred_tip],
            confidenza=confidenza_tip,
            confidenza_percentuale=confidenza_tip * 100,
            scores=scores_tipologia
        ),
        riferimento_temporale=DimensionClassification(
            predizione_id=int(pred_rif),
            predizione_nome=category_names['riferimento_temporale'][pred_rif],
            confidenza=confidenza_rif,
            confidenza_percentuale=confidenza_rif * 100,
            scores=scores_riferimento
        ),
        confidenza_media=confidenza_media,
        confidenza_media_percentuale=confidenza_media * 100,
        raccomandazione=get_raccomandazione(confidenza_media),
        statistiche_testo=statistiche
    )
    
    return response


# ============================================================================
# ENDPOINTS API
# ============================================================================

@app.get("/", tags=["General"])
async def root():
    """Root endpoint con informazioni base"""
    return {
        "servizio": "API Classificatore Multi-Dimensionale Email Sinistri",
        "versione": "1.0.0",
        "stato": "operativo",
        "documentazione": "/docs",
        "endpoints": {
            "classificazione": "POST /api/v1/classify",
            "health": "GET /api/v1/health",
            "info": "GET /api/v1/model/info"
        }
    }


@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint per verificare lo stato del servizio.
    """
    modello_caricato = _model is not None
    
    return HealthResponse(
        status="healthy" if modello_caricato else "initializing",
        modello_caricato=modello_caricato,
        versione="1.0.0"
    )


@app.get("/api/v1/model/info", response_model=ModelInfo, tags=["Model"])
async def get_model_info():
    """
    Restituisce informazioni dettagliate sul modello.
    """
    # Assicura che il modello sia caricato
    _, vectorizer, category_names, dataset_size = load_model()
    
    # Type guards
    if vectorizer is None or category_names is None or dataset_size is None:
        raise RuntimeError("Modello non caricato correttamente")
    
    return ModelInfo(
        algoritmo="Logistic Regression",
        architettura="Multi-Output Classifier",
        dataset_size=dataset_size,
        features=len(vectorizer.get_feature_names_out()),
        ngram_range="(1, 2)",
        categorie=category_names
    )


@app.post("/api/v1/classify", response_model=ClassificationResponse, tags=["Classification"])
async def classify_email(request: ClassificationRequest):
    """
    Classifica un'email su due dimensioni indipendenti:
    
    - **Dimensione 1 - Tipologia**: Sinistro Avvenuto vs Circostanza Potenziale
    - **Dimensione 2 - Riferimento Temporale**: Fatto Iniziale vs Follow-up
    
    Restituisce gli score di probabilità per tutte le categorie su entrambe le dimensioni.
    """
    try:
        # Validazione input
        if not request.testo or not request.testo.strip():
            raise HTTPException(
                status_code=400,
                detail="Il campo 'testo' non può essere vuoto"
            )
        
        # Classificazione
        result = classify_text(request.testo)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore durante la classificazione: {str(e)}"
        )


@app.post("/api/v1/classify/batch", response_model=List[ClassificationResponse], tags=["Classification"])
async def classify_batch(requests: List[ClassificationRequest]):
    """
    Classifica multiple email in batch.
    
    Utile per processare più email contemporaneamente.
    Massimo 50 email per richiesta.
    
    NOTA: Se una email non passa la validazione Pydantic, l'intera richiesta fallirà.
    Per gestire errori individuali, inviare richieste separate.
    """
    if len(requests) > 50:
        raise HTTPException(
            status_code=400,
            detail="Massimo 50 email per richiesta batch"
        )
    
    results = []
    for idx, req in enumerate(requests):
        try:
            result = classify_text(req.testo)
            results.append(result)
        except Exception as e:
            # In caso di errore su una email, continua con le altre
            results.append(ClassificationResponse(
                successo=False,
                tipologia=None,
                riferimento_temporale=None,
                confidenza_media=0.0,
                confidenza_media_percentuale=0.0,
                raccomandazione=f"Errore: {str(e)}",
                statistiche_testo={},
                errore=f"Email {idx + 1}: {str(e)}"
            ))
    
    return results


# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Carica il modello all'avvio dell'applicazione"""
    print("🚀 Avvio API Classificatore Multi-Dimensionale...")
    print("📊 Caricamento modello in corso...")
    load_model()
    print("✅ Modello caricato con successo!")
    print("🌐 API pronta per ricevere richieste")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api_multidimensional_classifier:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
