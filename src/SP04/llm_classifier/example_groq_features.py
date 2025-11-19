"""
Esempio di utilizzo delle nuove funzionalità di groq_integration:
1. Recupero dinamico modelli
2. Progress bar con tqdm
3. Persistenza e ripresa analisi
"""

import os
from groq_integration import GroqClassifier
import pandas as pd
from dotenv import load_dotenv

# Carica variabili d'ambiente dal file .env
load_dotenv()

def esempio_recupero_modelli():
    """Esempio: recupero modelli disponibili da API Groq"""
    print("=" * 80)
    print("ESEMPIO 1: Recupero Modelli Disponibili")
    print("=" * 80)
    
    api_key = os.environ.get("GROQ_API_KEY")
    classifier = GroqClassifier(api_key=api_key)
    
    # Recupera tutti i modelli disponibili
    print("\n📋 Recupero modelli dall'API Groq...")
    available = classifier.fetch_available_models()
    
    print(f"\n✅ Trovati {len(available)} modelli:")
    for model in available:
        status = "🟢" if model.get("active", True) else "🔴"
        print(f"   {status} {model['id']}")
    
    # Ottieni modelli consigliati
    recommended = classifier.get_recommended_models()
    print(f"\n⭐ Modelli consigliati: {len(recommended)}")
    for model in recommended:
        print(f"   • {model}")


def esempio_progress_bar():
    """Esempio: classificazione con progress bar"""
    print("\n" + "=" * 80)
    print("ESEMPIO 2: Classificazione con Progress Bar")
    print("=" * 80)
    
    api_key = os.environ.get("GROQ_API_KEY")
    classifier = GroqClassifier(api_key=api_key)
    
    # Email di test
    test_emails = [
        "Segnalo grave errore chirurgico del 15/03/2024...",
        "Rif. pratica SIN12345, invio documentazione integrativa...",
        "Comunico situazione di potenziale rischio per paziente...",
        "Aggiorno su circostanza segnalata precedentemente...",
    ] * 5  # 20 email totali
    
    print(f"\n📧 Classifico {len(test_emails)} email con progress bar...")
    
    # Classifica con progress bar
    results = classifier.classify_batch(
        emails=test_emails,
        resume=True,  # Abilita ripresa
        save_interval=5  # Salva ogni 5 email
    )
    
    print(f"\n✅ Completato! Risultati: {len(results)} righe")
    print("\nPrime 3 classificazioni:")
    print(results[['email_id', 'tipologia', 'riferimento_temporale', 'latency']].head(3))


def esempio_persistenza():
    """Esempio: interruzione e ripresa analisi"""
    print("\n" + "=" * 80)
    print("ESEMPIO 3: Persistenza e Ripresa Analisi")
    print("=" * 80)
    
    api_key = os.environ.get("GROQ_API_KEY")
    classifier = GroqClassifier(
        api_key=api_key,
        cache_dir="groq_study_results/.cache"  # Directory cache personalizzata
    )
    
    # Simula un dataset più grande
    test_emails = [
        f"Email di test numero {i} sul sinistro..." for i in range(50)
    ]
    
    print(f"\n📧 Classifico {len(test_emails)} email...")
    print("💡 Premi Ctrl+C per interrompere durante l'esecuzione")
    print("   Poi riesegui questa funzione per riprendere\n")
    
    try:
        results = classifier.classify_batch(
            emails=test_emails,
            resume=True,  # Riprende automaticamente se interrotto
            save_interval=10  # Salva ogni 10 email
        )
        
        print(f"\n✅ Analisi completata: {len(results)} email classificate")
        
    except KeyboardInterrupt:
        print("\n⏸️  Analisi interrotta! Per riprendere, riesegui questa funzione")


def esempio_confronto_modelli():
    """Esempio: confronto modelli con progress tracking"""
    print("\n" + "=" * 80)
    print("ESEMPIO 4: Confronto Modelli con Progress Bar")
    print("=" * 80)
    
    api_key = os.environ.get("GROQ_API_KEY")
    classifier = GroqClassifier(api_key=api_key)
    
    # Email di test con ground truth
    test_emails = [
        "Segnalo grave errore chirurgico del 15/03/2024...",
        "Rif. pratica SIN12345, invio documentazione...",
        "Comunico situazione di potenziale rischio...",
    ] * 10  # 30 email
    
    true_labels = [(0, 0), (0, 1), (1, 0)] * 10  # Ground truth
    
    print(f"\n🏁 Confronto modelli su {len(test_emails)} email...")
    print("   I modelli vengono recuperati dinamicamente dall'API\n")
    
    # Confronta modelli (usa quelli disponibili)
    comparison = classifier.compare_models(
        test_emails=test_emails,
        true_labels=true_labels,
        models=None,  # Recupera automaticamente i modelli consigliati
        resume=True
    )
    
    print("\n📊 Risultati confronto:")
    print(comparison[['model', 'accuracy_both', 'throughput', 'avg_latency']])
    
    # Identifica il migliore
    best = comparison.loc[comparison['accuracy_both'].idxmax()]
    print(f"\n🏆 Migliore modello: {best['model']}")
    print(f"   Accuracy: {best['accuracy_both']:.1f}%")
    print(f"   Throughput: {best['throughput']:.1f} email/s")


if __name__ == "__main__":
    print("\n🚀 ESEMPI NUOVE FUNZIONALITÀ GROQ INTEGRATION\n")
    
    # Verifica API key
    if not os.environ.get("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY non trovata nelle variabili d'ambiente")
        print("   Imposta con: export GROQ_API_KEY='your-key-here'")
        exit(1)
    
    # Menu interattivo
    print("Scegli esempio da eseguire:")
    print("1. Recupero modelli disponibili")
    print("2. Classificazione con progress bar")
    print("3. Persistenza e ripresa analisi")
    print("4. Confronto modelli")
    print("5. Tutti gli esempi")
    
    choice = input("\nScelta (1-5): ").strip()
    
    if choice == "1":
        esempio_recupero_modelli()
    elif choice == "2":
        esempio_progress_bar()
    elif choice == "3":
        esempio_persistenza()
    elif choice == "4":
        esempio_confronto_modelli()
    elif choice == "5":
        esempio_recupero_modelli()
        esempio_progress_bar()
        esempio_persistenza()
        esempio_confronto_modelli()
    else:
        print("❌ Scelta non valida")
    
    print("\n✅ Esempio completato!")
