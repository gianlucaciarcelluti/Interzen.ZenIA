import PyPDF2
import pdfplumber
import logging
from typing import Dict, List, Optional
from pathlib import Path
from core.models import DocumentReference, DocumentType, FascicoloData

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processore per l'estrazione di contenuto dai documenti"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt']
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Estrae testo da un file PDF usando pdfplumber per maggiore precisione"""
        try:
            text_content = ""
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
            
            logger.info(f"Estratto testo da PDF: {len(text_content)} caratteri")
            return text_content.strip()
        
        except Exception as e:
            logger.error(f"Errore nell'estrazione del testo dal PDF {file_path}: {str(e)}")
            # Fallback con PyPDF2
            return self._extract_with_pypdf2(file_path)
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """Fallback con PyPDF2 per PDF problematici"""
        try:
            text_content = ""
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            
            logger.info(f"Estratto testo con PyPDF2: {len(text_content)} caratteri")
            return text_content.strip()
        
        except Exception as e:
            logger.error(f"Errore anche con PyPDF2 per {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Legge contenuto da file di testo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            logger.info(f"Letto file di testo: {len(content)} caratteri")
            return content.strip()
        
        except UnicodeDecodeError:
            # Prova con encoding diverso
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                logger.info(f"Letto file di testo con encoding latin-1: {len(content)} caratteri")
                return content.strip()
            except Exception as e:
                logger.error(f"Errore nella lettura del file {file_path}: {str(e)}")
                return ""
        
        except Exception as e:
            logger.error(f"Errore nella lettura del file {file_path}: {str(e)}")
            return ""
    
    def process_document(self, file_path: str) -> str:
        """Processa un documento ed estrae il contenuto testuale"""
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"File non trovato: {file_path}")
            return ""
        
        extension = path.suffix.lower()
        
        if extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif extension == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            logger.warning(f"Formato file non supportato: {extension}")
            return ""
    
    def classify_document_type(self, filename: str, content: str) -> DocumentType:
        """Classifica automaticamente il tipo di documento basandosi su nome e contenuto"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Classificazione basata sul nome del file
        if any(keyword in filename_lower for keyword in ['istanza', 'domanda', 'richiesta']):
            return DocumentType.ISTANZA
        
        if any(keyword in filename_lower for keyword in ['identita', 'carta', 'documento']):
            return DocumentType.DOCUMENTO_IDENTITA
        
        if any(keyword in filename_lower for keyword in ['certificat', 'attestat']):
            return DocumentType.CERTIFICAZIONE
        
        if any(keyword in filename_lower for keyword in ['tecnico', 'progett', 'relazion']):
            return DocumentType.ALLEGATO_TECNICO
        
        # Classificazione basata sul contenuto
        if any(keyword in content_lower for keyword in [
            'istanza', 'domanda', 'richiesta', 'chiede', 'sottoscritt'
        ]):
            return DocumentType.ISTANZA
        
        if any(keyword in content_lower for keyword in [
            'progetto', 'tecnico', 'relazione', 'calcol', 'disegn'
        ]):
            return DocumentType.ALLEGATO_TECNICO
        
        if any(keyword in content_lower for keyword in [
            'certifico', 'attesto', 'dichiar'
        ]):
            return DocumentType.CERTIFICAZIONE
        
        # Default
        return DocumentType.COMUNICAZIONE
    
    def analyze_document_content(self, content: str) -> Dict[str, any]:
        """Analizza il contenuto del documento per estrarre informazioni strutturate"""
        analysis = {
            'word_count': len(content.split()),
            'character_count': len(content),
            'has_tables': 'tabella' in content.lower() or '|' in content,
            'has_dates': self._extract_dates(content),
            'has_amounts': self._extract_amounts(content),
            'language': 'italian'  # Assumiamo italiano per ora
        }
        
        return analysis
    
    def _extract_dates(self, content: str) -> List[str]:
        """Estrae date dal contenuto (implementazione base)"""
        import re
        
        # Pattern per date italiane
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # gg/mm/aaaa
            r'\d{1,2}-\d{1,2}-\d{4}',  # gg-mm-aaaa
            r'\d{1,2}\.\d{1,2}\.\d{4}', # gg.mm.aaaa
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, content))
        
        return dates
    
    def _extract_amounts(self, content: str) -> List[str]:
        """Estrae importi monetari dal contenuto"""
        import re
        
        # Pattern per importi in euro
        amount_patterns = [
            r'€\s*\d+(?:[.,]\d+)?',  # €123,45
            r'\d+(?:[.,]\d+)?\s*€',  # 123,45€
            r'\d+(?:[.,]\d+)?\s*euro', # 123,45 euro
        ]
        
        amounts = []
        for pattern in amount_patterns:
            amounts.extend(re.findall(pattern, content, re.IGNORECASE))
        
        return amounts
