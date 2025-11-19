"""
Test Script per SP00 Procedural Classifier
Testa il classificatore con il dataset di procedimenti
"""

import sys
from pathlib import Path

# Aggiungi il path del modulo
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

from groq_procedural_classifier import ProceduralClassifier, quick_test_classifier
from procedimenti_dataset import create_procedimenti_dataset
import pandas as pd


def test_with_dataset():
    """Test completo con dataset procedimenti"""
    
    print("=" * 80)
    print("🧪 TEST SP00 CON DATASET PROCEDIMENTI")
    print("=" * 80)
    
    # Crea dataset di test
    print("\n📊 Creazione dataset di test...")
    df = create_procedimenti_dataset(n_samples_per_procedimento=2)
    print(f"✅ Dataset creato: {len(df)} istanze")
    
    # Campione ridotto per test rapido
    sample_size = min(10, len(df))
    df_sample = df.sample(n=sample_size, random_state=42)
    
    print(f"\n🎲 Campione per test: {sample_size} istanze")
    
    # Inizializza classifier
    print("\n🤖 Inizializzazione classificatore...")
    classifier = ProceduralClassifier(model="llama-3.3-70b-versatile")
    
    # Classifica batch
    print("\n🚀 Classificazione batch in corso...")
    istanze = df_sample['testo'].tolist()
    true_labels = df_sample['procedimento'].tolist()
    
    results_df = classifier.classify_batch(
        istanze=istanze,
        true_labels=true_labels,
        resume=False
    )
    
    # Analisi risultati
    print("\n" + "=" * 80)
    print("📊 ANALISI RISULTATI")
    print("=" * 80)
    
    successful = results_df[results_df['success'] == True]
    
    if len(successful) > 0:
        print(f"\n✅ Classificazioni riuscite: {len(successful)}/{len(results_df)}")
        
        # Accuracy
        if 'correct' in successful.columns:
            accuracy = successful['correct'].mean() * 100
            print(f"📈 Accuracy: {accuracy:.1f}%")
        
        # Confidence media
        avg_conf = successful['confidence'].mean()
        print(f"📊 Confidence media: {avg_conf:.2f}")
        
        # Latenza
        avg_latency = successful['latency'].mean()
        print(f"⏱️  Latenza media: {avg_latency:.3f}s")
        
        # Token usage
        avg_tokens = successful['tokens_used'].mean()
        print(f"🔢 Token medi: {avg_tokens:.0f}")
        
        # Distribuzione per categoria
        if 'categoria' in successful.columns:
            print("\n📋 Distribuzione per categoria:")
            print(successful['categoria'].value_counts().to_string())
        
        # Esempi di risultati
        print("\n" + "=" * 80)
        print("📝 ESEMPI DI CLASSIFICAZIONI")
        print("=" * 80)
        
        for idx in range(min(3, len(successful))):
            row = successful.iloc[idx]
            print(f"\n{idx+1}. Istanza ID: {row.get('istanza_id', 'N/A')}")
            print(f"   Testo: {row.get('istanza_text', '')[:100]}...")
            print(f"   Procedimento Predetto: {row.get('procedimento', 'N/A')}")
            if 'true_procedimento' in row:
                print(f"   Procedimento Vero: {row.get('true_procedimento', 'N/A')}")
                correct = "✅" if row.get('correct', False) else "❌"
                print(f"   Corretto: {correct}")
            print(f"   Provvedimento: {row.get('tipo_provvedimento', 'N/A')}")
            print(f"   Confidence: {row.get('confidence', 0.0):.2f}")
            print("-" * 80)
    
    else:
        print("❌ Nessuna classificazione riuscita")
    
    # Esporta risultati
    print("\n💾 Esportazione risultati...")
    filename = classifier.export_results(results_df)
    print(f"✅ Risultati salvati in: {filename}")
    
    return results_df


def main():
    """Main function"""
    
    print("\n🏛️ SP00 - PROCEDURAL CLASSIFIER TEST SUITE")
    print("=" * 80)
    
    # Menu
    print("\nScegli il tipo di test:")
    print("1. Quick test (singola istanza)")
    print("2. Test con dataset (batch)")
    print("3. Entrambi")
    
    try:
        choice = input("\nScelta (1/2/3): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Test interrotto")
        return
    
    if choice == "1":
        quick_test_classifier()
    
    elif choice == "2":
        test_with_dataset()
    
    elif choice == "3":
        quick_test_classifier()
        print("\n" + "=" * 80)
        print("Proseguo con test dataset...")
        print("=" * 80)
        test_with_dataset()
    
    else:
        print("❌ Scelta non valida")
    
    print("\n✅ Test completati!")


if __name__ == "__main__":
    main()
