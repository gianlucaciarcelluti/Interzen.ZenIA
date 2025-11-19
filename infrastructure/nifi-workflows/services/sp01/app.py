"""
SP01 - EML Parser & Email Intelligence Service

Questo microservizio analizza email PEC in arrivo ed estrae metadata e contenuto.
Implementa parsing completo di file .eml, estrazione allegati, validazione PEC,
classificazione intelligente e salvataggio su database.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from email import policy
from email.parser import BytesParser
from email.header import decode_header
import base64
import os
import logging
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
import json
import re
import psycopg
from psycopg.rows import dict_row
import groq
import magic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="SP01 - EML Parser & Email Intelligence",
    description="Servizio per parsing email PEC e estrazione intelligente di metadata",
    version="1.0.0"
)


# Configuration
class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/provvedimenti")
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    ATTACHMENTS_DIR = Path(os.getenv("ATTACHMENTS_DIR", "/tmp/sp01_attachments"))
    MAX_ATTACHMENT_SIZE = int(os.getenv("MAX_ATTACHMENT_SIZE", "50_000_000"))  # 50MB


settings = Settings()
settings.ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)


# Initialize clients
groq_client = groq.Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None


# Models
class EmailParseRequest(BaseModel):
    """Request model for email parsing"""
    eml_content: Optional[str] = None  # Base64 encoded .eml file
    workflow_id: Optional[str] = None  # Optional workflow tracking


class EmailMetadata(BaseModel):
    """Email metadata extracted"""
    from_address: Optional[EmailStr] = None
    to_addresses: List[EmailStr] = []
    cc_addresses: List[EmailStr] = []
    bcc_addresses: List[EmailStr] = []
    subject: Optional[str] = None
    date: Optional[str] = None
    message_id: Optional[str] = None
    in_reply_to: Optional[str] = None
    references: List[str] = []
    priority: Optional[str] = None
    content_type: Optional[str] = None


class AttachmentInfo(BaseModel):
    """Attachment information"""
    filename: str
    content_type: str
    size_bytes: int
    saved_path: Optional[str] = None
    file_hash: Optional[str] = None
    is_signed: bool = False
    signature_valid: Optional[bool] = None


class PECValidation(BaseModel):
    """PEC validation results"""
    is_pec: bool = False
    pec_domain: Optional[str] = None
    signature_present: bool = False
    signature_valid: Optional[bool] = None
    certificate_info: Optional[Dict[str, Any]] = None


class EmailClassification(BaseModel):
    """Email classification results"""
    category: str = "UNKNOWN"
    subcategory: Optional[str] = None
    confidence: float = 0.0
    keywords: List[str] = []
    urgency_level: str = "NORMAL"  # LOW, NORMAL, HIGH, URGENT


class EmailParseResponse(BaseModel):
    """Response model for parsed email"""
    workflow_id: Optional[str] = None
    metadata: EmailMetadata
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    attachments: List[AttachmentInfo] = []
    pec_validation: PECValidation
    classification: EmailClassification
    processing_time_ms: int = 0
    saved_to_db: bool = False
    email_id: Optional[str] = None


# Database functions
def get_db_connection():
    """Get PostgreSQL connection"""
    try:
        conn = psycopg.connect(settings.DATABASE_URL)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise Exception(f"Database connection failed: {str(e)}")


def save_email_to_db(email_data: Dict[str, Any]) -> str:
    """Save email metadata to database"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Insert email record
            cursor.execute("""
                INSERT INTO emails (
                    workflow_id, from_address, to_addresses, cc_addresses, bcc_addresses,
                    subject, email_date, message_id, in_reply_to, references, priority,
                    content_type, body_text, body_html, is_pec, pec_domain,
                    signature_present, signature_valid, category, subcategory,
                    classification_confidence, keywords, urgency_level,
                    attachments_count, processing_time_ms, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                ) RETURNING id
            """, (
                email_data.get('workflow_id'),
                email_data['metadata'].get('from_address'),
                json.dumps(email_data['metadata'].get('to_addresses', [])),
                json.dumps(email_data['metadata'].get('cc_addresses', [])),
                json.dumps(email_data['metadata'].get('bcc_addresses', [])),
                email_data['metadata'].get('subject'),
                email_data['metadata'].get('date'),
                email_data['metadata'].get('message_id'),
                email_data['metadata'].get('in_reply_to'),
                json.dumps(email_data['metadata'].get('references', [])),
                email_data['metadata'].get('priority'),
                email_data['metadata'].get('content_type'),
                email_data.get('body_text'),
                email_data.get('body_html'),
                email_data['pec_validation'].get('is_pec'),
                email_data['pec_validation'].get('pec_domain'),
                email_data['pec_validation'].get('signature_present'),
                email_data['pec_validation'].get('signature_valid'),
                email_data['classification'].get('category'),
                email_data['classification'].get('subcategory'),
                email_data['classification'].get('confidence'),
                json.dumps(email_data['classification'].get('keywords', [])),
                email_data['classification'].get('urgency_level'),
                len(email_data.get('attachments', [])),
                email_data.get('processing_time_ms', 0)
            ))

            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=500, detail="Failed to insert email record")
            email_id = result[0]

            # Insert attachments
            for attachment in email_data.get('attachments', []):
                cursor.execute("""
                    INSERT INTO email_attachments (
                        email_id, filename, content_type, size_bytes,
                        saved_path, file_hash, is_signed, signature_valid, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """, (
                    email_id,
                    attachment.get('filename'),
                    attachment.get('content_type'),
                    attachment.get('size_bytes'),
                    attachment.get('saved_path'),
                    attachment.get('file_hash'),
                    attachment.get('is_signed'),
                    attachment.get('signature_valid')
                ))

            conn.commit()
            logger.info(f"Email saved to database with ID: {email_id}")
            return str(email_id)

    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to save email to database: {e}")
        raise HTTPException(status_code=500, detail=f"Database save failed: {str(e)}")
    finally:
        conn.close()


# Email parsing functions
def decode_header_value(header_value: str) -> str:
    """Decode email header with proper encoding handling"""
    if not header_value:
        return ""

    try:
        decoded_parts = decode_header(header_value)
        decoded_string = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    decoded_string += part.decode(encoding)
                else:
                    decoded_string += part.decode('utf-8', errors='replace')
            else:
                decoded_string += str(part)
        return decoded_string
    except Exception as e:
        logger.warning(f"Header decode failed: {e}, returning raw value")
        return str(header_value)


def extract_email_addresses(header_value: str) -> List[str]:
    """Extract email addresses from header"""
    if not header_value:
        return []

    # Simple regex to extract email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, header_value)
    return list(set(matches))  # Remove duplicates


def parse_email_content(eml_bytes: bytes) -> Dict[str, Any]:
    """Parse email content and extract all information"""
    try:
        # Parse email
        msg = BytesParser(policy=policy.default).parsebytes(eml_bytes)

        # Extract metadata
        metadata = {
            'from_address': extract_email_addresses(decode_header_value(msg.get('From', ''))),
            'to_addresses': extract_email_addresses(decode_header_value(msg.get('To', ''))),
            'cc_addresses': extract_email_addresses(decode_header_value(msg.get('Cc', ''))),
            'bcc_addresses': extract_email_addresses(decode_header_value(msg.get('Bcc', ''))),
            'subject': decode_header_value(msg.get('Subject', '')),
            'date': msg.get('Date'),
            'message_id': msg.get('Message-ID'),
            'in_reply_to': msg.get('In-Reply-To'),
            'references': msg.get('References', '').split() if msg.get('References') else [],
            'priority': msg.get('Priority', msg.get('X-Priority')),
            'content_type': msg.get('Content-Type')
        }

        # Take first from_address if multiple
        metadata['from_address'] = metadata['from_address'][0] if metadata['from_address'] else None

        # Extract body content
        body_text = None
        body_html = None

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition', ''))

                # Skip attachments
                if 'attachment' in content_disposition:
                    continue

                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        if isinstance(payload, bytes):
                            text_content = payload.decode(charset, errors='replace')
                        else:
                            text_content = str(payload)

                        if content_type == 'text/plain' and not body_text:
                            body_text = text_content
                        elif content_type == 'text/html' and not body_html:
                            body_html = text_content
                except Exception as e:
                    logger.warning(f"Failed to decode part: {e}")
                    continue
        else:
            # Single part email
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or 'utf-8'
                    if isinstance(payload, bytes):
                        content = payload.decode(charset, errors='replace')
                    else:
                        content = str(payload)
                    if msg.get_content_type() == 'text/html':
                        body_html = content
                    else:
                        body_text = content
            except Exception as e:
                logger.warning(f"Failed to decode single part: {e}")

        return {
            'metadata': metadata,
            'body_text': body_text,
            'body_html': body_html,
            'raw_msg': msg
        }

    except Exception as e:
        logger.error(f"Email parsing failed: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid email format: {str(e)}")


def extract_attachments(msg, workflow_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Extract attachments from email message"""
    attachments = []

    for part in msg.walk():
        content_disposition = str(part.get('Content-Disposition', ''))

        if 'attachment' in content_disposition:
            try:
                filename = part.get_filename()
                if not filename:
                    continue

                # Decode filename if needed
                filename = decode_header_value(filename)

                # Get content
                content = part.get_payload(decode=True)
                if not content:
                    continue

                # Ensure content is bytes for attachment processing
                if isinstance(content, str):
                    content = content.encode('utf-8')

                # Check size limit
                if len(content) > settings.MAX_ATTACHMENT_SIZE:
                    logger.warning(f"Attachment {filename} too large: {len(content)} bytes")
                    continue

                # Generate file hash
                file_hash = hashlib.sha256(content).hexdigest()

                # Determine content type
                content_type = part.get_content_type()
                if not content_type or content_type == 'application/octet-stream':
                    # Try to detect with magic
                    try:
                        content_type = magic.from_buffer(content, mime=True)
                    except Exception:
                        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

                # Save attachment to filesystem
                safe_filename = "".join(c for c in filename if c.isalnum() or c in '._-').strip()
                if not safe_filename:
                    safe_filename = f"attachment_{len(attachments) + 1}"

                # Create subdirectory structure by workflow_id or date
                if workflow_id:
                    save_dir = settings.ATTACHMENTS_DIR / workflow_id
                else:
                    date_str = datetime.now().strftime("%Y%m%d")
                    save_dir = settings.ATTACHMENTS_DIR / date_str

                save_dir.mkdir(parents=True, exist_ok=True)

                file_path = save_dir / f"{file_hash}_{safe_filename}"
                saved_path = None

                try:
                    # Save file synchronously for now
                    with open(file_path, 'wb') as f:
                        f.write(content)
                    saved_path = str(file_path)

                except Exception as e:
                    logger.error(f"Failed to save attachment {filename}: {e}")
                    continue

                # Check if signed
                is_signed = filename.lower().endswith('.p7m') or content_type in [
                    'application/pkcs7-mime', 'application/x-pkcs7-mime'
                ]

                attachment_info = {
                    'filename': filename,
                    'content_type': content_type,
                    'size_bytes': len(content),
                    'saved_path': saved_path,
                    'file_hash': file_hash,
                    'is_signed': is_signed,
                    'signature_valid': None  # TODO: implement signature validation
                }

                attachments.append(attachment_info)
                logger.info(f"Extracted attachment: {filename} ({len(content)} bytes)")

            except Exception as e:
                logger.warning(f"Failed to process attachment: {e}")
                continue

    return attachments


def validate_pec(msg, from_address: str) -> Dict[str, Any]:
    """Validate PEC email characteristics"""
    pec_validation = {
        'is_pec': False,
        'pec_domain': None,
        'signature_present': False,
        'signature_valid': None,
        'certificate_info': None
    }

    try:
        # Check if from domain is PEC certified
        if from_address and '@' in from_address:
            domain = from_address.split('@')[1].lower()
            pec_domains = [
                'pec.it', 'pec.gov.it', 'cert.legalmail.it',
                'pecmail.com', 'postacertificata.gov.it'
            ]

            # Check for PEC indicators
            subject = msg.get('Subject', '').lower()
            pec_indicators = [
                'posta certificata', 'pec', 'certified mail',
                'posta elettronica certificata'
            ]

            is_pec_domain = any(pec_domain in domain for pec_domain in pec_domains)
            has_pec_subject = any(indicator in subject for indicator in pec_indicators)

            pec_validation['is_pec'] = is_pec_domain or has_pec_subject
            if is_pec_domain:
                pec_validation['pec_domain'] = domain

        # Check for digital signature
        has_signature = False
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type in ['application/pkcs7-signature', 'application/x-pkcs7-signature']:
                has_signature = True
                break

        pec_validation['signature_present'] = has_signature

        # TODO: Implement full signature validation
        if has_signature:
            pec_validation['signature_valid'] = True  # Placeholder

    except Exception as e:
        logger.warning(f"PEC validation failed: {e}")

    return pec_validation


def classify_email(body_text: str, subject: str) -> Dict[str, Any]:
    """Classify email content using AI"""
    classification = {
        'category': 'UNKNOWN',
        'subcategory': None,
        'confidence': 0.0,
        'keywords': [],
        'urgency_level': 'NORMAL'
    }

    try:
        # Combine text for analysis
        full_text = f"Subject: {subject}\n\n{body_text or ''}"

        # Extract keywords
        keywords = []
        admin_keywords = [
            'richiesta', 'autorizzazione', 'permesso', 'licenza', 'concessione',
            'provvedimento', 'determina', 'delibera', 'ordinanza', 'decreto',
            'istanza', 'domanda', 'pratica', 'fascicolo', 'procedimento'
        ]

        for keyword in admin_keywords:
            if keyword.lower() in full_text.lower():
                keywords.append(keyword)

        classification['keywords'] = keywords

        # Basic rule-based classification
        if any(word in full_text.lower() for word in ['autorizzazione', 'licenza', 'concessione']):
            classification.update({
                'category': 'RICHIESTA_AUTORIZZAZIONE',
                'subcategory': 'AUTORIZZAZIONE_ATTIVITA',
                'confidence': 0.8
            })
        elif any(word in full_text.lower() for word in ['scarico', 'acque', 'rifiuti']):
            classification.update({
                'category': 'RICHIESTA_AUTORIZZAZIONE',
                'subcategory': 'AUTORIZZAZIONE_SCARICO',
                'confidence': 0.9
            })
        elif any(word in full_text.lower() for word in ['edilizia', 'costruzione', 'permesso di costruire']):
            classification.update({
                'category': 'RICHIESTA_AUTORIZZAZIONE',
                'subcategory': 'AUTORIZZAZIONE_EDILIZIA',
                'confidence': 0.85
            })
        elif keywords:
            classification.update({
                'category': 'RICHIESTA_AMMINISTRATIVA',
                'confidence': min(0.7, len(keywords) * 0.1)
            })

        # Check urgency
        urgent_keywords = ['urgente', 'immediata', 'tempestiva', 'entro', 'scadenza']
        if any(word in full_text.lower() for word in urgent_keywords):
            classification['urgency_level'] = 'HIGH'

        # Use Groq for advanced classification if available
        if groq_client and len(full_text) > 50:
            try:
                prompt = f"""
                Classifica questa email amministrativa. Rispondi solo con un JSON valido:

                Email:
                {full_text[:1000]}

                Formato risposta JSON:
                {{
                    "categoria": "string",
                    "sottocategoria": "string",
                    "urgenza": "BASSA|NORMALE|ALTA|URGENTE",
                    "confidence": 0.0-1.0
                }}
                """

                response = groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=200
                )

                content = response.choices[0].message.content
                ai_result = json.loads(content.strip() if content else "{}")
                if ai_result.get('categoria'):
                    classification.update({
                        'category': ai_result['categoria'],
                        'subcategory': ai_result.get('sottocategoria'),
                        'urgency_level': ai_result.get('urgenza', 'NORMAL').upper(),
                        'confidence': max(classification['confidence'], ai_result.get('confidence', 0.0))
                    })

            except Exception as e:
                logger.warning(f"Groq classification failed: {e}")

    except Exception as e:
        logger.warning(f"Email classification failed: {e}")

    return classification


# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SP01-EML-Parser",
        "timestamp": datetime.now().isoformat(),
        "attachments_dir": str(settings.ATTACHMENTS_DIR),
        "groq_available": groq_client is not None
    }


@app.post("/parse", response_model=EmailParseResponse)
async def parse_email(request: EmailParseRequest):
    """
    Parse email content and extract metadata, attachments, and intelligence

    Args:
        request: EmailParseRequest with email content

    Returns:
        EmailParseResponse with extracted metadata
    """
    start_time = datetime.now()

    try:
        logger.info(f"Starting email parsing for workflow: {request.workflow_id}")

        if not request.eml_content:
            raise HTTPException(status_code=400, detail="eml_content is required")

        # Decode base64 if needed
        try:
            eml_bytes = base64.b64decode(request.eml_content)
        except Exception:
            # Assume it's raw email content
            eml_bytes = request.eml_content.encode('utf-8')

        # Parse email content
        parsed_data = parse_email_content(eml_bytes)
        msg = parsed_data['raw_msg']

        # Extract attachments
        attachments = extract_attachments(msg, request.workflow_id)
        logger.info(f"Extracted {len(attachments)} attachments")

        # Validate PEC
        pec_validation = validate_pec(msg, parsed_data['metadata']['from_address'])

        # Classify email
        classification = classify_email(
            parsed_data['body_text'],
            parsed_data['metadata']['subject']
        )

        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

        # Prepare response
        response_data = {
            'workflow_id': request.workflow_id,
            'metadata': EmailMetadata(**parsed_data['metadata']),
            'body_text': parsed_data['body_text'],
            'body_html': parsed_data['body_html'],
            'attachments': [AttachmentInfo(**att) for att in attachments],
            'pec_validation': PECValidation(**pec_validation),
            'classification': EmailClassification(**classification),
            'processing_time_ms': processing_time,
            'saved_to_db': False,
            'email_id': None
        }

        # Save to database
        try:
            email_id = save_email_to_db(response_data)
            response_data['saved_to_db'] = True
            response_data['email_id'] = email_id
            logger.info(f"Email saved to database with ID: {email_id}")
        except Exception as e:
            logger.error(f"Database save failed: {e}")
            # Continue without failing the request

        logger.info(f"Email parsing completed in {processing_time}ms")
        return EmailParseResponse(**response_data)

    except HTTPException:
        raise
    except Exception as e:
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.error(f"Email parsing failed after {processing_time}ms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Email parsing failed: {str(e)}")


@app.post("/parse-file", response_model=EmailParseResponse)
async def parse_email_file(
    file: UploadFile = File(...),
    workflow_id: Optional[str] = Form(None)
):
    """
    Parse uploaded .eml file directly

    Args:
        file: Uploaded .eml file
        workflow_id: Optional workflow tracking ID

    Returns:
        EmailParseResponse with extracted metadata
    """
    try:
        logger.info(f"Parsing uploaded file: {file.filename}")

        # Read file content
        content = await file.read()

        # Create request object
        request = EmailParseRequest(
            eml_content=base64.b64encode(content).decode('utf-8'),
            workflow_id=workflow_id
        )

        # Use existing parse endpoint
        return await parse_email(request)

    except Exception as e:
        logger.error(f"File parsing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File parsing failed: {str(e)}")


@app.get("/attachments/{email_id}")
async def get_email_attachments(email_id: str):
    """Get attachments for a specific email"""
    try:
        conn = get_db_connection()
        try:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT filename, content_type, size_bytes, saved_path, file_hash,
                           is_signed, signature_valid, created_at
                    FROM email_attachments
                    WHERE email_id = %s
                    ORDER BY created_at
                """, (email_id,))

                attachments = cursor.fetchall()
                return {"email_id": email_id, "attachments": attachments}

        finally:
            conn.close()

    except Exception as e:
        logger.error(f"Failed to get attachments: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "SP01 - EML Parser & Email Intelligence",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "parse": "POST /parse",
            "parse-file": "POST /parse-file",
            "attachments": "GET /attachments/{email_id}",
            "health": "GET /health",
            "docs": "GET /docs"
        },
        "capabilities": [
            "EML file parsing",
            "Metadata extraction",
            "Attachment extraction and storage",
            "PEC validation",
            "AI-powered email classification",
            "PostgreSQL persistence",
            "Async processing"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
