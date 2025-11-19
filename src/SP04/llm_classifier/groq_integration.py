"""
Sistema di Classificazione Sinistri con Groq API
Ultra-veloce per analisi e studio su grandi volumi
"""

import os
from groq import Groq
import json
import pandas as pd
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import numpy as np
from tqdm import tqdm
import hashlib
import pickle
from dotenv import load_dotenv

# Carica variabili d'ambiente dal file .env nella root del progetto
load_dotenv()

class GroqClassifier:
    """
    Classificatore veloce usando Groq API
    Ideale per batch processing e analisi rapida
    
    Features:
    - Recupero dinamico modelli da Groq API
    - Progress bar con tqdm
    - Persistenza stato per riprend    # Esporta risultati
    filename = classifier.export_results(results_df)
    
    print("\n✅ Analisi completata!")
    print("\n📊 File generati:")
    print(f"   {filename}")alisi interrotte
    """
    
    # Modelli disponibili su Groq (ordinati per velocità) - DEPRECATO, usa fetch_available_models()
    AVAILABLE_MODELS = {
        "llama-3.1-70b-versatile": {
            "speed": "ultra_fast",
            "quality": "high",
            "cost": "low",
            "recommended": True
        },
        "llama-3.1-8b-instant": {
            "speed": "lightning",
            "quality": "good", 
            "cost": "very_low",
            "recommended": True  # Per studio veloce
        },
        "mixtral-8x7b-32768": {
            "speed": "very_fast",
            "quality": "high",
            "cost": "low",
            "recommended": False
        },
        "gemma2-9b-it": {
            "speed": "very_fast",
            "quality": "good",
            "cost": "very_low",
            "recommended": False
        }
    }
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-8b-instant", 
                 cache_dir: str = "groq_study_results/.cache"):
        """
        Inizializza classificatore Groq
        
        Args:
            api_key: Groq API key (o usa variabile ambiente GROQ_API_KEY)
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
        
        # System prompt ottimizzato
        self.system_prompt = """Sei un esperto classificatore di sinistri assicurativi nel settore medical malpractice.

COMPITO: Classifica email secondo DUE dimensioni.

DIMENSIONE 1 - TIPOLOGIA:
- 0 = Sinistro Avvenuto: evento dannoso GIÀ verificato, richiesta risarcimento
  Indicatori: verbi passati ("è avvenuto", "si è verificato"), data evento, "richiesta danni"
  
- 1 = Circostanza Potenziale: situazione rischiosa che POTREBBE causare sinistro
  Indicatori: "potrebbe", "rischia", "temo", "sono preoccupato", verbi futuro/presente

DIMENSIONE 2 - RIFERIMENTO TEMPORALE:
- 0 = Fatto Iniziale: prima segnalazione del caso
  Indicatori: assenza riferimenti precedenti
  
- 1 = Follow-up: aggiornamento su caso già segnalato
  Indicatori: "Rif. pratica", "caso ID", "come da precedente", "aggiorno"

Rispondi SOLO con JSON valido:
{
    "tipologia": 0 o 1,
    "riferimento_temporale": 0 o 1,
    "confidence_tipologia": 0.0-1.0,
    "confidence_riferimento": 0.0-1.0,
    "spiegazione": "breve motivazione (max 50 parole)",
    "indicatori_chiave": ["max", "5", "parole/frasi", "determinanti"]
}

IMPORTANTE: Rispondi SOLO con il JSON, nessun testo aggiuntivo."""
    
    def fetch_available_models(self) -> List[Dict[str, str]]:
        """
        Recupera lista modelli disponibili dall'API Groq
        
        Returns:
            Lista di dizionari con info sui modelli disponibili
        """
        try:
            response = self.client.models.list()
            models = []
            
            for model in response.data:
                models.append({
                    "id": model.id,
                    "owned_by": model.owned_by,
                    "active": getattr(model, 'active', True),
                    "context_window": getattr(model, 'context_window', None)
                })
            
            return models
            
        except Exception as e:
            print(f"⚠️ Errore recupero modelli: {e}")
            print("Uso fallback a modelli predefiniti")
            return []
    
    def get_recommended_models(self) -> List[str]:
        """
        Ottiene lista modelli consigliati per classificazione
        
        Returns:
            Lista di model IDs consigliati
        """
        available = self.fetch_available_models()
        
        if not available:
            # Fallback
            return ["llama-3.1-8b-instant", "llama-3.1-70b-versatile"]
        
        # Filtra modelli attivi e consigliati per il task
        recommended_keywords = ["llama", "mixtral", "gemma"]
        recommended = []
        
        for model in available:
            if model.get("active", True):
                model_id = model["id"]
                if any(kw in model_id.lower() for kw in recommended_keywords):
                    recommended.append(model_id)
        
        return recommended if recommended else [m["id"] for m in available[:5]]
    
    def _get_cache_key(self, emails: List[str], model: str) -> str:
        """Genera chiave univoca per cache basata su email e modello"""
        content = f"{model}_{len(emails)}_" + "".join(emails[:3])
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
    
    def classify_single(self, email_text: str, temperature: float = 0.1) -> Dict:
        """
        Classifica una singola email
        
        Returns:
            Dict con classificazione e metadati
        """
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Classifica questa email:\n\n{email_text}"}
                ],
                temperature=temperature,
                max_tokens=300,
                response_format={"type": "json_object"}  # Forza risposta JSON
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
                      emails: List[str], 
                      true_labels: Optional[List[Tuple[int, int]]] = None,
                      resume: bool = True,
                      save_interval: int = 10) -> pd.DataFrame:
        """
        Classifica batch di email con progress tracking e persistenza
        
        Args:
            emails: Lista testi email
            true_labels: Se fornite, calcola accuracy [(tip, rif), ...]
            resume: Se True, riprende da analisi precedente interrotta
            save_interval: Salva progresso ogni N email
            
        Returns:
            DataFrame con risultati
        """
        total = len(emails)
        cache_key = self._get_cache_key(emails, self.model)
        
        # Tenta di caricare progresso precedente
        results = []
        start_index = 0
        
        if resume:
            saved_state = self._load_progress(cache_key)
            if saved_state:
                results = saved_state["results"]
                start_index = saved_state["current_index"]
                print("\n🔄 Ripresa analisi precedente:")
                print(f"   Già completate: {start_index}/{total} email")
                print(f"   Timestamp: {saved_state['timestamp']}")
                print(f"   Modello: {saved_state['model']}")
        
        if start_index == 0:
            print(f"\n🚀 Nuova classificazione batch: {total} email")
            print(f"   Modello: {self.model}")
            print(f"   Velocità attesa: ~{self._estimate_throughput()} email/min")
            print(f"   Salvataggio automatico ogni {save_interval} email")
        
        print("=" * 80)
        
        start_batch = time.time()
        
        # Progress bar con tqdm
        with tqdm(total=total, initial=start_index, 
                  desc=f"Classificazione ({self.model})",
                  unit="email",
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:
            
            try:
                for i in range(start_index, total):
                    email = emails[i]
                    
                    result = self.classify_single(email)
                    
                    # Aggiungi ground truth se disponibile
                    if true_labels and i < len(true_labels):
                        true_tip, true_rif = true_labels[i]
                        result.update({
                            "true_tipologia": true_tip,
                            "true_riferimento": true_rif,
                            "correct_tipologia": result.get("tipologia") == true_tip if result.get("success") else False,
                            "correct_riferimento": result.get("riferimento_temporale") == true_rif if result.get("success") else False
                        })
                    
                    result["email_id"] = i + 1
                    result["email_text"] = email[:100] + "..." if len(email) > 100 else email
                    results.append(result)
                    
                    # Salva progresso periodicamente
                    if (i + 1) % save_interval == 0:
                        self._save_progress(cache_key, results, i + 1)
                        pbar.set_postfix({"saved": "✓"})
                    
                    pbar.update(1)
                    
                    # Rispetta rate limits Groq (generoso ma meglio essere prudenti)
                    time.sleep(0.1)  # 100ms tra richieste = max 10 req/s
                    
            except KeyboardInterrupt:
                print("\n\n⏸️  Analisi interrotta dall'utente")
                self._save_progress(cache_key, results, len(results))
                print(f"   Progresso salvato: {len(results)}/{total} email")
                print("   Per riprendere, riesegui la stessa chiamata con resume=True")
                
                # Restituisci risultati parziali
                df = pd.DataFrame(results)
                return df
        
        total_time = time.time() - start_batch
        
        print("=" * 80)
        print("✅ Batch completato!")
        print(f"   Tempo totale: {total_time:.1f}s")
        print(f"   Velocità media: {total/total_time:.1f} email/s")
        print(f"   Throughput: {total/total_time*60:.0f} email/min")
        
        df = pd.DataFrame(results)
        
        # Calcola statistiche se labels disponibili
        if true_labels and len(true_labels) > 0:
            self._print_accuracy_report(df)
        
        # Rimuovi cache al completamento
        self._clear_cache(cache_key)
        
        return df
    
    def _estimate_throughput(self) -> int:
        """Stima throughput email/min per il modello"""
        throughputs = {
            "llama-3.1-8b-instant": 120,
            "llama-3.1-70b-versatile": 60,
            "mixtral-8x7b-32768": 80,
            "gemma2-9b-it": 100
        }
        return throughputs.get(self.model, 60)
    
    def _print_accuracy_report(self, df: pd.DataFrame):
        """Stampa report accuracy dettagliato"""
        successful = df[df['success'] == True]
        
        if len(successful) == 0:
            print("\n⚠️  Nessuna classificazione riuscita")
            return
        
        acc_tip = successful['correct_tipologia'].mean() * 100
        acc_rif = successful['correct_riferimento'].mean() * 100
        acc_both = (successful['correct_tipologia'] & 
                   successful['correct_riferimento']).mean() * 100
        
        avg_conf_tip = successful['confidence_tipologia'].mean()
        avg_conf_rif = successful['confidence_riferimento'].mean()
        
        avg_latency = successful['latency'].mean()
        avg_tokens = successful['tokens_used'].mean()
        
        print("\n📊 METRICHE PERFORMANCE:")
        print(f"   Accuracy Tipologia:          {acc_tip:.1f}%")
        print(f"   Accuracy Riferimento:        {acc_rif:.1f}%")
        print(f"   Accuracy Entrambe:           {acc_both:.1f}%")
        print(f"\n   Confidence Media Tipologia:  {avg_conf_tip:.2f}")
        print(f"   Confidence Media Riferimento:{avg_conf_rif:.2f}")
        print(f"\n   Latenza Media:               {avg_latency:.3f}s")
        print(f"   Token Medi per Email:        {avg_tokens:.0f}")
    
    def compare_models(self, 
                      test_emails: List[str],
                      true_labels: List[Tuple[int, int]],
                      models: Optional[List[str]] = None,
                      resume: bool = True) -> pd.DataFrame:
        """
        Confronta performance di diversi modelli Groq con progress tracking
        
        Args:
            test_emails: Campione email per test
            true_labels: Ground truth labels
            models: Lista modelli da testare (default: quelli disponibili da API)
            resume: Riprendi analisi interrotta
            
        Returns:
            DataFrame comparativo
        """
        if models is None:
            # Recupera modelli disponibili dinamicamente
            print("\n🔍 Recupero modelli disponibili dall'API Groq...")
            available_models = self.get_recommended_models()
            models = available_models[:5]  # Limita a 5 per evitare troppi test
            print(f"   Trovati {len(available_models)} modelli, uso i primi {len(models)}")
            for m in models:
                print(f"      • {m}")
        
        print("\n" + "=" * 80)
        print("🏁 BENCHMARK MULTI-MODELLO GROQ")
        print("=" * 80)
        print(f"Modelli da testare: {len(models)}")
        print(f"Email per modello: {len(test_emails)}")
        print(f"Totale classificazioni: {len(models) * len(test_emails)}")
        
        comparison_results = []
        
        # Progress bar per i modelli
        with tqdm(total=len(models), desc="Modelli testati", unit="model") as model_pbar:
            for model_name in models:
                print(f"\n🤖 Testing: {model_name}")
                print("-" * 80)
                
                # Cambia modello temporaneamente
                original_model = self.model
                self.model = model_name
                
                # Classifica batch con progress bar
                results_df = self.classify_batch(
                    emails=test_emails,
                    true_labels=true_labels,
                    resume=resume
                )
                
                # Calcola metriche aggregate
                successful = results_df[results_df['success'] == True]
                
                if len(successful) > 0:
                    comparison_results.append({
                        "model": model_name,
                        "accuracy_tipologia": successful['correct_tipologia'].mean() * 100,
                        "accuracy_riferimento": successful['correct_riferimento'].mean() * 100,
                        "accuracy_both": (successful['correct_tipologia'] & 
                                        successful['correct_riferimento']).mean() * 100,
                        "avg_confidence": (successful['confidence_tipologia'].mean() + 
                                         successful['confidence_riferimento'].mean()) / 2,
                        "avg_latency": successful['latency'].mean(),
                        "throughput": len(successful) / successful['latency'].sum(),
                        "avg_tokens": successful['tokens_used'].mean()
                    })
                
                # Ripristina modello
                self.model = original_model
                
                model_pbar.update(1)
        
        # Crea DataFrame comparativo
        comparison_df = pd.DataFrame(comparison_results)
        
        # Stampa tabella comparativa
        print("\n" + "=" * 80)
        print("📊 TABELLA COMPARATIVA")
        print("=" * 80)
        print(comparison_df.to_string(index=False))
        
        # Identifica vincitore
        if len(comparison_df) > 0:
            best_accuracy = comparison_df.loc[comparison_df['accuracy_both'].idxmax()]
            best_speed = comparison_df.loc[comparison_df['throughput'].idxmax()]
            
            print("\n🏆 VINCITORI:")
            print(f"   Migliore Accuracy: {best_accuracy['model']} ({best_accuracy['accuracy_both']:.1f}%)")
            print(f"   Più Veloce:        {best_speed['model']} ({best_speed['throughput']:.1f} email/s)")
        
        return comparison_df
    
    def export_results(self, 
                      results_df: pd.DataFrame,
                      filename: Optional[str] = None) -> str:
        """Esporta risultati in CSV con timestamp"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"groq_classification_results_{timestamp}.csv"
        
        results_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 Risultati salvati: {filename}")
        return filename


def quick_test_groq(api_key: Optional[str] = None):
    """Test rapido per verificare setup Groq"""
    
    print("=" * 80)
    print("🧪 QUICK TEST GROQ API")
    print("=" * 80)
    
    try:
        classifier = GroqClassifier(api_key=api_key)
        
        # Test singolo
        test_email = """Buongiorno, vi scrivo per segnalare un grave errore 
        chirurgico avvenuto il 15 marzo 2024. Durante l'intervento al ginocchio 
        sinistro, il chirurgo ha operato per errore il ginocchio destro sano."""
        
        print("\n📧 Email di test:")
        print(f"   {test_email[:100]}...")
        print("\n⏳ Classificazione in corso...\n")
        
        result = classifier.classify_single(test_email)
        
        if result['success']:
            print("✅ SUCCESSO!")
            print("\n📊 Risultato:")
            print(f"   Tipologia: {result['tipologia']} (Sinistro Avvenuto)")
            print(f"   Riferimento: {result['riferimento_temporale']} (Fatto Iniziale)")
            print(f"   Confidence: Tip={result['confidence_tipologia']:.2f}, Rif={result['confidence_riferimento']:.2f}")
            print(f"   Latenza: {result['latency']:.3f}s")
            print(f"   Velocità: {result['tokens_per_second']:.0f} tokens/s")
            print(f"\n💡 Spiegazione: {result['spiegazione']}")
            print(f"   Indicatori: {', '.join(result['indicatori_chiave'])}")
            
            return True
        else:
            print(f"❌ ERRORE: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Setup fallito: {e}")
        print("\n💡 Verifica:")
        print("   1. API key corretta")
        print("   2. Groq package installato: pip install groq")
        print("   3. Connessione internet attiva")
        return False


def full_dataset_analysis(api_key: Optional[str] = None, 
                         dataset_path: str = "dataset_medical_malpractice_complete.csv",
                         sample_size: int = 100):
    """
    Analisi completa del dataset con Groq
    Usa per studiare performance su tutti i modelli velocemente
    """
    
    print("=" * 80)
    print("🔬 ANALISI COMPLETA DATASET CON GROQ")
    print("=" * 80)
    
    # Carica dataset
    print(f"\n📂 Caricamento dataset: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"✅ Dataset caricato: {len(df)} email totali")
    
    # Campiona bilanciato
    print(f"\n🎲 Campionamento bilanciato: {sample_size} email")
    sample = []
    samples_per_category = sample_size // 4
    
    for tip in [0, 1]:
        for rif in [0, 1]:
            subset = df[(df['tipologia'] == tip) & 
                       (df['riferimento_temporale'] == rif)].sample(
                           n=min(samples_per_category, len(df[(df['tipologia'] == tip) & 
                                                              (df['riferimento_temporale'] == rif)])),
                           random_state=42
                       )
            sample.append(subset)
    
    sample_df = pd.concat(sample).reset_index(drop=True)
    
    emails = sample_df['testo'].tolist()
    labels = list(zip(sample_df['tipologia'], sample_df['riferimento_temporale']))
    
    print(f"✅ Campione preparato: {len(sample_df)} email")
    
    # Inizializza classifier
    classifier = GroqClassifier(api_key=api_key, model="llama-3.1-8b-instant")
    
    # Confronta modelli
    comparison_df = classifier.compare_models(
        test_emails=emails,
        true_labels=labels
    )
    
    # Classifica tutto il campione con il migliore
    best_model_value = comparison_df.loc[comparison_df['accuracy_both'].idxmax(), 'model']
    best_model = str(best_model_value)
    print(f"\n🎯 Analisi completa con modello migliore: {best_model}")
    
    classifier.model = best_model
    results_df = classifier.classify_batch(emails, labels)
    
    # Esporta risultati
    filename = classifier.export_results(results_df)
    
    print("\n✅ Analisi completata!")
    print("\n📊 File generati:")
    print(f"   • {filename}")
    
    return results_df, comparison_df


# ============================================================================
# MAIN - Esempi di utilizzo
# ============================================================================

if __name__ == "__main__":
    
    print("🚀 GROQ CLASSIFIER PER SINISTRI MEDICAL MALPRACTICE")
    print("=" * 80)
    print("\nOpzioni:")
    print("1. Quick test (verifica setup)")
    print("2. Analisi completa dataset")
    print("3. Confronto modelli")
    
    # Per test rapido
    # quick_test_groq()
    
    # Per analisi completa (decommentare e fornire API key)
    # full_dataset_analysis(
    #     api_key="your-groq-api-key",
    #     sample_size=200
    # )
    
    print("\n💡 SETUP:")
    print("   1. Ottieni API key gratis: https://console.groq.com")
    print("   2. export GROQ_API_KEY='your-key'")
    print("   3. pip install groq")
    print("   4. Esegui: python groq_classifier.py")