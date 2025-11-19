"""
Test per API Classificatore Multi-Dimensionale
"""

import sys
import os

# Aggiungi il path per import moduli
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'classifier'))

import pytest
from fastapi.testclient import TestClient

# Importa l'app dopo aver configurato il path
from api_multidimensional_classifier import app

client = TestClient(app)


def test_root_endpoint():
    """Test endpoint root"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "servizio" in data
    assert data["stato"] == "operativo"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "modello_caricato" in data


def test_model_info():
    """Test endpoint informazioni modello"""
    response = client.get("/api/v1/model/info")
    assert response.status_code == 200
    data = response.json()
    assert data["algoritmo"] == "Logistic Regression"
    assert data["architettura"] == "Multi-Output Classifier"
    assert "categorie" in data


def test_classify_sinistro_avvenuto_iniziale():
    """Test classificazione: Sinistro Avvenuto - Fatto Iniziale"""
    payload = {
        "testo": "Mio padre è morto il 5 maggio 2023 a causa di una trasfusione con gruppo sanguigno errato. Voglio avviare causa per risarcimento danni."
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["successo"] is True
    assert "tipologia" in data
    assert "riferimento_temporale" in data
    assert "confidenza_media" in data
    
    # Verifica che non ci siano errori
    assert data.get("errore") is None
    
    # Verifica struttura tipologia
    assert data["tipologia"] is not None
    assert "predizione_id" in data["tipologia"]
    assert "predizione_nome" in data["tipologia"]
    assert "confidenza" in data["tipologia"]
    assert "scores" in data["tipologia"]
    assert len(data["tipologia"]["scores"]) == 2
    
    # Verifica struttura riferimento temporale
    assert data["riferimento_temporale"] is not None
    assert "predizione_id" in data["riferimento_temporale"]
    assert "scores" in data["riferimento_temporale"]
    assert len(data["riferimento_temporale"]["scores"]) == 2


def test_classify_circostanza_followup():
    """Test classificazione: Circostanza Potenziale - Follow-up"""
    payload = {
        "testo": "Con riferimento alla segnalazione 98765: aggiorno che la situazione persiste. Gli infermieri continuano a non rispettare le procedure."
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["successo"] is True
    assert 0.0 <= data["confidenza_media"] <= 1.0
    assert 0.0 <= data["confidenza_media_percentuale"] <= 100.0


def test_classify_empty_text():
    """Test classificazione con testo vuoto"""
    payload = {"testo": ""}
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 422  # Pydantic validation error


def test_classify_short_text():
    """Test classificazione con testo troppo corto"""
    payload = {"testo": "Ciao"}
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 422  # Validation error


def test_classify_batch():
    """Test classificazione batch"""
    payload = [
        {"testo": "Mio padre è morto a causa di una trasfusione errata durante un intervento chirurgico. Voglio richiedere risarcimento."},
        {"testo": "Rif. pratica 123: invio documentazione aggiornata come richiesto dal vostro ufficio legale."}
    ]
    response = client.post("/api/v1/classify/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 2
    
    for result in data:
        assert "successo" in result
        assert "tipologia" in result
        assert "riferimento_temporale" in result
        # Verifica che le classificazioni siano riuscite
        if result["successo"]:
            assert result["tipologia"] is not None
            assert result["riferimento_temporale"] is not None


def test_classify_batch_with_error():
    """Test batch con una email vuota - Pydantic valida tutto prima quindi restituisce 422"""
    payload = [
        {"testo": "Mio padre è morto a causa di una trasfusione errata. Voglio risarcimento danni."},
        {"testo": ""},  # Email vuota
        {"testo": "Rif. pratica 123: invio documentazione."}
    ]
    response = client.post("/api/v1/classify/batch", json=payload)
    # Pydantic valida tutti gli elementi prima di passarli alla funzione
    # quindi se uno fallisce, restituisce 422
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # Contiene i dettagli dell'errore di validazione


def test_classify_batch_too_many():
    """Test batch con troppe email"""
    payload = [{"testo": f"Test email numero {i} per verificare il limite massimo"} for i in range(51)]
    response = client.post("/api/v1/classify/batch", json=payload)
    assert response.status_code == 400


def test_scores_sum_to_one():
    """Test che le probabilità sommino a 1 per ciascuna dimensione"""
    payload = {
        "testo": "Test email per verificare le probabilità delle classificazioni multiple dimensionali."
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Somma probabilità tipologia
    sum_tip = sum(score["probabilita"] for score in data["tipologia"]["scores"])
    assert abs(sum_tip - 1.0) < 0.01  # Tolleranza per arrotondamenti
    
    # Somma probabilità riferimento temporale
    sum_rif = sum(score["probabilita"] for score in data["riferimento_temporale"]["scores"])
    assert abs(sum_rif - 1.0) < 0.01


def test_response_structure():
    """Test struttura completa della response"""
    payload = {
        "testo": "Segnalo un grave episodio avvenuto ieri in ospedale durante la somministrazione farmaci."
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Campi principali
    assert "successo" in data
    assert "tipologia" in data
    assert "riferimento_temporale" in data
    assert "confidenza_media" in data
    assert "confidenza_media_percentuale" in data
    assert "raccomandazione" in data
    assert "statistiche_testo" in data
    
    # Statistiche testo
    stats = data["statistiche_testo"]
    assert "lunghezza_caratteri" in stats
    assert "numero_parole" in stats
    assert "numero_righe" in stats
    assert stats["lunghezza_caratteri"] > 0
    assert stats["numero_parole"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
