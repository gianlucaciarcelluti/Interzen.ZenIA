"""
Test rapido della funzione get_available_models
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carica .env dalla root
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent.parent
env_file = root_dir / '.env'

if env_file.exists():
    load_dotenv(env_file)

# Import dopo aver caricato .env
import requests
import streamlit as st

# Copia la funzione qui per testarla
def get_available_models(api_key=None):
    """
    Recupera i modelli disponibili dall'API Groq
    """
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "")
    
    if not api_key:
        return {
            "llama-3.1-8b-instant": "Llama 3.1 8B Instant",
            "llama-3.3-70b-versatile": "🚀 Llama 3.3 70B Versatile (Potente)",
            "gemma2-9b-it": "💎 Gemma 2 9B IT"
        }
    
    try:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            models = {}
            
            exclude_keywords = ['whisper', 'tts', 'guard', 'prompt-guard']
            
            for model in data.get('data', []):
                model_id = model.get('id', '')
                
                if any(keyword in model_id.lower() for keyword in exclude_keywords):
                    continue
                
                display_name = model_id
                
                if 'llama-3.1-8b-instant' in model_id:
                    display_name = "⚡ Llama 3.1 8B Instant (Veloce)"
                elif 'llama-3.3-70b' in model_id:
                    display_name = "🚀 Llama 3.3 70B Versatile (Potente)"
                elif 'llama-4-maverick' in model_id:
                    display_name = "🎯 Llama 4 Maverick 17B"
                elif 'llama-4-scout' in model_id:
                    display_name = "🔍 Llama 4 Scout 17B"
                elif 'deepseek-r1' in model_id:
                    display_name = "🧠 DeepSeek R1 Distill 70B"
                elif 'gemma2-9b' in model_id:
                    display_name = "💎 Gemma 2 9B IT"
                elif 'compound-mini' in model_id:
                    display_name = "⚡ Groq Compound Mini"
                elif 'compound' in model_id and 'mini' not in model_id:
                    display_name = "🔥 Groq Compound"
                elif 'kimi-k2' in model_id:
                    display_name = "🌙 Kimi K2 Instruct"
                elif 'gpt-oss' in model_id:
                    display_name = f"🤖 GPT OSS {model_id.split('-')[-1].upper()}"
                elif 'qwen3' in model_id:
                    display_name = "🇨🇳 Qwen3 32B"
                elif 'allam' in model_id:
                    display_name = "🌍 Allam 2 7B"
                
                models[model_id] = display_name
            
            if models:
                return models
        
    except Exception as e:
        print(f"⚠️ Errore nel recupero modelli: {e}")
    
    return {
        "llama-3.1-8b-instant": "⚡ Llama 3.1 8B Instant (Veloce)",
        "llama-3.3-70b-versatile": "🚀 Llama 3.3 70B Versatile (Potente)",
        "gemma2-9b-it": "💎 Gemma 2 9B IT"
    }


# Test
print("=" * 80)
print("TEST GET_AVAILABLE_MODELS")
print("=" * 80)

api_key = os.environ.get("GROQ_API_KEY", "")
print(f"\n🔑 API Key presente: {'✅' if api_key else '❌'}")

models = get_available_models(api_key)

print(f"\n📊 Modelli disponibili: {len(models)}\n")
print("-" * 80)

for model_id, display_name in models.items():
    print(f"{display_name:<50} | {model_id}")

print("-" * 80)

# Verifica il default
default_model = "llama-3.1-8b-instant"
if default_model in models:
    print(f"\n✅ Default model '{default_model}' trovato!")
    print(f"   Nome: {models[default_model]}")
else:
    print(f"\n❌ Default model '{default_model}' NON trovato!")
    print(f"   Primo modello disponibile: {list(models.keys())[0]}")

print("\n" + "=" * 80)
