-- =========================================
-- Dati di esempio per procedimenti amministrativi
-- =========================================

-- Procedimento: Autorizzazione Scarico Acque Reflue
INSERT INTO procedimenti_amministrativi (
    codice,
    denominazione,
    categoria,
    sottocategoria,
    normativa_base,
    termini_giorni,
    silenzio_assenso,
    tipo_provvedimento_default,
    autorita_competente,
    metadata_required,
    fasi_procedurali,
    enti_coinvolti,
    template_id,
    keywords
) VALUES (
    'PROC_AMB_001',
    'AUTORIZZAZIONE_SCARICO_ACQUE_REFLUE',
    'AMBIENTE',
    'TUTELA_ACQUE',
    '[
        {"tipo": "DECRETO_LEGISLATIVO", "numero": "152/2006", "articolo": "124", "descrizione": "Disciplina degli scarichi"},
        {"tipo": "LEGGE_REGIONALE", "numero": "62/1998", "articolo": "8", "descrizione": "Norme regionali tutela acque"}
    ]'::jsonb,
    90,
    false,
    'DETERMINAZIONE_DIRIGENZIALE',
    'DIRIGENTE_SETTORE_AMBIENTE',
    '{
        "obbligatori": [
            "dati_identificativi_richiedente",
            "localizzazione_scarico",
            "caratteristiche_scarico",
            "relazione_tecnica",
            "planimetria",
            "certificato_iscrizione_cciaa"
        ],
        "opzionali": [
            "studio_impatto_ambientale",
            "documentazione_fotografica"
        ]
    }'::jsonb,
    '[
        "VERIFICA_COMPLETEZZA_ISTANZA",
        "ISTRUTTORIA_TECNICA",
        "PARERI_ENTI_ESTERNI",
        "CONFERENZA_SERVIZI",
        "DETERMINAZIONE_FINALE"
    ]'::jsonb,
    '[
        {"ente": "ARPA", "tipo_coinvolgimento": "PARERE_OBBLIGATORIO", "termini_risposta": 30},
        {"ente": "ASL", "tipo_coinvolgimento": "PARERE_FACOLTATIVO", "termini_risposta": 15}
    ]'::jsonb,
    'TPL_DET_AMB_001',
    ARRAY['scarico', 'acque', 'reflue', 'industriali', 'autorizzazione', 'ambiente']
);

-- Procedimento: Permesso di Costruire
INSERT INTO procedimenti_amministrativi (
    codice,
    denominazione,
    categoria,
    sottocategoria,
    normativa_base,
    termini_giorni,
    silenzio_assenso,
    tipo_provvedimento_default,
    autorita_competente,
    metadata_required,
    fasi_procedurali,
    enti_coinvolti,
    template_id,
    keywords
) VALUES (
    'PROC_URB_001',
    'PERMESSO_DI_COSTRUIRE',
    'URBANISTICA',
    'EDILIZIA',
    '[
        {"tipo": "DPR", "numero": "380/2001", "articolo": "20", "descrizione": "Testo Unico Edilizia"},
        {"tipo": "LEGGE_REGIONALE", "numero": "12/2005", "articolo": "15", "descrizione": "Governo del territorio"}
    ]'::jsonb,
    60,
    false,
    'DETERMINAZIONE_DIRIGENZIALE',
    'DIRIGENTE_EDILIZIA',
    '{
        "obbligatori": [
            "dati_identificativi_richiedente",
            "titolo_proprieta",
            "progetto_architettonico",
            "relazione_tecnica",
            "calcoli_strutturali",
            "certificato_destinazione_urbanistica"
        ],
        "opzionali": [
            "relazione_paesaggistica",
            "valutazione_sismica"
        ]
    }'::jsonb,
    '[
        "VERIFICA_COMPLETEZZA_ISTANZA",
        "ISTRUTTORIA_URBANISTICA",
        "PARERI_ENTI_ESTERNI",
        "VERIFICA_VINCOLI",
        "DETERMINAZIONE_FINALE"
    ]'::jsonb,
    '[
        {"ente": "SOPRINTENDENZA", "tipo_coinvolgimento": "PARERE_VINCOLANTE", "termini_risposta": 45},
        {"ente": "VIGILI_FUOCO", "tipo_coinvolgimento": "PARERE_OBBLIGATORIO", "termini_risposta": 30}
    ]'::jsonb,
    'TPL_DET_URB_001',
    ARRAY['permesso', 'costruire', 'edilizia', 'urbanistica', 'costruzione']
);

-- Procedimento: Licenza Commerciale
INSERT INTO procedimenti_amministrativi (
    codice,
    denominazione,
    categoria,
    sottocategoria,
    normativa_base,
    termini_giorni,
    silenzio_assenso,
    tipo_provvedimento_default,
    autorita_competente,
    metadata_required,
    fasi_procedurali,
    enti_coinvolti,
    template_id,
    keywords
) VALUES (
    'PROC_COMM_001',
    'LICENZA_COMMERCIALE',
    'COMMERCIO',
    'ATTIVITA_COMMERCIALI',
    '[
        {"tipo": "DECRETO_LEGISLATIVO", "numero": "114/1998", "articolo": "7", "descrizione": "Riforma commercio"},
        {"tipo": "LEGGE_REGIONALE", "numero": "28/2005", "articolo": "12", "descrizione": "Commercio regionale"}
    ]'::jsonb,
    45,
    true,
    'DETERMINAZIONE_DIRIGENZIALE',
    'DIRIGENTE_SUAP',
    '{
        "obbligatori": [
            "dati_identificativi_richiedente",
            "certificato_iscrizione_cciaa",
            "planimetria_locali",
            "dichiarazione_conformita_urbanistica",
            "certificato_agibilita"
        ],
        "opzionali": [
            "dichiarazione_haccp",
            "autorizzazione_somministrazione"
        ]
    }'::jsonb,
    '[
        "VERIFICA_COMPLETEZZA_ISTANZA",
        "ISTRUTTORIA_SUAP",
        "VERIFICA_REQUISITI",
        "DETERMINAZIONE_FINALE"
    ]'::jsonb,
    '[
        {"ente": "ASL", "tipo_coinvolgimento": "PARERE_OBBLIGATORIO", "termini_risposta": 30},
        {"ente": "VIGILI_FUOCO", "tipo_coinvolgimento": "PARERE_FACOLTATIVO", "termini_risposta": 20}
    ]'::jsonb,
    'TPL_DET_COMM_001',
    ARRAY['licenza', 'commerciale', 'negozio', 'attività', 'commercio']
);

-- Procedimento: Autorizzazione ZTL
INSERT INTO procedimenti_amministrativi (
    codice,
    denominazione,
    categoria,
    sottocategoria,
    normativa_base,
    termini_giorni,
    silenzio_assenso,
    tipo_provvedimento_default,
    autorita_competente,
    metadata_required,
    fasi_procedurali,
    enti_coinvolti,
    template_id,
    keywords
) VALUES (
    'PROC_MOB_001',
    'AUTORIZZAZIONE_ZTL',
    'MOBILITA',
    'CIRCOLAZIONE',
    '[
        {"tipo": "DECRETO_LEGISLATIVO", "numero": "285/1992", "articolo": "7", "descrizione": "Codice della Strada"},
        {"tipo": "REGOLAMENTO_COMUNALE", "numero": "45/2020", "articolo": "3", "descrizione": "ZTL comunale"}
    ]'::jsonb,
    15,
    false,
    'ORDINANZA',
    'SINDACO',
    '{
        "obbligatori": [
            "dati_identificativi_richiedente",
            "motivazione_accesso",
            "targa_veicolo",
            "periodo_richiesto"
        ],
        "opzionali": [
            "certificato_disabilita",
            "autorizzazione_cantiere"
        ]
    }'::jsonb,
    '[
        "VERIFICA_COMPLETEZZA_ISTANZA",
        "ISTRUTTORIA_POLIZIA_LOCALE",
        "ORDINANZA_SINDACALE"
    ]'::jsonb,
    '[
        {"ente": "POLIZIA_LOCALE", "tipo_coinvolgimento": "ISTRUTTORIA", "termini_risposta": 10}
    ]'::jsonb,
    'TPL_ORD_MOB_001',
    ARRAY['ztl', 'zona', 'traffico', 'limitato', 'accesso', 'circolazione']
);

-- Procedimento: Assegnazione Alloggio ERP
INSERT INTO procedimenti_amministrativi (
    codice,
    denominazione,
    categoria,
    sottocategoria,
    normativa_base,
    termini_giorni,
    silenzio_assenso,
    tipo_provvedimento_default,
    autorita_competente,
    metadata_required,
    fasi_procedurali,
    enti_coinvolti,
    template_id,
    keywords
) VALUES (
    'PROC_SOC_001',
    'ASSEGNAZIONE_ALLOGGIO_ERP',
    'SOCIALE',
    'EDILIZIA_RESIDENZIALE_PUBBLICA',
    '[
        {"tipo": "LEGGE", "numero": "179/1992", "articolo": "2", "descrizione": "Edilizia Residenziale Pubblica"},
        {"tipo": "LEGGE_REGIONALE", "numero": "96/1996", "articolo": "18", "descrizione": "Edilizia residenziale"}
    ]'::jsonb,
    120,
    false,
    'DETERMINAZIONE_DIRIGENZIALE',
    'DIRIGENTE_SERVIZI_SOCIALI',
    '{
        "obbligatori": [
            "dati_identificativi_richiedente",
            "composizione_nucleo_familiare",
            "isee",
            "dichiarazione_redditi",
            "certificato_residenza"
        ],
        "opzionali": [
            "certificato_invalidita",
            "documentazione_sfratto"
        ]
    }'::jsonb,
    '[
        "VERIFICA_COMPLETEZZA_ISTANZA",
        "ISTRUTTORIA_SOCIALE",
        "CALCOLO_PUNTEGGIO",
        "GRADUATORIA",
        "DETERMINAZIONE_ASSEGNAZIONE"
    ]'::jsonb,
    '[
        {"ente": "INPS", "tipo_coinvolgimento": "VERIFICA_ISEE", "termini_risposta": 20}
    ]'::jsonb,
    'TPL_DET_SOC_001',
    ARRAY['alloggio', 'erp', 'sociale', 'casa', 'popolare', 'assegnazione']
);

-- Procedimento: Variante Urbanistica
INSERT INTO procedimenti_amministrativi (
    codice,
    denominazione,
    categoria,
    sottocategoria,
    normativa_base,
    termini_giorni,
    silenzio_assenso,
    tipo_provvedimento_default,
    autorita_competente,
    metadata_required,
    fasi_procedurali,
    enti_coinvolti,
    template_id,
    keywords
) VALUES (
    'PROC_URB_002',
    'VARIANTE_URBANISTICA',
    'URBANISTICA',
    'PIANIFICAZIONE',
    '[
        {"tipo": "LEGGE_REGIONALE", "numero": "12/2005", "articolo": "25", "descrizione": "Governo del territorio"},
        {"tipo": "DPR", "numero": "380/2001", "articolo": "15", "descrizione": "Testo Unico Edilizia"}
    ]'::jsonb,
    180,
    false,
    'DELIBERA_CONSIGLIO',
    'CONSIGLIO_COMUNALE',
    '{
        "obbligatori": [
            "relazione_tecnica",
            "elaborati_grafici",
            "norme_tecniche_attuazione",
            "rapporto_ambientale_vas"
        ],
        "opzionali": [
            "studio_viabilita",
            "relazione_geologica"
        ]
    }'::jsonb,
    '[
        "ADOZIONE_GIUNTA",
        "PUBBLICAZIONE",
        "OSSERVAZIONI_PUBBLICO",
        "CONTRODEDUZIONI",
        "APPROVAZIONE_CONSIGLIO",
        "PUBBLICAZIONE_DEFINITIVA"
    ]'::jsonb,
    '[
        {"ente": "REGIONE", "tipo_coinvolgimento": "PARERE_VINCOLANTE", "termini_risposta": 90},
        {"ente": "SOPRINTENDENZA", "tipo_coinvolgimento": "PARERE_VINCOLANTE", "termini_risposta": 60},
        {"ente": "ASL", "tipo_coinvolgimento": "PARERE_OBBLIGATORIO", "termini_risposta": 45}
    ]'::jsonb,
    'TPL_DEL_URB_001',
    ARRAY['variante', 'urbanistica', 'piano', 'regolatore', 'pgt', 'pianificazione']
);

-- Aggiungi altri procedimenti comuni...

-- Log di inizializzazione
INSERT INTO audit_log (
    action,
    details,
    user_id
) VALUES (
    'INIT_PROCEDIMENTI',
    '{"count": 6, "categories": ["AMBIENTE", "URBANISTICA", "COMMERCIO", "MOBILITA", "SOCIALE"]}',
    'SYSTEM'
);
