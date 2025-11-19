#!/usr/bin/env python3
"""
POC Streamlit: Email (.eml) → HITL Checkpoint
Interfaccia interattiva per testare il workflow completo Ingress → SP01 → HITL
"""

import streamlit as st
import requests
import time
from datetime import datetime
from pathlib import Path
import email
from email import policy
import base64
import psycopg2
from psycopg2.extras import RealDictCursor
import json

# Configurazione
INGRESS_ENDPOINT = "http://localhost:9099/contentListener/fascicolo"
SP01_HEALTH = "http://localhost:5001/health"
HITL_HEALTH = "http://localhost:5009/health"

# Database Audit Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'nifi_audit',
    'user': 'nifi',
    'password': 'nifi_password'
}


def get_db_connection():
    """Get database connection to nifi_audit"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"❌ Errore connessione database: {e}")
        return None


def track_workflow_execution(execution_id: str, max_wait: int = 30) -> dict:
    """
    Track workflow execution by polling the audit database.
    Returns the workflow status and results.
    """
    workflow_steps = {
        'Ingress': {'order': 1, 'status': 'pending', 'duration_ms': None},
        'SP01_Parse': {'order': 2, 'status': 'pending', 'duration_ms': None},
        'SP01_Classify': {'order': 3, 'status': 'pending', 'duration_ms': None},
        'HITL_Review': {'order': 4, 'status': 'pending', 'duration_ms': None}
    }
    
    conn = get_db_connection()
    if not conn:
        return {'steps': workflow_steps, 'completed': False, 'error': 'DB connection failed'}
    
    start_time = time.time()
    completed = False
    final_result = None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            while (time.time() - start_time) < max_wait and not completed:
                # Query workflow executions
                cursor.execute("""
                    SELECT 
                        workflow_name,
                        step_name,
                        status,
                        duration_ms,
                        output_data,
                        error_message,
                        completed_at
                    FROM workflow_executions
                    WHERE execution_id = %s
                    ORDER BY started_at DESC
                """, (execution_id,))
                
                executions = cursor.fetchall()
                
                # Update workflow steps based on executions
                for exec_row in executions:
                    workflow_name = exec_row['workflow_name']
                    step_name = exec_row['step_name']
                    status = exec_row['status']
                    
                    # Map to our workflow steps
                    if 'Ingress' in workflow_name or 'HTTP' in step_name:
                        workflow_steps['Ingress']['status'] = status.lower()
                        workflow_steps['Ingress']['duration_ms'] = exec_row['duration_ms']
                    
                    elif workflow_name == 'SP01_EML_Parser':
                        if 'Parse' in step_name or 'Call_Microservice' in step_name:
                            workflow_steps['SP01_Parse']['status'] = status.lower()
                            workflow_steps['SP01_Parse']['duration_ms'] = exec_row['duration_ms']
                            
                            # Extract classification result
                            if exec_row['output_data'] and status == 'SUCCESS':
                                final_result = exec_row['output_data']
                        
                        elif 'Classif' in step_name:
                            workflow_steps['SP01_Classify']['status'] = status.lower()
                            workflow_steps['SP01_Classify']['duration_ms'] = exec_row['duration_ms']
                    
                    elif 'HITL' in workflow_name or 'SP11' in workflow_name:
                        workflow_steps['HITL_Review']['status'] = status.lower()
                        workflow_steps['HITL_Review']['duration_ms'] = exec_row['duration_ms']
                
                # Check if workflow is completed
                all_completed = all(
                    step['status'] in ['success', 'failed'] 
                    for step in workflow_steps.values()
                )
                
                has_failure = any(
                    step['status'] == 'failed'
                    for step in workflow_steps.values()
                )
                
                if all_completed or has_failure:
                    completed = True
                    break
                
                time.sleep(1)  # Poll every second
        
    except Exception as e:
        st.error(f"❌ Errore tracking workflow: {e}")
        return {'steps': workflow_steps, 'completed': False, 'error': str(e)}
    
    finally:
        conn.close()
    
    return {
        'steps': workflow_steps,
        'completed': completed,
        'result': final_result,
        'elapsed_time': time.time() - start_time
    }


def display_workflow_progress(workflow_status: dict):
    """Display workflow progress with improved UX"""
    steps = workflow_status['steps']
    
    st.markdown("---")
    st.markdown("### 📊 Stato Elaborazione")
    
    # Calculate overall progress
    total_steps = len(steps)
    completed_steps = sum(1 for step in steps.values() if step['status'] in ['success', 'failed'])
    progress = completed_steps / total_steps
    
    # Display progress bar with percentage
    st.progress(progress)
    st.caption(f"Completato: {int(progress * 100)}% ({completed_steps}/{total_steps} fasi)")
    
    # Display step details in a more readable way
    step_labels = {
        'Ingress': '📥 Ricezione Email',
        'SP01_Parse': '📄 Analisi Contenuto',
        'SP01_Classify': '🤖 Classificazione AI',
        'HITL_Review': '👤 Revisione Umana'
    }
    
    st.markdown("#### Dettaglio Fasi:")
    
    for step_name, step_data in sorted(steps.items(), key=lambda x: x[1]['order']):
        status = step_data['status']
        label = step_labels.get(step_name, step_name)
        
        # Create a nice status display
        if status == 'success':
            st.success(f"✅ **{label}** - Completato con successo")
            if step_data['duration_ms']:
                st.caption(f"   ⏱️ Tempo impiegato: {step_data['duration_ms']}ms")
        elif status == 'failed':
            st.error(f"❌ **{label}** - Fallito")
            if step_data.get('error_message'):
                st.caption(f"   ⚠️ Errore: {step_data['error_message']}")
        elif status == 'running':
            st.warning(f"⏳ **{label}** - In esecuzione...")
        else:
            st.info(f"⏸️ **{label}** - In attesa")


def display_classification_result(result_data: dict):
    """Display classification result with clear HITL options"""
    if not result_data:
        st.info("⏳ In attesa del risultato della classificazione...")
        return
    
    st.markdown("---")
    st.markdown("### � Risultato Analisi Documento")
    
    # Create a nice card-like display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Main classification result
        if 'tipologia_provvedimento' in result_data:
            st.success(f"### 📄 {result_data['tipologia_provvedimento']}")
        else:
            st.warning("⚠️ Tipologia non identificata")
    
    with col2:
        # Confidence score
        if 'classification_confidence' in result_data:
            confidence = result_data.get('classification_confidence', 0)
            if isinstance(confidence, (int, float)):
                st.metric(
                    label="🎯 Affidabilità",
                    value=f"{confidence * 100:.0f}%",
                    delta="Alta" if confidence > 0.8 else "Media" if confidence > 0.6 else "Bassa"
                )
    
    # Additional info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'attachments_extracted' in result_data:
            st.metric("📎 Allegati", result_data['attachments_extracted'])
    
    with col2:
        if 'groq_model' in result_data:
            st.caption(f"🤖 Modello: {result_data['groq_model']}")
    
    with col3:
        if 'processing_time_ms' in result_data:
            st.caption(f"⏱️ Tempo: {result_data['processing_time_ms']}ms")
    
    # Full result in expander
    with st.expander("🔍 Visualizza Dettagli Completi JSON"):
        st.json(result_data)
    
    st.markdown("---")


def display_hitl_checkpoint(result_data: dict):
    """Display HITL checkpoint with clear approval/rejection options"""
    st.markdown("---")
    st.markdown("## 🛡️ CHECKPOINT - Conferma Risultato")
    
    st.info("""
    **👤 Intervento Richiesto**
    
    Sei a un punto di controllo umano (HITL - Human In The Loop).
    
    Rivedi il risultato della classificazione e conferma se è corretto oppure rigettalo per richiedere una revisione manuale.
    """)
    
    # Create two clear options with descriptions
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("### ✅ Approva")
        st.caption("Il risultato è corretto")
        approve_btn = st.button(
            "✅ APPROVA E CONTINUA",
            type="primary",
            use_container_width=True,
            key="approve_hitl"
        )
        
        if approve_btn:
            st.success("✅ **Risultato approvato!**")
            st.info("Il workflow continuerà con la generazione del provvedimento...")
            st.balloons()
            
            # Here you would call the next workflow step
            st.code("""
# Prossimo step: Generazione Provvedimento
POST /api/workflow/generate-document
{
  "execution_id": "...",
  "tipologia": "Autorizzazione Scarico Acque",
  "approved_by": "user",
  "approved_at": "2025-11-04T10:30:00Z"
}
            """, language="json")
    
    with col2:
        st.markdown("### ❌ Rigetta")
        st.caption("Il risultato non è corretto")
        reject_btn = st.button(
            "❌ RIGETTA E RIVEDI",
            type="secondary",
            use_container_width=True,
            key="reject_hitl"
        )
        
        if reject_btn:
            st.error("❌ **Risultato rigettato**")
            st.warning("Il caso verrà inoltrato per revisione manuale.")
            
            # Show manual review form
            st.markdown("#### 📝 Motivo del rigetto:")
            rejection_reason = st.text_area(
                "Spiega perché il risultato non è corretto",
                placeholder="Es: La tipologia identificata non corrisponde al contenuto della richiesta...",
                key="rejection_reason"
            )
            
            if st.button("📨 Invia per Revisione", type="primary", key="submit_rejection"):
                if rejection_reason:
                    st.success("✅ Feedback inviato! Un operatore revisionerà il caso.")
                else:
                    st.warning("⚠️ Inserisci un motivo per il rigetto")
    
    with col3:
        st.markdown("### ✏️ Modifica")
        st.caption("Correggi il risultato")
        modify_btn = st.button(
            "✏️ MODIFICA MANUALMENTE",
            use_container_width=True,
            key="modify_hitl"
        )
        
        if modify_btn:
            st.info("📝 **Modalità Modifica Attivata**")
            
            # Show editable form
            st.markdown("#### Modifica i campi:")
            
            new_tipologia = st.text_input(
                "Tipologia Provvedimento",
                value=result_data.get('tipologia_provvedimento', ''),
                key="edit_tipologia"
            )
            
            new_confidence = st.slider(
                "Affidabilità (dopo correzione)",
                0.0, 1.0, 1.0,  # Max confidence after human correction
                key="edit_confidence"
            )
            
            if st.button("💾 Salva Modifiche", type="primary", key="save_modifications"):
                st.success(f"✅ Modifiche salvate! Nuova tipologia: **{new_tipologia}**")
                st.info("Il workflow continuerà con i dati corretti...")




def parse_eml_file(eml_content: str) -> dict:
    """Parse .eml file and extract metadata + attachments."""
    from email import message_from_string, policy

    msg = message_from_string(eml_content, policy=policy.default)

    # Extract basic headers
    from_addr = msg.get('From', '')
    to_addr = msg.get('To', '')
    subject = msg.get('Subject', '')

    # Extract body and attachments
    body_text = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get('Content-Disposition', ''))

            # Extract text body
            if content_type == 'text/plain' and 'attachment' not in disposition:
                try:
                    # Use get_content() instead of get_payload().decode()
                    body_text = part.get_content()
                except Exception:
                    pass

            # Extract attachments
            elif 'attachment' in disposition or content_type.startswith('application/'):
                filename = part.get_filename()
                if filename:
                    try:
                        payload = part.get_payload(decode=True)
                        if payload and isinstance(payload, bytes):
                            attachments.append({
                                'filename': filename,
                                'content_type': content_type,
                                'size_kb': len(payload) / 1024
                            })
                    except Exception:
                        pass
    else:
        # Single part message
        try:
            # Use get_content() for text content
            body_text = msg.get_content()
        except Exception:
            # Fallback to string payload
            body_text = str(msg.get_payload())

    return {
        'from': from_addr,
        'to': to_addr,
        'subject': subject,
        'body': body_text.strip() if body_text else "",
        'attachments': attachments
    }

def check_services_health():
    """Verifica lo stato dei servizi"""
    services = {
        "SP01 Parser": SP01_HEALTH,
        "HITL Manager": HITL_HEALTH
    }

    results = {}
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                results[name] = {"status": "✅ Healthy", "data": response.json()}
            else:
                results[name] = {"status": "⚠️ Warning", "data": None}
        except Exception as e:
            results[name] = {"status": "❌ Offline", "data": str(e)}

    return results

def send_email_to_workflow(eml_content):
    """Invia l'email al workflow NiFi e restituisce execution_id"""
    import uuid
    
    # Generate unique execution ID
    execution_id = str(uuid.uuid4())
    
    try:
        response = requests.post(
            INGRESS_ENDPOINT,
            headers={
                "Content-Type": "message/rfc822",
                "X-Execution-ID": execution_id  # Pass execution ID to NiFi
            },
            data=eml_content.encode('utf-8'),
            timeout=10
        )
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response": response.text[:500],  # Primi 500 caratteri
            "execution_id": execution_id
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "response": str(e),
            "execution_id": execution_id
        }

# Configurazione pagina Streamlit
st.set_page_config(
    page_title="POC: Email → HITL Workflow",
    page_icon="📧",
    layout="wide"
)

# Header
st.title("📧 POC: Email (.eml) → HITL Checkpoint")
st.markdown("### Workflow Completo: Ingress → SP01 → HITL")

# Sidebar - Stato Servizi
with st.sidebar:
    st.header("🔍 Stato Servizi")

    if st.button("🔄 Aggiorna Stato", use_container_width=True):
        st.rerun()

    services_status = check_services_health()

    for service_name, status_data in services_status.items():
        with st.expander(f"{status_data['status']} {service_name}"):
            if status_data['data']:
                st.json(status_data['data'])
            else:
                st.warning("Servizio non disponibile")

    st.markdown("---")
    st.markdown("### 📊 Endpoints")
    st.code(f"Ingress: {INGRESS_ENDPOINT}", language="text")
    st.code(f"SP01: {SP01_HEALTH}", language="text")
    st.code(f"HITL: {HITL_HEALTH}", language="text")

# Main content - Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📧 Invio Email", 
    "📝 Email Personalizzata", 
    "📊 Workflow Info",
    "🧪 Test HITL UI"
])

with tab1:
    st.header("📧 Esempi Email Preconfigurate")
    st.markdown("Seleziona un esempio di email e invialo al workflow per testare l'elaborazione completa.")

    # Opzione per caricare .eml da file
    st.markdown("### 📁 Carica un file .eml")

    # Path agli esempi preconfigurati
    examples_dir = Path(__file__).parent.parent.parent / "examples" / "eml-samples"

    # Inizializza variabili
    selected_eml_content = None
    selected_filename = None

    col_upload1, col_upload2 = st.columns([3, 1])

    with col_upload1:
        # Mostra file .eml disponibili
        if examples_dir.exists():
            eml_files = sorted(examples_dir.glob("*.eml"))
            if eml_files:
                selected_file = st.selectbox(
                    "File .eml preconfigurati con allegati PDF:",
                    options=[f.name for f in eml_files],
                    index=0
                )

                if selected_file:
                    selected_path = examples_dir / selected_file

                    # Leggi e parse l'.eml
                    with open(selected_path, 'r', encoding='utf-8') as f:
                        selected_eml_content = f.read()
                        selected_filename = selected_file

                    try:
                        parsed_email = parse_eml_file(selected_eml_content)

                        # Display info email
                        st.text_input("Da:", value=parsed_email['from'], disabled=True)
                        st.text_input("A:", value=parsed_email['to'], disabled=True)
                        st.text_input("Oggetto:", value=parsed_email['subject'], disabled=True)

                        # Info allegati
                        if parsed_email['attachments']:
                            st.info(f"📎 **{len(parsed_email['attachments'])} allegato/i:**")
                            for att in parsed_email['attachments']:
                                st.markdown(f"  - `{att['filename']}` ({att['size_kb']:.1f} KB) - {att['content_type']}")

                        st.text_area("Corpo:", value=parsed_email['body'], height=250, disabled=True)

                    except Exception as e:
                        st.error(f"Errore parsing .eml: {str(e)}")
                        eml_content_preview = selected_eml_content[:500] + "..." if len(selected_eml_content) > 500 else selected_eml_content
                        st.code(eml_content_preview, language="text")

    with col_upload2:
        st.markdown("### 📊 Azioni")

        # Controlla se c'è contenuto disponibile per l'invio
        can_send = selected_eml_content is not None

        if st.button("🚀 Invia", type="primary", use_container_width=True, disabled=not can_send):
            if not can_send:
                st.warning("⚠️ Seleziona prima un file .eml")
            else:
                # Send email
                with st.spinner("📤 Invio email in corso..."):
                    result = send_email_to_workflow(selected_eml_content)

                if result['success']:
                    st.success("✅ Email inviata con successo!")
                    
                    # Get execution ID
                    execution_id = result.get('execution_id')
                    
                    if execution_id:
                        st.info(f"🔍 **Execution ID:** `{execution_id}`")
                        
                        # Track workflow execution
                        st.markdown("---")
                        st.subheader("📊 Avanzamento Workflow")
                        
                        # Progress container
                        progress_container = st.empty()
                        status_container = st.empty()
                        result_container = st.empty()
                        
                        with st.spinner("⏳ Elaborazione in corso..."):
                            workflow_status = track_workflow_execution(execution_id, max_wait=30)
                        
                        # Display final progress
                        with progress_container:
                            display_workflow_progress(workflow_status)
                        
                        # Display results
                        if workflow_status.get('completed'):
                            with status_container:
                                st.success(f"✅ Workflow completato in {workflow_status['elapsed_time']:.1f}s")
                            
                            # Display classification result
                            if workflow_status.get('result'):
                                with result_container:
                                    display_classification_result(workflow_status['result'])
                                    display_hitl_checkpoint(workflow_status['result'])
                            else:
                                with result_container:
                                    st.warning("⚠️ Nessun risultato di classificazione disponibile")
                        else:
                            with status_container:
                                st.warning("⏱️ Workflow non completato nel tempo limite")
                    
                    with st.expander("📋 Dettagli Risposta HTTP"):
                        st.write(f"**Status Code:** {result['status_code']}")
                        st.code(result['response'][:200], language="text")
                else:
                    st.error(f"❌ Errore invio: {result['status_code']}")
                    st.code(result['response'], language="text")

        if st.button("💾 Download", use_container_width=True, disabled=not can_send):
            if can_send and selected_filename:
                st.download_button(
                    label="📥 Scarica .eml",
                    data=selected_eml_content,
                    file_name=selected_filename,
                    mime="message/rfc822",
                    use_container_width=True
                )

    st.markdown("---")

    # Oppure carica file personalizzato
    st.markdown("### 📤 Oppure carica il tuo file .eml")
    uploaded_file = st.file_uploader("Scegli un file .eml", type=['eml'])

    if uploaded_file:
        custom_eml_content = uploaded_file.read().decode('utf-8')

        col1, col2 = st.columns([3, 1])

        with col1:
            try:
                parsed = parse_eml_file(custom_eml_content)
                st.text_input("Da:", value=parsed['from'], disabled=True, key="custom_from")
                st.text_input("A:", value=parsed['to'], disabled=True, key="custom_to")
                st.text_input("Oggetto:", value=parsed['subject'], disabled=True, key="custom_subject")

                if parsed['attachments']:
                    st.success(f"📎 {len(parsed['attachments'])} allegato/i trovato/i")
                    for att in parsed['attachments']:
                        st.write(f"  - {att['filename']} ({att['size_kb']:.1f} KB)")

                st.text_area("Corpo:", value=parsed['body'], height=200, disabled=True, key="custom_body")
            except Exception as e:
                st.warning(f"⚠️ Parsing limitato: {str(e)}")
                st.code(custom_eml_content[:300], language="text")

        with col2:
            if st.button("🚀 Invia File", type="primary", use_container_width=True, key="send_custom"):
                with st.spinner("📤 Invio..."):
                    result = send_email_to_workflow(custom_eml_content)

                if result['success']:
                    st.success("✅ Email inviata!")
                    
                    execution_id = result.get('execution_id')
                    if execution_id:
                        st.info(f"🔍 **Execution ID:** `{execution_id}`")
                        
                        with st.spinner("⏳ Elaborazione..."):
                            workflow_status = track_workflow_execution(execution_id, max_wait=30)
                        
                        display_workflow_progress(workflow_status)
                        
                        if workflow_status.get('completed'):
                            if workflow_status.get('result'):
                                display_classification_result(workflow_status['result'])
                                display_hitl_checkpoint(workflow_status['result'])
                            else:
                                st.warning("⚠️ Nessun risultato di classificazione disponibile")
                else:
                    st.error(f"❌ Errore {result['status_code']}")

with tab2:
    st.header("📝 Crea Email Personalizzata")
    st.markdown("Componi una tua email personalizzata da inviare al workflow.")

    with st.form("custom_email_form"):
        custom_from = st.text_input("Da:", value="test@pec.esempio.it")
        custom_to = st.text_input("A:", value="ufficio@comune.esempio.it")
        custom_subject = st.text_input("Oggetto:", value="Test Email Personalizzata")
        custom_body = st.text_area("Corpo del messaggio:", height=400, value="Inserisci qui il testo della tua email...")

        submit = st.form_submit_button("🚀 Invia Email Personalizzata", type="primary", use_container_width=True)

        if submit:
            if custom_from and custom_to and custom_subject and custom_body:
                # Create .eml content manually
                timestamp = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0100")
                message_id = f"<{int(time.time())}@esempio.it>"

                eml_content = f"""From: {custom_from}
To: {custom_to}
Subject: {custom_subject}
Date: {timestamp}
Message-ID: {message_id}
Content-Type: text/plain; charset=utf-8

{custom_body}
"""

                with st.spinner("📤 Invio email personalizzata..."):
                    result = send_email_to_workflow(eml_content)

                if result['success']:
                    st.success("✅ Email personalizzata inviata!")
                    
                    execution_id = result.get('execution_id')
                    if execution_id:
                        st.info(f"🔍 **Execution ID:** `{execution_id}`")
                        
                        st.warning("""
                        ⚠️ **Tracking in Sviluppo** - Usa la tab "🧪 Test HITL UI" per testare l'interfaccia
                        """)
                        
                        if st.checkbox("🎨 Mostra Anteprima HITL", key="preview_form"):
                            mock_result = {
                                "tipologia_provvedimento": f"Email da: {custom_from}",
                                "classification_confidence": 0.70,
                                "attachments_extracted": 0,
                                "email_subject": custom_subject
                            }
                            display_classification_result(mock_result)
                            display_hitl_checkpoint(mock_result)
                else:
                    st.error(f"❌ Errore invio: Status {result['status_code']}")
            else:
                st.warning("⚠️ Compila tutti i campi prima di inviare!")

with tab3:
    st.header("📊 Informazioni Workflow")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔄 Flusso Elaborazione")
        st.markdown("""
        ```
        📧 Email (.eml)
         ↓
        🌐 POST http://localhost:9099/contentListener/fascicolo
         ↓
        📦 Ingress_ContentListener
         ├─ HandleHttpRequest
         ├─ Generate_Workflow_ID
         ├─ Log_Incoming_Request
         ├─ Route_To_Workflow
         └─ HandleHttpResponse (HTTP 200)
         ↓
        📦 SP01_EML_Parser
         ├─ Input Port 'From_Ingress'
         ├─ Call_SP01_Microservice
         │   → POST http://sp01:5001/parse
         │   → Groq AI Classification
         ├─ Route_Success_Failure
         └─ Output Port 'Success'
         ↓
        📦 SP11_HITL_Manager
         ├─ Input Port 'From_SP01'
         ├─ Call_SP11_Security_Audit
         │   → POST http://hitl:5009/hitl/review
         └─ Human-In-The-Loop Review
        ```
        """)

    with col2:
        st.subheader("🎯 Checkpoint HITL")
        st.info("""
        **Obiettivo:** Validare il flusso completo dall'email iniziale
        fino all'arrivo dei dati al sistema HITL per la review umana.
        """)

        st.subheader("✅ Componenti Attivi")
        st.markdown("""
        - ✅ Ingress HTTP Endpoint (porta 9099)
        - ✅ SP01 EML Parser (porta 5001)
        - ✅ HITL Manager (porta 5009)
        - ✅ NiFi Process Groups connessi
        - ✅ Classificazione AI Groq
        """)

        st.subheader("📈 Metriche")
        st.markdown("""
        - **Process Groups:** 10
        - **Connessioni inter-PG:** 2
        - **Microservizi:** 5 attivi
        - **Controller Services:** 3
        """)

with tab4:
    st.header("🧪 Test Interfaccia HITL")
    st.markdown("""
    Questa tab ti permette di testare l'interfaccia HITL con dati mock senza dover eseguire l'intero workflow.
    
    Utile per:
    - Vedere come appare il checkpoint HITL
    - Testare i bottoni Approva/Rigetta/Modifica
    - Visualizzare il layout dei risultati
    """)
    
    st.markdown("---")
    
    # Mock data per test
    mock_result = {
        "tipologia_provvedimento": "Autorizzazione Scarico Acque Reflue",
        "classification_confidence": 0.92,
        "attachments_extracted": 2,
        "groq_model": "llama-3.3-70b-versatile",
        "processing_time_ms": 3200,
        "email_subject": "Richiesta autorizzazione scarico acque reflue industriali",
        "sender": "azienda.esempio@pec.it",
        "extracted_data": {
            "richiedente": "ACME Industrial S.p.A.",
            "tipo_scarico": "Acque reflue industriali",
            "portata_max": "50 m³/h",
            "corpo_ricettore": "Fiume Po"
        }
    }
    
    if st.button("🎨 Mostra Esempio HITL", type="primary", use_container_width=True):
        st.markdown("---")
        st.success("✅ **Simulazione Completata** - Ecco come apparirà l'interfaccia HITL:")
        st.markdown("---")
        
        # Display mock classification
        display_classification_result(mock_result)
        
        # Display HITL checkpoint
        display_hitl_checkpoint(mock_result)
    
    st.markdown("---")
    st.info("""
    💡 **Suggerimento:** Clicca sul bottone sopra per vedere un esempio completo di come
    l'utente vedrà i risultati della classificazione e potrà interagire con il checkpoint HITL.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🚀 POC Workflow Management System | Ingress → SP01 → HITL</p>
    <p><small>Apache NiFi + FastAPI + Groq AI + Streamlit</small></p>
</div>
""", unsafe_allow_html=True)
