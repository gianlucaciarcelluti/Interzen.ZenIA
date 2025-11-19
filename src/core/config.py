import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()


class Config:
    """Configurazione centralizzata dell'applicazione"""
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    
    # MCP Server Configuration
    MCP_SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "3001"))
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Streamlit Configuration
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", "8501"))
    
    # Paths
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./outputs")
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "./templates")
    
    # Limits
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    MAX_PROCESSING_TIME_SECONDS: int = int(os.getenv("MAX_PROCESSING_TIME_SECONDS", "300"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def setup_logging(cls) -> None:
        """Configura il logging per l'applicazione"""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('app.log', encoding='utf-8')
            ]
        )
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Assicura che le directory necessarie esistano"""
        directories = [cls.UPLOAD_DIR, cls.OUTPUT_DIR, cls.TEMPLATES_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# Istanza globale della configurazione
config = Config()
