"""
Template esempio per determine amministrative.
"""

TEMPLATE_STANDARD = {
    "id": "standard",
    "nome": "Template Standard Determina",
    "versione": "1.0",
    "struttura": {
        "intestazione": {
            "ente": "{ente_nome}",
            "settore": "{settore_nome}",
            "numero": "Determina n. [DA_ASSEGNARE]",
            "data": "[DATA_ODIERNA]"
        },
        "oggetto_template": "Procedimento relativo a {oggetto_richiesta} - Richiedente: {richiedente_nome}",
        "premesse_template": """
IL DIRIGENTE

PREMESSO CHE:
- in data {data_istanza} è pervenuta istanza da parte di {richiedente_completo}, codice fiscale {codice_fiscale}, per {oggetto_richiesta};
- l'istanza è stata presentata ai sensi di {normativa_riferimento};
- sono stati allegati i seguenti documenti: {elenco_documenti};

RICHIAMATI:
- {riferimenti_normativi};
- lo Statuto Comunale e il Regolamento;

PRESO ATTO che {ente_nome} è competente per il rilascio del presente atto;

VERIFICATA la completezza della documentazione presentata;
""",
        "motivazione_template": """
CONSIDERATO CHE:
- l'istruttoria condotta dall'ufficio ha evidenziato {risultati_istruttoria};
- la richiesta risulta {valutazione_conformita} con la normativa vigente;
- {ulteriori_considerazioni};

RITENUTO di dover procedere {decisione_motivazione};
""",
        "dispositivo_template": """
DETERMINA

di {decisione_finale} la richiesta presentata da {richiedente_completo} per {oggetto_richiesta}.

{eventuali_prescrizioni}

La presente determina:
- è immediatamente esecutiva;
- sarà pubblicata all'Albo Pretorio per 15 giorni consecutivi;
- sarà notificata all'interessato.

Avverso la presente determina è ammesso ricorso al TAR entro 60 giorni dalla notificazione.
"""
    }
}

TEMPLATE_AUTORIZZAZIONE = {
    "id": "autorizzazione",
    "nome": "Template Autorizzazione",
    "versione": "1.0",
    "struttura": {
        "oggetto_template": "Autorizzazione per {oggetto_richiesta} - Richiedente: {richiedente_nome}",
        "dispositivo_specifico": """
AUTORIZZA

{richiedente_completo} all'esercizio di {attivita_autorizzata} con le seguenti prescrizioni:

{prescrizioni_specifiche}

L'autorizzazione:
- ha validità {durata_validita};
- è soggetta al pagamento dei diritti dovuti;
- decade in caso di mancato rispetto delle prescrizioni.
"""
    }
}

TEMPLATE_CONCESSIONE = {
    "id": "concessione",
    "nome": "Template Concessione",
    "versione": "1.0", 
    "struttura": {
        "oggetto_template": "Concessione per {oggetto_richiesta} - Richiedente: {richiedente_nome}",
        "dispositivo_specifico": """
CONCEDE

a {richiedente_completo} la concessione per {oggetto_concessione} con le seguenti modalità:

{modalita_concessione}

Oneri e condizioni:
{oneri_condizioni}

La concessione ha durata {durata_concessione} ed è rinnovabile su istanza di parte.
"""
    }
}

# Dizionario dei template disponibili
TEMPLATES = {
    "standard": TEMPLATE_STANDARD,
    "autorizzazione": TEMPLATE_AUTORIZZAZIONE,
    "concessione": TEMPLATE_CONCESSIONE
}

def get_template(template_id: str) -> dict:
    """Ottiene un template specifico"""
    return TEMPLATES.get(template_id, TEMPLATE_STANDARD)

def get_available_templates() -> list:
    """Ottiene la lista dei template disponibili"""
    return list(TEMPLATES.keys())
