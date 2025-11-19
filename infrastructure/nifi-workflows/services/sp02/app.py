"""
SP02 - Document Extractor & Attachment Classifier Service

Questo microservizio estrae testo da allegati (PDF, immagini, DOC) e classifica i documenti.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import logging
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SP02 - Document Extractor & Attachment Classifier",
    description="Servizio per estrazione testo da documenti e classificazione allegati",
    version="1.0.0"
)

# Models
class DocumentClassification(BaseModel):
    """Document classification result"""
    document_type: str
    confidence: float
    category: Optional[str] = None
    
class ExtractedData(BaseModel):
    """Structured data extracted from document"""
    dates: List[str] = []
    amounts: List[float] = []
    names: List[str] = []
    codes: List[str] = []
    references: List[str] = []
    
class DocumentExtractResponse(BaseModel):
    """Response model for document extraction"""
    filename: str
    content_type: str
    text_content: str
    classification: DocumentClassification
    extracted_data: ExtractedData
    page_count: Optional[int] = None
    word_count: int = 0
    ocr_applied: bool = False

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SP02-Document-Extractor"}

# Main endpoint
@app.post("/extract", response_model=DocumentExtractResponse)
async def extract_document(file: UploadFile = File(...)):
    """
    Extract text and metadata from document
    
    Args:
        file: Uploaded document (PDF, DOC, images)
        
    Returns:
        DocumentExtractResponse with extracted content
    """
    try:
        logger.info(f"Processing file: {file.filename}")
        
        # Read file content
        content = await file.read()
        
        # TODO: Implementare estrazione reale
        # - PDF: PyPDF2 o pdfplumber
        # - Immagini: Tesseract OCR
        # - DOC/DOCX: python-docx
        
        # Placeholder response
        response = DocumentExtractResponse(
            filename=file.filename,
            content_type=file.content_type or "unknown",
            text_content="Testo estratto dal documento...",
            classification=DocumentClassification(
                document_type="PLANIMETRIA_TECNICA",
                confidence=0.88,
                category="TECNICO"
            ),
            extracted_data=ExtractedData(
                dates=["2025-11-03"],
                amounts=[150000.00],
                names=["Ing. Mario Rossi"],
                codes=["CIG123456"],
                references=["L. 241/1990"]
            ),
            page_count=5,
            word_count=1234,
            ocr_applied=False
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error extracting document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document extraction failed: {str(e)}")

@app.post("/classify")
async def classify_document(file: UploadFile = File(...)):
    """
    Classify document type without full extraction
    
    Args:
        file: Uploaded document
        
    Returns:
        Document classification
    """
    try:
        logger.info(f"Classifying file: {file.filename}")
        
        # TODO: Implementare classificazione rapida
        
        return {
            "filename": file.filename,
            "classification": {
                "document_type": "RELAZIONE_TECNICA",
                "confidence": 0.92,
                "category": "TECNICO"
            }
        }
        
    except Exception as e:
        logger.error(f"Error classifying document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "SP02 - Document Extractor & Attachment Classifier",
        "status": "running",
        "version": "1.0.0",
        "supported_formats": ["PDF", "DOC", "DOCX", "JPG", "PNG", "TIFF"],
        "endpoints": {
            "extract": "/extract",
            "classify": "/classify",
            "health": "/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
