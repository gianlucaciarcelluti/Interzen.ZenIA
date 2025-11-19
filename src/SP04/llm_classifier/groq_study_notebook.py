"""
Notebook Studio Completo: Classificazione Sinistri con Groq
Esegui step-by-step per analisi rapida e iterativa
"""

import os
from groq_integration import GroqClassifier, quick_test_groq, full_dataset_analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# ============================================================================
# STEP 1: CONFIGURAZIONE
# ============================================================================

print("=" * 80)
print("📚 STUDIO CLASSIFICAZIONE SINISTRI CON GROQ")
print("=" * 80)

# Inserisci la tua API key (o usa variabile ambiente)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "inserisci-qui-se-non-usi-env")

# Configurazione studio
CONFIG = {
    "dataset_path": "dataset_medical_malpractice_complete.csv",
    "sample_sizes": [50, 100, 200],  # Diversi sample size per test
    "models_to_test": [
        "llama-3.1-8b-instant",      # Velocissimo
        "llama-3.1-70b-versatile"    # Più accurato
    ],
    "export_dir": "groq_study_results"
}

# Crea directory risultati
os.makedirs(CONFIG["export_dir"], exist_ok=True)

print(f"\n✅ Configurazione caricata")
print(f"   Dataset: {CONFIG['dataset_path']}")
print(f"   Modelli: {len(CONFIG['models_to_test'])}")
print(f"   Output: {CONFIG['export_dir']}/")

# ============================================================================
# STEP 2: VERIFICA CONNESSIONE
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1: Verifica Setup")
print("=" * 80)

if quick_test_groq(GROQ_API_KEY):
    print("\n✅ Setup verificato! Pronto per lo studio")
else:
    print("\n❌ Setup fallito. Verifica API key e connessione")
    exit(1)

# ============================================================================
# STEP 3: CARICA E ANALIZZA DATASET
# ============================================================================

print("\n" + "=" * 80)
print("STEP 2: Analisi Dataset")
print("=" * 80)

df = pd.read_csv(CONFIG["dataset_path"])

print(f"\n📊 Statistiche Dataset:")
print(f"   Totale email: {len(df)}")
print(f"\n   Distribuzione Tipologia:")
for tip in [0, 1]:
    count = len(df[df['tipologia'] == tip])
    pct = count / len(df) * 100
    label = "Sinistro Avvenuto" if tip == 0 else "Circostanza Potenziale"
    print(f"      {tip} ({label}): {count} ({pct:.1f}%)")

print(f"\n   Distribuzione Riferimento:")
for rif in [0, 1]:
    count = len(df[df['riferimento_temporale'] == rif])
    pct = count / len(df) * 100
    label = "Fatto Iniziale" if rif == 0 else "Follow-up"
    print(f"      {rif} ({label}): {count} ({pct:.1f}%)")

print(f"\n   Distribuzione Combinata:")
for tip in [0, 1]:
    for rif in [0, 1]:
        count = len(df[(df['tipologia'] == tip) & (df['riferimento_temporale'] == rif)])
        print(f"      Tip={tip}, Rif={rif}: {count}")

# ============================================================================
# STEP 4: ESPERIMENTO 1 - Test Velocità vs Accuratezza
# ============================================================================

print("\n" + "=" * 80)
print("STEP 3: Esperimento - Velocità vs Accuratezza")
print("=" * 80)

# Prepara campione test bilanciato (100 email)
sample_size = 100
samples_per_cat = sample_size // 4

test_sample = []
for tip in [0, 1]:
    for rif in [0, 1]:
        subset = df[(df['tipologia'] == tip) & 
                   (df['riferimento_temporale'] == rif)].sample(
                       samples_per_cat, random_state=42
                   )
        test_sample.append(subset)

test_df = pd.concat(test_sample).reset_index(drop=True)
test_emails = test_df['testo'].tolist()
test_labels = list(zip(test_df['tipologia'], test_df['riferimento_temporale']))

print(f"\n📧 Campione test preparato: {len(test_df)} email")

# Confronta modelli
classifier = GroqClassifier(api_key=GROQ_API_KEY)
comparison_df = classifier.compare_models(
    test_emails=test_emails,
    true_labels=test_labels,
    models=CONFIG["models_to_test"]
)

# Salva risultati
comparison_file = f"{CONFIG['export_dir']}/model_comparison.csv"
comparison_df.to_csv(comparison_file, index=False)
print(f"\n💾 Confronto salvato: {comparison_file}")

# ============================================================================
# STEP 5: ESPERIMENTO 2 - Analisi Errori
# ============================================================================

print("\n" + "=" * 80)
print("STEP 4: Analisi Errori Dettagliata")
print("=" * 80)

# Usa il modello migliore dal confronto
best_model = comparison_df.loc[comparison_df['accuracy_both'].idxmax(), 'model']
print(f"\n🎯 Usando modello migliore: {best_model}")

classifier.model = best_model
results_df = classifier.classify_batch(test_emails, test_labels, show_progress=True)

# Identifica errori
errors_df = results_df[
    (results_df['success'] == True) & 
    ((results_df['correct_tipologia'] == False) | 
     (results_df['correct_riferimento'] == False))
]

print(f"\n❌ Analisi Errori:")
print(f"   Totale errori: {len(errors_df)}/{len(results_df)}")

if len(errors_df) > 0:
    print(f"\n   Top 5 Errori:")
    for idx, row in errors_df.head(5).iterrows():
        print(f"\n   Email: {row['email_text']}")
        print(f"   Predetto: Tip={row['tipologia']}, Rif={row['riferimento_temporale']}")
        print(f"   Corretto: Tip={row['true_tipologia']}, Rif={row['true_riferimento']}")
        print(f"   Spiegazione: {row.get('spiegazione', 'N/A')}")
        print(f"   Confidence: Tip={row.get('confidence_tipologia', 0):.2f}, "
              f"Rif={row.get('confidence_riferimento', 0):.2f}")

# Salva errori per analisi
errors_file = f"{CONFIG['export_dir']}/classification_errors.csv"
errors_df.to_csv(errors_file, index=False)
print(f"\n💾 Errori salvati: {errors_file}")

# ============================================================================
# STEP 6: ESPERIMENTO 3 - Matrice di Confusione
# ============================================================================

print("\n" + "=" * 80)
print("STEP 5: Matrici di Confusione")
print("=" * 80)

successful = results_df[results_df['success'] == True]

# Matrice per Tipologia
y_true_tip = successful['true_tipologia']
y_pred_tip = successful['tipologia']

cm_tip = confusion_matrix(y_true_tip, y_pred_tip)

print("\n📊 Matrice Confusione - TIPOLOGIA:")
print("                    Predetto")
print("                  0 (Sin)  1 (Circ)")
print(f"Vero  0 (Sin)    {cm_tip[0,0]:5d}    {cm_tip[0,1]:5d}")
print(f"      1 (Circ)   {cm_tip[1,0]:5d}    {cm_tip[1,1]:5d}")

# Matrice per Riferimento Temporale
y_true_rif = successful['true_riferimento']
y_pred_rif = successful['riferimento_temporale']

cm_rif = confusion_matrix(y_true_rif, y_pred_rif)

print("\n📊 Matrice Confusione - RIFERIMENTO TEMPORALE:")
print("                    Predetto")
print("                  0 (Iniz)  1 (Foll)")
print(f"Vero  0 (Iniz)   {cm_rif[0,0]:5d}    {cm_rif[0,1]:5d}")
print(f"      1 (Foll)   {cm_rif[1,0]:5d}    {cm_rif[1,1]:5d}")

# Visualizza matrici con heatmap
try:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Tipologia
    sns.heatmap(cm_tip, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=['Sinistro', 'Circostanza'],
                yticklabels=['Sinistro', 'Circostanza'])
    axes[0].set_title('Matrice Confusione - TIPOLOGIA')
    axes[0].set_ylabel('Vero')
    axes[0].set_xlabel('Predetto')
    
    # Riferimento
    sns.heatmap(cm_rif, annot=True, fmt='d', cmap='Greens', ax=axes[1],
                xticklabels=['Iniziale', 'Follow-up'],
                yticklabels=['Iniziale', 'Follow-up'])
    axes[1].set_title('Matrice Confusione - RIFERIMENTO TEMPORALE')
    axes[1].set_ylabel('Vero')
    axes[1].set_xlabel('Predetto')
    
    plt.tight_layout()
    
    confusion_plot = f"{CONFIG['export_dir']}/confusion_matrices.png"
    plt.savefig(confusion_plot, dpi=300, bbox_inches='tight')
    print(f"\n💾 Grafici salvati: {confusion_plot}")
    plt.close()
    
except Exception as e:
    print(f"\n⚠️  Grafici non generati (matplotlib non disponibile): {e}")

# ============================================================================
# STEP 7: ESPERIMENTO 4 - Analisi Confidence
# ============================================================================

print("\n" + "=" * 80)
print("STEP 6: Analisi Confidence Scores")
print("=" * 80)

# Analizza relazione confidence/correttezza
correct_predictions = successful[
    (successful['correct_tipologia'] == True) & 
    (successful['correct_riferimento'] == True)
]
incorrect_predictions = successful[
    (successful['correct_tipologia'] == False) | 
    (successful['correct_riferimento'] == False)
]

print(f"\n📈 Confidence Scores:")
print(f"\n   Predizioni CORRETTE:")
print(f"      Media Confidence Tipologia:    {correct_predictions['confidence_tipologia'].mean():.3f}")
print(f"      Media Confidence Riferimento:  {correct_predictions['confidence_riferimento'].mean():.3f}")

if len(incorrect_predictions) > 0:
    print(f"\n   Predizioni ERRATE:")
    print(f"      Media Confidence Tipologia:    {incorrect_predictions['confidence_tipologia'].mean():.3f}")
    print(f"      Media Confidence Riferimento:  {incorrect_predictions['confidence_riferimento'].mean():.3f}")
    
    # Identifica predizioni con alta confidence ma errate (falsi positivi pericolosi)
    high_conf_errors = incorrect_predictions[
        (incorrect_predictions['confidence_tipologia'] > 0.8) |
        (incorrect_predictions['confidence_riferimento'] > 0.8)
    ]
    
    if len(high_conf_errors) > 0:
        print(f"\n   ⚠️  ALERT: {len(high_conf_errors)} errori con alta confidence!")
        print(f"      Questi richiedono analisi approfondita:")
        for idx, row in high_conf_errors.head(3).iterrows():
            print(f"\n      • {row['email_text']}")
            print(f"        Confidence: {row['confidence_tipologia']:.2f}, {row['confidence_riferimento']:.2f}")

# Grafico distribuzione confidence
try:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Tipologia - Corrette
    axes[0, 0].hist(correct_predictions['confidence_tipologia'], bins=20, 
                    color='green', alpha=0.7, edgecolor='black')
    axes[0, 0].set_title('Confidence Tipologia - Predizioni CORRETTE')
    axes[0, 0].set_xlabel('Confidence')
    axes[0, 0].set_ylabel('Frequenza')
    
    # Tipologia - Errate
    if len(incorrect_predictions) > 0:
        axes[0, 1].hist(incorrect_predictions['confidence_tipologia'], bins=20,
                       color='red', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Confidence Tipologia - Predizioni ERRATE')
    axes[0, 1].set_xlabel('Confidence')
    axes[0, 1].set_ylabel('Frequenza')
    
    # Riferimento - Corrette
    axes[1, 0].hist(correct_predictions['confidence_riferimento'], bins=20,
                    color='green', alpha=0.7, edgecolor='black')
    axes[1, 0].set_title('Confidence Riferimento - Predizioni CORRETTE')
    axes[1, 0].set_xlabel('Confidence')
    axes[1, 0].set_ylabel('Frequenza')
    
    # Riferimento - Errate
    if len(incorrect_predictions) > 0:
        axes[1, 1].hist(incorrect_predictions['confidence_riferimento'], bins=20,
                       color='red', alpha=0.7, edgecolor='black')
    axes[1, 1].set_title('Confidence Riferimento - Predizioni ERRATE')
    axes[1, 1].set_xlabel('Confidence')
    axes[1, 1].set_ylabel('Frequenza')
    
    plt.tight_layout()
    
    confidence_plot = f"{CONFIG['export_dir']}/confidence_analysis.png"
    plt.savefig(confidence_plot, dpi=300, bbox_inches='tight')
    print(f"\n💾 Analisi confidence salvata: {confidence_plot}")
    plt.close()
    
except Exception as e:
    print(f"\n⚠️  Grafici confidence non generati: {e}")

# ============================================================================
# STEP 8: ESPERIMENTO 5 - Test su Dataset Completo
# ============================================================================

print("\n" + "=" * 80)
print("STEP 7: Test su Dataset Completo (Campione 500)")
print("=" * 80)

response = input("\nVuoi eseguire test su campione più grande (500 email)? [s/N]: ")

if response.lower() == 's':
    print("\n🚀 Inizio test su campione esteso...")
    
    # Prepara campione più grande
    large_sample_size = 500
    samples_per_cat = large_sample_size // 4
    
    large_sample = []
    for tip in [0, 1]:
        for rif in [0, 1]:
            subset = df[(df['tipologia'] == tip) & 
                       (df['riferimento_temporale'] == rif)].sample(
                           min(samples_per_cat, len(df[(df['tipologia'] == tip) & 
                                                       (df['riferimento_temporale'] == rif)])),
                           random_state=42
                       )
            large_sample.append(subset)
    
    large_df = pd.concat(large_sample).reset_index(drop=True)
    large_emails = large_df['testo'].tolist()
    large_labels = list(zip(large_df['tipologia'], large_df['riferimento_temporale']))
    
    print(f"\n📧 Campione esteso: {len(large_df)} email")
    
    # Classifica con modello migliore
    large_results = classifier.classify_batch(large_emails, large_labels)
    
    # Salva risultati
    large_results_file = f"{CONFIG['export_dir']}/large_sample_results.csv"
    large_results.to_csv(large_results_file, index=False)
    print(f"\n💾 Risultati campione esteso salvati: {large_results_file}")
    
else:
    print("\n⏭️  Saltato test campione esteso")

# ============================================================================
# STEP 9: ESPERIMENTO 6 - Analisi Indicatori Chiave
# ============================================================================

print("\n" + "=" * 80)
print("STEP 8: Analisi Indicatori Chiave Più Frequenti")
print("=" * 80)

# Estrai tutti gli indicatori
all_indicators = []
for indicators in successful['indicatori_chiave']:
    if isinstance(indicators, list):
        all_indicators.extend([ind.lower() for ind in indicators])

# Conta frequenze
from collections import Counter
indicator_counts = Counter(all_indicators)

print(f"\n🔑 Top 20 Indicatori Più Usati dal Modello:")
for indicator, count in indicator_counts.most_common(20):
    print(f"   {indicator:<40} {count:>3} volte")

# Salva indicatori
indicators_df = pd.DataFrame(indicator_counts.most_common(), 
                             columns=['Indicatore', 'Frequenza'])
indicators_file = f"{CONFIG['export_dir']}/key_indicators.csv"
indicators_df.to_csv(indicators_file, index=False)
print(f"\n💾 Indicatori salvati: {indicators_file}")

# ============================================================================
# STEP 10: REPORT FINALE
# ============================================================================

print("\n" + "=" * 80)
print("📋 REPORT FINALE STUDIO")
print("=" * 80)

# Calcola metriche finali
final_accuracy_tip = successful['correct_tipologia'].mean() * 100
final_accuracy_rif = successful['correct_riferimento'].mean() * 100
final_accuracy_both = (successful['correct_tipologia'] & 
                       successful['correct_riferimento']).mean() * 100

avg_latency = successful['latency'].mean()
total_time = successful['latency'].sum()
avg_tokens = successful['tokens_used'].mean()
total_tokens = successful['tokens_used'].sum()

# Stima costo (Groq pricing approssimativo)
estimated_cost_per_1k_tokens = 0.0001  # $0.0001 per 1K tokens (molto basso)
estimated_total_cost = (total_tokens / 1000) * estimated_cost_per_1k_tokens

print(f"\n🎯 METRICHE FINALI:")
print(f"   Modello utilizzato:              {best_model}")
print(f"   Email classificate:              {len(successful)}")
print(f"\n   Accuracy Tipologia:              {final_accuracy_tip:.2f}%")
print(f"   Accuracy Riferimento:            {final_accuracy_rif:.2f}%")
print(f"   Accuracy Entrambe:               {final_accuracy_both:.2f}%")

print(f"\n⚡ PERFORMANCE:")
print(f"   Latenza media:                   {avg_latency:.3f}s")
print(f"   Tempo totale:                    {total_time:.1f}s ({total_time/60:.1f} min)")
print(f"   Throughput:                      {len(successful)/total_time:.1f} email/s")
print(f"   Velocità equivalente:            {len(successful)/total_time*60:.0f} email/ora")

print(f"\n💰 COSTI:")
print(f"   Token totali usati:              {total_tokens:,.0f}")
print(f"   Token medi per email:            {avg_tokens:.0f}")
print(f"   Costo stimato totale:            ${estimated_total_cost:.4f}")
print(f"   Costo per 1000 email:            ${estimated_cost_per_1k_tokens * avg_tokens:.4f}")

print(f"\n📁 FILE GENERATI:")
print(f"   • {comparison_file}")
print(f"   • {errors_file}")
print(f"   • {indicators_file}")
if 'confusion_plot' in locals():
    print(f"   • {confusion_plot}")
if 'confidence_plot' in locals():
    print(f"   • {confidence_plot}")

print(f"\n💡 CONCLUSIONI:")

if final_accuracy_both >= 90:
    print(f"   ✅ Accuracy eccellente ({final_accuracy_both:.1f}%)")
    print(f"   ✅ Modello pronto per produzione")
elif final_accuracy_both >= 80:
    print(f"   ⚠️  Accuracy buona ({final_accuracy_both:.1f}%)")
    print(f"   💡 Considera fine-tuning per migliorare")
else:
    print(f"   ❌ Accuracy insufficiente ({final_accuracy_both:.1f}%)")
    print(f"   💡 Necessario prompt engineering o fine-tuning")

print(f"\n🚀 PROSSIMI PASSI CONSIGLIATI:")
print(f"   1. Analizza errori in {errors_file}")
print(f"   2. Ottimizza system prompt basandoti su indicatori")
print(f"   3. Se accuracy OK → Deploy in produzione")
print(f"   4. Se accuracy bassa → Fine-tuning con Unsloth/LoRA")
print(f"   5. Setup sistema apprendimento continuo")

print("\n" + "=" * 80)
print("✅ STUDIO COMPLETATO!")
print("=" * 80)

# ============================================================================
# STEP 11: GENERAZIONE REPORT HTML (BONUS)
# ============================================================================

print("\n📄 Generazione report HTML...")

html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Report Studio Classificazione Sinistri</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .metric-value {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }}
        .metric-label {{
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #667eea;
            color: white;
        }}
        .success {{ color: #28a745; }}
        .warning {{ color: #ffc107; }}
        .error {{ color: #dc3545; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Report Studio Classificazione Sinistri</h1>
        <p>Analisi con Groq API - {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        <p>Modello: {best_model}</p>
    </div>
    
    <div class="grid">
        <div class="metric-card">
            <div class="metric-value {'success' if final_accuracy_both >= 90 else 'warning' if final_accuracy_both >= 80 else 'error'}">
                {final_accuracy_both:.1f}%
            </div>
            <div class="metric-label">Accuracy Totale</div>
        </div>
        
        <div class="metric-card">
            <div class="metric-value">{len(successful)}</div>
            <div class="metric-label">Email Classificate</div>
        </div>
        
        <div class="metric-card">
            <div class="metric-value">{len(successful)/total_time:.1f}</div>
            <div class="metric-label">Email/Secondo</div>
        </div>
        
        <div class="metric-card">
            <div class="metric-value">${estimated_total_cost:.4f}</div>
            <div class="metric-label">Costo Totale</div>
        </div>
    </div>
    
    <div class="metric-card">
        <h2>📈 Metriche Dettagliate</h2>
        <table>
            <tr>
                <th>Metrica</th>
                <th>Valore</th>
            </tr>
            <tr>
                <td>Accuracy Tipologia</td>
                <td class="{'success' if final_accuracy_tip >= 90 else 'warning'}">{final_accuracy_tip:.2f}%</td>
            </tr>
            <tr>
                <td>Accuracy Riferimento Temporale</td>
                <td class="{'success' if final_accuracy_rif >= 90 else 'warning'}">{final_accuracy_rif:.2f}%</td>
            </tr>
            <tr>
                <td>Latenza Media</td>
                <td>{avg_latency:.3f}s</td>
            </tr>
            <tr>
                <td>Token Medi per Email</td>
                <td>{avg_tokens:.0f}</td>
            </tr>
            <tr>
                <td>Throughput</td>
                <td>{len(successful)/total_time*60:.0f} email/ora</td>
            </tr>
        </table>
    </div>
    
    <div class="metric-card">
        <h2>🔑 Top 10 Indicatori Chiave</h2>
        <table>
            <tr>
                <th>Indicatore</th>
                <th>Frequenza</th>
            </tr>
            {"".join([f"<tr><td>{ind}</td><td>{count}</td></tr>" 
                     for ind, count in indicator_counts.most_common(10)])}
        </table>
    </div>
    
    <div class="metric-card">
        <h2>💡 Conclusioni e Raccomandazioni</h2>
        <ul>
            <li>Il modello <strong>{best_model}</strong> ha raggiunto un'accuracy del <strong>{final_accuracy_both:.1f}%</strong></li>
            <li>Throughput di <strong>{len(successful)/total_time*60:.0f} email/ora</strong> permette elaborazione rapida</li>
            <li>Costo molto contenuto: <strong>${estimated_total_cost:.4f}</strong> per questo test</li>
            {"<li class='success'>✅ Performance eccellente - pronto per produzione</li>" if final_accuracy_both >= 90 else 
             "<li class='warning'>⚠️ Performance buona - considera ottimizzazione</li>" if final_accuracy_both >= 80 else
             "<li class='error'>❌ Performance insufficiente - necessario miglioramento</li>"}
        </ul>
    </div>
</body>
</html>
"""

html_file = f"{CONFIG['export_dir']}/studio_report.html"
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_report)

print(f"✅ Report HTML generato: {html_file}")
print(f"   Apri nel browser per visualizzazione completa")

print("\n" + "=" * 80)
print("🎉 STUDIO COMPLETO TERMINATO CON SUCCESSO!")
print("=" * 80)