import ollama
import time
import tiktoken

# Configurazione
MODEL_NAME = "llama3.2:1b"  # cambia con il modello Ollama che vuoi testare
NUM_RUNS = 5
# Usa 'cl100k_base' o il tokenizer che corrisponde al modello
ENCODING = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    """Conta i token usando tiktoken."""
    return len(ENCODING.encode(text))

def check_ollama_status():
    """Controlla lo stato della connessione con Ollama e mostra i modelli disponibili."""
    print("🔍 Controllo stato Ollama...")
    
    try:
        # Test connessione base
        models = ollama.list()
        print("✅ Connessione con Ollama: OK")
        
        # Mostra modelli disponibili
        if models and 'models' in models:
            print(f"📋 Modelli disponibili ({len(models['models'])}):")
            for model in models['models']:
                name = model.get('name', 'N/A')
                size = model.get('size', 0)
                # Converti dimensione in formato leggibile
                if size > 0:
                    if size > 1e9:
                        size_str = f"{size/1e9:.1f}GB"
                    elif size > 1e6:
                        size_str = f"{size/1e6:.1f}MB"
                    else:
                        size_str = f"{size/1e3:.1f}KB"
                else:
                    size_str = "N/A"
                
                modified = model.get('modified_at', 'N/A')
                if modified != 'N/A':
                    # Formatta la data se disponibile
                    try:
                        from datetime import datetime
                        modified_dt = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                        modified = modified_dt.strftime('%d/%m/%Y %H:%M')
                    except:
                        pass
                
                print(f"  • {name} ({size_str}) - Modificato: {modified}")
        else:
            print("⚠️  Nessun modello trovato")
        
        # Verifica se il modello configurato esiste
        model_names = [m.get('name', '') for m in models.get('models', [])]
        if MODEL_NAME in model_names:
            print(f"✅ Modello configurato '{MODEL_NAME}': Disponibile")
        else:
            print(f"❌ Modello configurato '{MODEL_NAME}': NON trovato!")
            print(f"   Modelli disponibili: {', '.join(model_names)}")
            
    except Exception as e:
        print(f"❌ Errore connessione Ollama: {e}")
        print("   Assicurati che Ollama sia avviato e accessibile")
        return False
    
    print("-" * 50)
    return True

# Prompt di esempio per test differenti
PROMPTS = [
    # Test breve / risposta veloce
    "Cos'è il metaverso? Spiegazione semplice in 2 frasi.",

    # Test descrittivo / lungo
    "Descrivi in dettaglio le cause e le conseguenze della crisi finanziaria del 2008, includendo i principali attori e le misure adottate dai governi.",

    # Test creativo
    "Inventati una fiaba fantasy ambientata in un regno volante dove gli abitanti dominano il cielo con creature alate.",

    # Test tecnico
    "Spiega come funziona il protocollo TLS, inclusi handshake, cifratura, autenticazione, chiavi pubbliche e private.",

    # Test pratico / istruzioni
    "Dammi una guida passo dopo passo per installare e configurare Docker su Ubuntu, partendo da zero."
]

def benchmark_run(model: str, prompt: str) -> tuple[float, int]:
    """Esegue un singolo run che genera output dal modello con stream, restituisce (token/sec, numero_tokens)."""
    start = time.time()
    output_text = ""
    for event in ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        if "message" in event:
            output_text += event["message"]["content"]
    elapsed = time.time() - start
    tokens = count_tokens(output_text)
    if elapsed > 0:
        return tokens / elapsed, tokens
    else:
        return float('inf'), tokens

def benchmark_multiple(model: str, prompts: list[str], runs: int):
    """Esegue NUM_RUNS per ogni prompt, stampa la media e dettagli."""
    results = {}  # prompt -> list di velocità
    for prompt in prompts:
        speeds = []
        token_counts = []
        print(f"\n--- Prompt: {prompt[:60]}{'...' if len(prompt)>60 else ''} ---")
        for i in range(runs):
            speed, tokens = benchmark_run(model, prompt)
            print(f"Run {i+1}/{runs}: {tokens} token in {speed:.2f} tok/s")
            speeds.append(speed)
            token_counts.append(tokens)
        avg_speed = sum(speeds) / len(speeds)
        avg_tokens = sum(token_counts) / len(token_counts)
        results[prompt] = {
            "avg_speed_tok_per_sec": avg_speed,
            "avg_tokens": avg_tokens,
            "runs": runs
        }
        print(f"--> Media: {avg_tokens:.1f} token, {avg_speed:.2f} tok/sec")
    return results

if __name__ == "__main__":
    print("🚀 Speed Test Ollama - Avvio controlli preliminari")
    print("=" * 50)
    
    # Controlla stato Ollama e modelli disponibili
    if not check_ollama_status():
        print("❌ Impossibile procedere: problema con Ollama")
        exit(1)
    
    print(f"🏃 Inizio benchmark modello: {MODEL_NAME}")
    print(f"📊 Configurazione: {NUM_RUNS} run per prompt")
    print("=" * 50)
    
    stats = benchmark_multiple(MODEL_NAME, PROMPTS, NUM_RUNS)
    
    print("\n" + "=" * 50)
    print("🎯 RISULTATI COMPLESSIVI")
    print("=" * 50)
    for prompt, data in stats.items():
        print(f"Prompt: \"{prompt[:50]}{'...' if len(prompt)>50 else ''}\"")
        print(f"    📝 Media token generati: {data['avg_tokens']:.1f}")
        print(f"    ⚡ Velocità media: {data['avg_speed_tok_per_sec']:.2f} token/sec")
        print()
