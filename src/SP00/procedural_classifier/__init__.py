"""
SP00 - Procedural Classifier Module
Sistema di classificazione procedimenti amministrativi → provvedimenti
"""

__version__ = "1.0.0"
__author__ = "Interzen POC Team"

from .groq_procedural_classifier import ProceduralClassifier, quick_test_classifier
from .procedimenti_dataset import (
    create_procedimenti_dataset,
    get_procedimento_info,
    get_all_procedimenti,
    get_categorie,
    get_tipi_provvedimento
)

__all__ = [
    "ProceduralClassifier",
    "quick_test_classifier",
    "create_procedimenti_dataset",
    "get_procedimento_info",
    "get_all_procedimenti",
    "get_categorie",
    "get_tipi_provvedimento",
]
