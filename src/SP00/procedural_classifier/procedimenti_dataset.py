"""
Dataset Mock: Procedimenti Amministrativi → Provvedimenti
Per testing e sviluppo SP00 Procedural Classifier
"""

import pandas as pd
from typing import Dict, List, Tuple
import random


# ============================================================================
# MAPPATURA PROCEDIMENTI → PROVVEDIMENTI
# ============================================================================

PROCEDIMENTI_MAPPING = {
    # CATEGORIA: AMBIENTE
    "AUTORIZZAZIONE_SCARICO_ACQUE": {
        "categoria": "AMBIENTE",
        "sottocategoria": "TUTELA_ACQUE",
        "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
        "autorita_competente": "DIRIGENTE_SETTORE_AMBIENTE",
        "normativa": ["D.Lgs 152/2006", "L.R. 62/1998"],
        "termini_giorni": 90,
        "keywords": ["scarico", "acque reflue", "depurazione", "autorizzazione idraulica"]
    },
    "VIA_VALUTAZIONE_IMPATTO_AMBIENTALE": {
        "categoria": "AMBIENTE",
        "sottocategoria": "VIA",
        "tipo_provvedimento": "DELIBERA_GIUNTA",
        "autorita_competente": "GIUNTA_COMUNALE",
        "normativa": ["D.Lgs 152/2006", "L.R. 10/2010"],
        "termini_giorni": 150,
        "keywords": ["VIA", "valutazione impatto", "studio ambientale", "sostenibilità"]
    },
    "AUTORIZZAZIONE_EMISSIONI_ATMOSFERA": {
        "categoria": "AMBIENTE",
        "sottocategoria": "EMISSIONI",
        "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
        "autorita_competente": "DIRIGENTE_SETTORE_AMBIENTE",
        "normativa": ["D.Lgs 152/2006 Parte V"],
        "termini_giorni": 90,
        "keywords": ["emissioni", "atmosfera", "inquinamento", "camino", "fumi"]
    },
    
    # CATEGORIA: URBANISTICA
    "PERMESSO_DI_COSTRUIRE": {
        "categoria": "URBANISTICA",
        "sottocategoria": "EDILIZIA",
        "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
        "autorita_competente": "DIRIGENTE_EDILIZIA",
        "normativa": ["D.P.R. 380/2001", "L.R. 12/2005"],
        "termini_giorni": 60,
        "keywords": ["permesso costruire", "edificazione", "PDC", "costruzione"]
    },
    "VARIANTE_URBANISTICA": {
        "categoria": "URBANISTICA",
        "sottocategoria": "PIANIFICAZIONE",
        "tipo_provvedimento": "DELIBERA_CONSIGLIO",
        "autorita_competente": "CONSIGLIO_COMUNALE",
        "normativa": ["L.R. 12/2005"],
        "termini_giorni": 180,
        "keywords": ["variante", "piano regolatore", "PRG", "zonizzazione"]
    },
    "CERTIFICATO_DESTINAZIONE_URBANISTICA": {
        "categoria": "URBANISTICA",
        "sottocategoria": "CERTIFICAZIONI",
        "tipo_provvedimento": "CERTIFICATO",
        "autorita_competente": "DIRIGENTE_EDILIZIA",
        "normativa": ["D.P.R. 380/2001"],
        "termini_giorni": 30,
        "keywords": ["CDU", "destinazione urbanistica", "certificato", "vincoli"]
    },
    
    # CATEGORIA: COMMERCIO
    "LICENZA_COMMERCIALE": {
        "categoria": "COMMERCIO",
        "sottocategoria": "COMMERCIO_DETTAGLIO",
        "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
        "autorita_competente": "DIRIGENTE_SUAP",
        "normativa": ["D.Lgs 114/1998"],
        "termini_giorni": 90,
        "keywords": ["licenza commerciale", "esercizio commerciale", "vendita", "negozio"]
    },
    "SCIA_COMMERCIO": {
        "categoria": "COMMERCIO",
        "sottocategoria": "COMMERCIO_DETTAGLIO",
        "tipo_provvedimento": "RICEVUTA_SCIA",
        "autorita_competente": "DIRIGENTE_SUAP",
        "normativa": ["L. 122/2010"],
        "termini_giorni": 0,  # SCIA è ad efficacia immediata
        "keywords": ["SCIA", "segnalazione certificata", "inizio attività", "commercio"]
    },
    "OCCUPAZIONE_SUOLO_PUBBLICO": {
        "categoria": "COMMERCIO",
        "sottocategoria": "DEMANIO",
        "tipo_provvedimento": "ORDINANZA",
        "autorita_competente": "SINDACO",
        "normativa": ["Codice della Strada", "Regolamento comunale"],
        "termini_giorni": 30,
        "keywords": ["occupazione suolo", "dehors", "plateatico", "passi carrabili"]
    },
    
    # CATEGORIA: SOCIALE
    "ASSEGNAZIONE_ALLOGGIO_ERP": {
        "categoria": "SOCIALE",
        "sottocategoria": "EDILIZIA_RESIDENZIALE",
        "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
        "autorita_competente": "DIRIGENTE_SERVIZI_SOCIALI",
        "normativa": ["L.R. 96/1996"],
        "termini_giorni": 120,
        "keywords": ["alloggio", "ERP", "casa popolare", "assegnazione"]
    },
    "CONTRIBUTO_ASSISTENZIALE": {
        "categoria": "SOCIALE",
        "sottocategoria": "ASSISTENZA",
        "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
        "autorita_competente": "DIRIGENTE_SERVIZI_SOCIALI",
        "normativa": ["L. 328/2000"],
        "termini_giorni": 60,
        "keywords": ["contributo", "assistenza", "sussidio", "aiuto economico"]
    },
    
    # CATEGORIA: MOBILITÀ
    "AUTORIZZAZIONE_ZTL": {
        "categoria": "MOBILITA",
        "sottocategoria": "TRAFFICO",
        "tipo_provvedimento": "ORDINANZA",
        "autorita_competente": "SINDACO",
        "normativa": ["Codice della Strada"],
        "termini_giorni": 30,
        "keywords": ["ZTL", "zona traffico limitato", "accesso", "centro storico"]
    },
    "PERMESSO_PARCHEGGIO_RESIDENTI": {
        "categoria": "MOBILITA",
        "sottocategoria": "SOSTA",
        "tipo_provvedimento": "AUTORIZZAZIONE",
        "autorita_competente": "DIRIGENTE_MOBILITA",
        "normativa": ["Regolamento comunale sosta"],
        "termini_giorni": 15,
        "keywords": ["parcheggio", "residenti", "sosta", "contrassegno"]
    },
    
    # CATEGORIA: CULTURA
    "PATROCINIO_COMUNALE": {
        "categoria": "CULTURA",
        "sottocategoria": "EVENTI",
        "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
        "autorita_competente": "DIRIGENTE_CULTURA",
        "normativa": ["Regolamento patrocini"],
        "termini_giorni": 30,
        "keywords": ["patrocinio", "evento", "manifestazione", "logo comunale"]
    },
}


# ============================================================================
# FUNZIONI GENERAZIONE DATASET
# ============================================================================

def generate_istanza_text(procedimento: str, info: Dict) -> str:
    """
    Genera testo realistico di un'istanza di parte
    
    Args:
        procedimento: Nome del procedimento
        info: Informazioni sul procedimento
    
    Returns:
        Testo dell'istanza
    """
    templates = {
        "AUTORIZZAZIONE_SCARICO_ACQUE": [
            "Spettabile Comune, la scrivente {azienda} richiede autorizzazione allo scarico di acque reflue industriali provenienti dal ciclo produttivo. Portata media: {portata} m³/giorno. Si allega relazione tecnica e planimetria degli impianti.",
            "Con la presente si richiede il rilascio dell'autorizzazione per lo scarico delle acque reflue industriali ai sensi del D.Lgs 152/2006. L'attività produttiva è {tipo_attivita} con scarico in pubblica fognatura.",
            "In qualità di legale rappresentante di {azienda}, chiedo autorizzazione per lo scarico di acque reflue di processo. L'impianto di depurazione è conforme alle norme vigenti. Allego documentazione tecnica completa.",
        ],
        "PERMESSO_DI_COSTRUIRE": [
            "Il sottoscritto {richiedente} chiede il rilascio del permesso di costruire per la realizzazione di un fabbricato residenziale unifamiliare sito in {indirizzo}. Superficie coperta: {mq} mq. Si allegano elaborati progettuali.",
            "Richiesta permesso di costruire per edificazione villetta bifamiliare su lotto di proprietà in zona residenziale {zona}. Progetto conforme a PRG vigente. Rispetto vincoli paesaggistici.",
            "La scrivente società richiede PDC per realizzazione capannone industriale destinato a {destinazione}. Volume: {volume} mc. Rispetto norme antisismiche e antincendio.",
        ],
        "LICENZA_COMMERCIALE": [
            "Il sottoscritto {richiedente} chiede il rilascio della licenza per l'esercizio di attività commerciale di {tipo_commercio} presso i locali siti in {indirizzo}. Superficie: {mq} mq.",
            "Con la presente si richiede licenza commerciale per apertura negozio di {settore} nel centro cittadino. Locali conformi a normative igienico-sanitarie e sicurezza.",
            "Richiesta autorizzazione commerciale per vendita al dettaglio di {prodotti}. L'esercizio sarà ubicato in {zona} con orario di apertura {orario}.",
        ],
        "SCIA_COMMERCIO": [
            "Si presenta SCIA per inizio attività commerciale di {tipo_attivita} presso {indirizzo}. Dichiarazione conformità locali e requisiti professionali del titolare.",
            "Segnalazione Certificata Inizio Attività per esercizio commerciale vendita {prodotti}. Superficie vendita: {mq} mq. Rispetto requisiti igienico-sanitari.",
            "Ai sensi della L. 122/2010 si presenta SCIA per apertura negozio {tipo_negozio}. Possesso requisiti morali e professionali. Conformità urbanistica locali.",
        ],
        "VARIANTE_URBANISTICA": [
            "Il Comune chiede approvazione variante al Piano Regolatore per modifica destinazione urbanistica area {zona} da {da} a {a}. Motivazione: {motivazione}.",
            "Si propone variante urbanistica per riqualificazione area industriale dismessa in zona residenziale. Prevista realizzazione di {progetto}.",
            "Variante PRG per ampliamento zona artigianale e servizi. Studio di impatto viabilistico allegato. Compatibilità con piano sovracomunale verificata.",
        ],
        "VIA_VALUTAZIONE_IMPATTO_AMBIENTALE": [
            "Si richiede procedura VIA per realizzazione {opera} in zona {località}. Allegato Studio di Impatto Ambientale comprensivo di analisi alternative progettuali.",
            "La scrivente società presenta istanza per Valutazione Impatto Ambientale relativa a progetto di {progetto}. Impatto previsto su matrici: aria, acqua, suolo, rumore.",
            "Richiesta VIA per costruzione impianto {tipo_impianto} con potenza {potenza} MW. Studio ambientale completo e misure mitigazione impatti allegati.",
        ],
    }
    
    # Seleziona template casuale per il procedimento
    if procedimento in templates:
        template = random.choice(templates[procedimento])
        
        # Sostituisci placeholder con valori casuali
        placeholders = {
            "azienda": random.choice(["ABC S.p.A.", "XYZ S.r.l.", "Industria Rossi", "Manifatture Italia"]),
            "richiedente": random.choice(["Mario Rossi", "Laura Bianchi", "Giuseppe Verdi", "Anna Romano"]),
            "indirizzo": random.choice(["Via Roma 123", "Corso Italia 45", "Piazza Garibaldi 8", "Via Mazzini 67"]),
            "zona": random.choice(["B2", "D1", "C3", "A1"]),
            "portata": random.choice(["500", "1000", "250", "750"]),
            "mq": random.choice(["150", "200", "300", "500"]),
            "volume": random.choice(["2000", "3500", "5000", "8000"]),
            "tipo_attivita": random.choice(["tessile", "chimica", "alimentare", "meccanica"]),
            "tipo_commercio": random.choice(["abbigliamento", "alimentari", "elettronica", "ferramenta"]),
            "settore": random.choice(["abbigliamento", "calzature", "gioielleria", "profumeria"]),
            "prodotti": random.choice(["abbigliamento", "generi alimentari", "articoli sportivi", "libri"]),
            "tipo_negozio": random.choice(["alimentari", "abbigliamento", "ferramenta", "giocattoli"]),
            "tipo_attivita": random.choice(["bar", "ristorante", "negozio alimentari", "parrucchiere"]),
            "orario": random.choice(["continuato", "8:30-19:30", "9:00-13:00 / 15:30-19:30"]),
            "destinazione": random.choice(["logistica", "produzione", "magazzino", "artigianato"]),
            "da": random.choice(["agricola", "industriale", "verde"]),
            "a": random.choice(["residenziale", "commerciale", "servizi"]),
            "motivazione": random.choice(["sviluppo urbano", "riqualificazione", "necessità abitativa"]),
            "progetto": random.choice(["residenze", "parco pubblico", "centro servizi"]),
            "opera": random.choice(["autostrada", "impianto fotovoltaico", "centro commerciale"]),
            "località": random.choice(["Vallechiara", "Monte Alto", "Pianura Verde"]),
            "progetto": random.choice(["impianto eolico", "discarica rifiuti", "centrale elettrica"]),
            "tipo_impianto": random.choice(["fotovoltaico", "eolico", "biomasse"]),
            "potenza": random.choice(["5", "10", "20", "50"]),
        }
        
        # Sostituisci tutti i placeholder
        result = template
        for key, value in placeholders.items():
            result = result.replace(f"{{{key}}}", value)
        
        return result
    
    # Fallback generico
    return f"Richiesta per procedimento {procedimento}. Documentazione allegata."


def create_procedimenti_dataset(n_samples_per_procedimento: int = 5) -> pd.DataFrame:
    """
    Crea dataset di istanze di parte per testing classificatore
    
    Args:
        n_samples_per_procedimento: Numero di istanze per ogni procedimento
    
    Returns:
        DataFrame con istanze sintetiche
    """
    data = []
    
    for procedimento, info in PROCEDIMENTI_MAPPING.items():
        for i in range(n_samples_per_procedimento):
            # Genera testo istanza
            testo_istanza = generate_istanza_text(procedimento, info)
            
            # Aggiungi rumore occasionale (per testare robustezza)
            if random.random() < 0.1:  # 10% con info aggiuntive
                noise = random.choice([
                    " Si richiede cortese riscontro urgente.",
                    " Ringrazio anticipatamente per l'attenzione.",
                    " Resto a disposizione per chiarimenti.",
                    " In attesa di riscontro, porgo cordiali saluti.",
                ])
                testo_istanza += noise
            
            data.append({
                "id_istanza": f"IST-{len(data)+1:04d}",
                "testo": testo_istanza,
                "procedimento": procedimento,
                "categoria": info["categoria"],
                "sottocategoria": info["sottocategoria"],
                "tipo_provvedimento": info["tipo_provvedimento"],
                "autorita_competente": info["autorita_competente"],
                "normativa": ", ".join(info["normativa"]),
                "termini_giorni": info["termini_giorni"],
            })
    
    return pd.DataFrame(data)


def get_procedimento_info(procedimento: str) -> Dict:
    """Ottiene informazioni su un procedimento specifico"""
    return PROCEDIMENTI_MAPPING.get(procedimento, {})


def get_all_procedimenti() -> List[str]:
    """Ottiene lista di tutti i procedimenti nel dataset"""
    return list(PROCEDIMENTI_MAPPING.keys())


def get_procedimenti_by_categoria(categoria: str) -> List[str]:
    """Ottiene procedimenti filtrati per categoria"""
    return [
        proc for proc, info in PROCEDIMENTI_MAPPING.items()
        if info["categoria"] == categoria
    ]


def get_categorie() -> List[str]:
    """Ottiene lista di tutte le categorie"""
    return list(set(info["categoria"] for info in PROCEDIMENTI_MAPPING.values()))


def get_tipi_provvedimento() -> List[str]:
    """Ottiene lista di tutti i tipi di provvedimento"""
    return list(set(info["tipo_provvedimento"] for info in PROCEDIMENTI_MAPPING.values()))


# ============================================================================
# MAIN - Test
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("📊 DATASET PROCEDIMENTI AMMINISTRATIVI - SP00")
    print("=" * 80)
    
    # Crea dataset
    df = create_procedimenti_dataset(n_samples_per_procedimento=3)
    
    print(f"\n✅ Dataset creato: {len(df)} istanze")
    print(f"   Procedimenti unici: {df['procedimento'].nunique()}")
    print(f"   Categorie: {df['categoria'].nunique()}")
    print(f"   Tipi provvedimento: {df['tipo_provvedimento'].nunique()}")
    
    # Statistiche
    print("\n📈 DISTRIBUZIONE PER CATEGORIA:")
    print(df['categoria'].value_counts().to_string())
    
    print("\n📋 DISTRIBUZIONE TIPI PROVVEDIMENTO:")
    print(df['tipo_provvedimento'].value_counts().to_string())
    
    # Esempi
    print("\n📧 ESEMPI DI ISTANZE:")
    print("=" * 80)
    for idx in range(min(3, len(df))):
        row = df.iloc[idx]
        print(f"\n{idx+1}. ID: {row['id_istanza']}")
        print(f"   Procedimento: {row['procedimento']}")
        print(f"   Provvedimento: {row['tipo_provvedimento']}")
        print(f"   Categoria: {row['categoria']}")
        print(f"   Testo: {row['testo'][:150]}...")
        print("-" * 80)
    
    # Salva CSV
    filename = "dataset_procedimenti_pa.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n💾 Dataset salvato: {filename}")
