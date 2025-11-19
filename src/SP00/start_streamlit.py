#!/usr/bin/env python3
"""
Script di avvio rapido per SP00 Procedural Classifier
Streamlit UI
"""

import sys
import os
from pathlib import Path

# Aggiungi il path per l'import
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir / "procedural_classifier"))

# Verifica .env
env_file = current_dir.parent / '.env'
if not env_file.exists():
    print("⚠️  File .env non trovato!")
    print(f"   Crea {env_file} con:")
    print("   GROQ_API_KEY=your-key-here")
    print()

# Avvia Streamlit
os.system(f"streamlit run {current_dir / 'procedural_classifier' / 'streamlit_procedural_app.py'}")
