"""
SP00 - Procedural Classifier con Groq API
Sistema di classificazione procedimenti amministrativi → provvedimenti
Ultra-veloce per analisi e studio strategie classificazione
"""

import os
from groq import Groq
import json
import pandas as pd
import time
from typing import Dict, List, Optional
from datetime import datetime
from tqdm import tqdm
import hashlib
import pickle
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()


class ProceduralClassifier:
    """
    Classificatore procedimenti amministrativi usando Groq API
    
    Features:
    - Classificazione istanza → procedimento + provvedimento
    - Estrazione metadata (normativa, termini, etc.)
    - Progress tracking e persistenza stato
    - Supporto batch processing
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile", 
                 cache_dir: str = ".cache"):
        """
        Inizializza classificatore procedimenti
        
        Args:
            api_key: Groq API key (o usa GROQ_API_KEY da env)
            model: Nome modello da usare
            cache_dir: Directory per cache e stato persistente
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "API key richiesta! Ottienila gratis su: https://console.groq.com\n"
                "Poi: export GROQ_API_KEY='your-key-here'"
            )
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
        self.cache_dir = cache_dir
        
        # Crea directory cache
        os.makedirs(cache_dir, exist_ok=True)
        
        # System prompt ottimizzato per classificazione procedimenti PA
        self.system_prompt = """Sei un esperto classificatore di procedimenti amministrativi della Pubblica Amministrazione italiana.

COMPITO: Classificare le istanze di parte (richieste cittadini/aziende) per identificare:
1. Il PROCEDIMENTO AMMINISTRATIVO corretto
2. Il TIPO DI PROVVEDIMENTO finale da emettere

PROCEDIMENTI SUPPORTATI (esempi principali):

AMBIENTE:
- AUTORIZZAZIONE_SCARICO_ACQUE → Determinazione Dirigenziale
- VIA_VALUTAZIONE_IMPATTO_AMBIENTALE → Delibera Giunta
- AUTORIZZAZIONE_EMISSIONI_ATMOSFERA → Determinazione Dirigenziale

URBANISTICA:
- PERMESSO_DI_COSTRUIRE → Determinazione Dirigenziale
- VARIANTE_URBANISTICA → Delibera Consiglio
- CERTIFICATO_DESTINAZIONE_URBANISTICA → Certificato

COMMERCIO:
- LICENZA_COMMERCIALE → Determinazione Dirigenziale
- SCIA_COMMERCIO → Ricevuta SCIA
- OCCUPAZIONE_SUOLO_PUBBLICO → Ordinanza

SOCIALE:
- ASSEGNAZIONE_ALLOGGIO_ERP → Determinazione Dirigenziale
- CONTRIBUTO_ASSISTENZIALE → Determinazione Dirigenziale

MOBILITÀ:
- AUTORIZZAZIONE_ZTL → Ordinanza
- PERMESSO_PARCHEGGIO_RESIDENTI → Autorizzazione

CULTURA:
- PATROCINIO_COMUNALE → Determinazione Dirigenziale

INDICATORI CHIAVE per classificazione:
- Oggetto/richiesta dell'istanza
- Settore/materia (ambiente, urbanistica, commercio, ecc.)
- Normativa citata (D.Lgs, L.R., ecc.)
- Tipo di richiedente (cittadino, azienda, ente)
- Caratteristiche tecniche (superfici, volumi, portate, ecc.)

Rispondi SOLO con JSON valido:
{
    "procedimento": "CODICE_PROCEDIMENTO",
    "procedimento_denominazione": "Nome leggibile del procedimento",
    "categoria": "CATEGORIA",
    "sottocategoria": "SOTTOCATEGORIA",
    "tipo_provvedimento": "TIPO_PROVVEDIMENTO",
    "autorita_competente": "AUTORITA_COMPETENTE",
    "normativa_base": ["normativa1", "normativa2"],
    "termini_giorni": numero_giorni_termine,
    "confidence": 0.0-1.0,
    "metadata_extracted": {
        "richiedente": "tipo richiedente",
        "oggetto_sintetico": "sintesi oggetto",
        "keywords_chiave": ["keyword1", "keyword2", "keyword3"]
    },
    "motivazione": "breve spiegazione della classificazione (max 100 parole)"
}

IMPORTANTE: 
- Rispondi SOLO con il JSON, nessun testo aggiuntivo
- Se non sei sicuro, usa confidence < 0.7
- Estrai metadata rilevanti dal testo dell'istanza
"""
    
    def _get_cache_key(self, texts: List[str], model: str) -> str:
        """Genera chiave univoca per cache"""
        content = f"{model}_{len(texts)}_" + "".join(texts[:3])
        return hashlib.md5(content.encode()).hexdigest()
    
    def _save_progress(self, cache_key: str, results: List[Dict], current_index: int):
        """Salva progresso corrente su disco"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        state = {
            "results": results,
            "current_index": current_index,
            "timestamp": datetime.now().isoformat(),
            "model": self.model
        }
        
        with open(cache_file, 'wb') as f:
            pickle.dump(state, f)
    
    def _load_progress(self, cache_key: str) -> Optional[Dict]:
        """Carica progresso salvato da disco"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    state = pickle.load(f)
                return state
            except Exception as e:
                print(f"⚠️ Errore caricamento cache: {e}")
                return None
        
        return None
    
    def _clear_cache(self, cache_key: str):
        """Rimuove cache completata"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        if os.path.exists(cache_file):
            os.remove(cache_file)
    
    def classify_single(self, istanza_text: str, temperature: float = 0.1) -> Dict:
        """
        Classifica una singola istanza
        
        Args:
            istanza_text: Testo dell'istanza di parte
            temperature: Temperatura del modello (più bassa = più deterministica)
        
        Returns:
            Dict con classificazione e metadati
        """
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Classifica questa istanza:\n\n{istanza_text}"}
                ],
                temperature=temperature,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            latency = time.time() - start_time
            
            # Parse risposta
            content = response.choices[0].message.content or "{}"
            result = json.loads(content)
            
            # Aggiungi metadati
            tokens_used = response.usage.total_tokens if response.usage else 0
            result.update({
                "success": True,
                "latency": latency,
                "model": self.model,
                "tokens_used": tokens_used,
                "tokens_per_second": tokens_used / latency if latency > 0 else 0
            })
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency": time.time() - start_time,
                "model": self.model
            }
    
    def classify_batch(self, 
                      istanze: List[str], 
                      true_labels: Optional[List[str]] = None,
                      resume: bool = True,
                      save_interval: int = 10) -> pd.DataFrame:
        """
        Classifica batch di istanze con progress tracking
        
        Args:
            istanze: Lista testi istanze
            true_labels: Se fornite, calcola accuracy [procedimento1, procedimento2, ...]
            resume: Se True, riprende da analisi precedente interrotta
            save_interval: Salva progresso ogni N istanze
            
        Returns:
            DataFrame con risultati
        """
        total = len(istanze)
        cache_key = self._get_cache_key(istanze, self.model)
        
        # Tenta di caricare progresso precedente
        results = []
        start_index = 0
        
        if resume:
            saved_state = self._load_progress(cache_key)
            if saved_state:
                results = saved_state["results"]
                start_index = saved_state["current_index"]
                print("\n🔄 Ripresa analisi precedente:")
                print(f"   Già completate: {start_index}/{total} istanze")
                print(f"   Timestamp: {saved_state['timestamp']}")
                print(f"   Modello: {saved_state['model']}")
        
        if start_index == 0:
            print(f"\n🚀 Nuova classificazione batch: {total} istanze")
            print(f"   Modello: {self.model}")
            print(f"   Salvataggio automatico ogni {save_interval} istanze")
        
        print("=" * 80)
        
        start_batch = time.time()
        
        # Progress bar con tqdm
        with tqdm(total=total, initial=start_index, 
                  desc=f"Classificazione ({self.model})",
                  unit="istanza",
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:
            
            try:
                for i in range(start_index, total):
                    istanza = istanze[i]
                    
                    result = self.classify_single(istanza)
                    
                    # Aggiungi ground truth se disponibile
                    if true_labels and i < len(true_labels):
                        true_proc = true_labels[i]
                        result.update({
                            "true_procedimento": true_proc,
                            "correct": result.get("procedimento") == true_proc if result.get("success") else False
                        })
                    
                    result["istanza_id"] = i + 1
                    result["istanza_text"] = istanza[:200] + "..." if len(istanza) > 200 else istanza
                    results.append(result)
                    
                    # Salva progresso periodicamente
                    if (i + 1) % save_interval == 0:
                        self._save_progress(cache_key, results, i + 1)
                        pbar.set_postfix({"saved": "✓"})
                    
                    pbar.update(1)
                    
                    # Rispetta rate limits Groq
                    time.sleep(0.1)
                    
            except KeyboardInterrupt:
                print("\n\n⏸️  Analisi interrotta dall'utente")
                self._save_progress(cache_key, results, len(results))
                print(f"   Progresso salvato: {len(results)}/{total} istanze")
                print("   Per riprendere, riesegui con resume=True")
                
                df = pd.DataFrame(results)
                return df
        
        total_time = time.time() - start_batch
        
        print("=" * 80)
        print("✅ Batch completato!")
        print(f"   Tempo totale: {total_time:.1f}s")
        print(f"   Velocità media: {total/total_time:.1f} istanze/s")
        print(f"   Throughput: {total/total_time*60:.0f} istanze/min")
        
        df = pd.DataFrame(results)
        
        # Calcola statistiche se labels disponibili
        if true_labels and len(true_labels) > 0:
            self._print_accuracy_report(df)
        
        # Rimuovi cache al completamento
        self._clear_cache(cache_key)
        
        return df
    
    def _print_accuracy_report(self, df: pd.DataFrame):
        """Stampa report accuracy dettagliato"""
        successful = df[df['success'] == True]
        
        if len(successful) == 0:
            print("\n⚠️  Nessuna classificazione riuscita")
            return
        
        acc = successful['correct'].mean() * 100
        avg_conf = successful['confidence'].mean()
        avg_latency = successful['latency'].mean()
        avg_tokens = successful['tokens_used'].mean()
        
        print("\n📊 METRICHE PERFORMANCE:")
        print(f"   Accuracy Procedimento:       {acc:.1f}%")
        print(f"   Confidence Media:            {avg_conf:.2f}")
        print(f"   Latenza Media:               {avg_latency:.3f}s")
        print(f"   Token Medi per Istanza:      {avg_tokens:.0f}")
    
    def export_results(self, 
                      results_df: pd.DataFrame,
                      filename: Optional[str] = None) -> str:
        """Esporta risultati in CSV con timestamp"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"procedural_classification_results_{timestamp}.csv"
        
        results_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 Risultati salvati: {filename}")
        return filename


def quick_test_classifier(api_key: Optional[str] = None):
    """Test rapido per verificare setup"""
    
    print("=" * 80)
    print("🧪 QUICK TEST PROCEDURAL CLASSIFIER")
    print("=" * 80)
    
    try:
        classifier = ProceduralClassifier(api_key=api_key)
        
        # Test singolo
        test_istanza = """Spettabile Comune, la scrivente ABC S.p.A. richiede 
        autorizzazione allo scarico di acque reflue industriali provenienti dal 
        ciclo produttivo tessile. Portata media: 500 m³/giorno. Si allegano 
        relazione tecnica e planimetria degli impianti di depurazione."""
        
        print("\n📧 Istanza di test:")
        print(f"   {test_istanza[:150]}...")
        print("\n⏳ Classificazione in corso...\n")
        
        result = classifier.classify_single(test_istanza)
        
        if result['success']:
            print("✅ SUCCESSO!")
            print("\n📊 Risultato:")
            print(f"   Procedimento: {result['procedimento']}")
            print(f"   Denominazione: {result.get('procedimento_denominazione', 'N/A')}")
            print(f"   Tipo Provvedimento: {result['tipo_provvedimento']}")
            print(f"   Categoria: {result['categoria']}")
            print(f"   Autorità: {result['autorita_competente']}")
            print(f"   Normativa: {', '.join(result.get('normativa_base', []))}")
            print(f"   Termini: {result.get('termini_giorni', 'N/A')} giorni")
            print(f"   Confidence: {result['confidence']:.2f}")
            print(f"   Latenza: {result['latency']:.3f}s")
            print(f"\n💡 Motivazione: {result.get('motivazione', 'N/A')}")
            
            if result.get('metadata_extracted'):
                print(f"\n📋 Metadata estratti:")
                for key, value in result['metadata_extracted'].items():
                    print(f"   - {key}: {value}")
            
            return True
        else:
            print(f"❌ ERRORE: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Setup fallito: {e}")
        return False


# ============================================================================
# MAIN - Esempi di utilizzo
# ============================================================================

if __name__ == "__main__":
    
    print("🚀 PROCEDURAL CLASSIFIER - SP00")
    print("=" * 80)
    print("\nOpzioni:")
    print("1. Quick test (verifica setup)")
    print("2. Test con dataset procedimenti")
    
    # Per test rapido
    quick_test_classifier()
    
    print("\n💡 SETUP:")
    print("   1. Ottieni API key gratis: https://console.groq.com")
    print("   2. export GROQ_API_KEY='your-key'")
    print("   3. pip install groq")
    print("   4. Esegui: python groq_procedural_classifier.py")
