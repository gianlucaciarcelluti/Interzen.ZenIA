"""
Dataset mock di email per classificazione sinistri medical malpractice.
PROSPETTIVA: Medico/Ospedale (assicurato) che segnala alla compagnia

Versione: 1000 email totali con classificazione multi-dimensionale

DIMENSIONE 1 - Tipologia:
- 0: Sinistro Avvenuto (incidente già verificato)
- 1: Circostanza Potenziale (situazione che potrebbe generare un sinistro)

DIMENSIONE 2 - Riferimento Temporale:
- 0: Fatto Iniziale (prima segnalazione del caso)
- 1: Follow-up (aggiornamento, integrazione documentale, evoluzione del caso)

Distribuzione: 250 email per ogni combinazione (0-0, 0-1, 1-0, 1-1)
"""

import pandas as pd
import random
from datetime import datetime, timedelta

def generate_random_date(start_year=2023, end_year=2024):
    """Genera una data casuale per rendere gli esempi più vari."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    date = start + timedelta(days=random_days)
    return date.strftime("%d/%m/%Y")

def generate_case_id():
    """Genera un ID caso per i follow-up."""
    prefixes = ["SIN", "PRAT", "RC", "MM", "CLM", "DEN"]
    year = random.choice(["23", "24"])
    number = random.randint(1000, 9999)
    return f"{random.choice(prefixes)}{year}{number}"

def create_mock_dataset():
    """Crea un dataset di 1000 email simulate per training e testing."""
    
    emails = []
    
    # ============================================================================
    # CATEGORIA 0-0: SINISTRI AVVENUTI - FATTO INIZIALE (250 esempi)
    # ============================================================================
    sinistri_iniziali = [
        "Spett.le Compagnia, sono il Dr. {medico} e vi scrivo per segnalare un evento avverso verificatosi il {data} presso il nostro reparto. Durante intervento chirurgico al ginocchio sx, per errore procedurale è stato operato il ginocchio dx del paziente. Il paziente è stato informato e richiede risarcimento. Allego documentazione clinica completa.",
        "Alla c.a. dell'Ufficio Sinistri. Sono il Primario {medico} del reparto di Cardiologia. Vi comunico con rammarico il decesso del paziente avvenuto il {data} per diagnosi tardiva di embolia polmonare, inizialmente interpretata come polmonite. I familiari hanno già manifestato intenzione di rivalsa legale. Necessario apertura sinistro.",
        "Oggetto: Denuncia sinistro del {data}. Io sottoscritto Dr. {medico}, responsabile della UOC di Anestesia, comunico evento sentinella: somministrazione farmaco errato ha causato danno permanente al paziente. La famiglia è assistita da legale. Chiedo immediata apertura pratica assicurativa.",
        "Egregi Signori, Dr.ssa {medico}, Direttore Sanitario Ospedale San Raffaele. Segnalo sinistro verificatosi il {data}: durante parto cesareo lesione iatrogena nervo sciatico con esiti invalidanti per la partoriente. La paziente ha già depositato formale reclamo. Allego relazione dettagliata.",
        "Spett.le compagnia assicurativa, sono il Dr. {medico}, chirurgo generale. Vi notifico complicanza post-operatoria grave del {data}: infezione nosocomiale da MDR dopo appendicectomia con necessità di tre reinterventi. Il paziente lamenta responsabilità medica. Richiedo attivazione copertura.",
        "Alla Direzione Sinistri. Sottoscritto Dr. {medico}, cardiologo. Comunico errore terapeutico del {data}: errata posologia anticoagulante ha causato emorragia cerebrale con danni neurologici permanenti. Familiari hanno contestato formalmente l'assistenza. Necessaria vostra valutazione urgente.",
        "Oggetto: Sinistro medico - {data}. Dr. {medico}, radiologo. Devo con dispiacere segnalare mancata diagnosi di neoplasia polmonare visibile in TAC torace. La massa era presente e refertabile. Ritardo diagnostico di 6 mesi ha compromesso prognosi. Paziente ha già consultato legale.",
        "Spett.le ufficio, sono il Dr. {medico}, responsabile UO Ortopedia. Segnalo caduta paziente da letto ospedaliero in data {data} con frattura femore. Dalle verifiche interne risultano assenti le protezioni laterali prescritte per paziente a rischio. Famiglia richiede risarcimento.",
        "Egregi, Dr.ssa {medico}, chirurgo laparoscopico. Comunico evento avverso intraoperatorio del {data}: ustioni iatrogene da elettrobisturi con perforazione intestinale. Necessario reintervento d'urgenza. Il paziente è informato della complicanza e dei suoi diritti. Chiedo attivazione polizza.",
        "Alla c.a. del Responsabile Sinistri. Sottoscritto Dr. {medico}, neonatologo. Segnalo danno neurologico permanente da asfissia perinatale verificatosi il {data}. Ritardo nell'esecuzione taglio cesareo d'emergenza. I genitori hanno manifestato intenzione di procedere legalmente.",
        "Spett.le compagnia, Dr. {medico}, primario cardiochirurgia. Vi informo di scambio paziente in sala operatoria del {data}: paziente omonimo sottoposto a intervento cardiaco non a lui destinato. Errore di identificazione pre-operatoria. Famiglia assistita da pool legale. Allego incident report.",
        "Oggetto: Apertura sinistro {data}. Dr.ssa {medico}, gastroenterologa. Durante colonscopia si è verificata perforazione colica con peritonite conseguente. Paziente ha richiesto formale spiegazione dell'accaduto e manifestato volontà di richiedere danni. Necessario vs intervento.",
        "Egregi Signori, sono il Dr. {medico}, Direttore UO Trasfusionale. Comunico grave errore trasfusionale del {data}: somministrata sacca gruppo incompatibile con shock anafilattico e danno renale permanente. Root cause analysis in corso. Famiglia ha già sporto denuncia. Urge apertura pratica.",
        "Spett.le ufficio sinistri, Dr. {medico}, ginecologo. Segnalo trauma ostetrico del {data}: frattura clavicola neonatale durante manovra estrattiva. Complicanza eccedente la normalità assistenziale. Genitori hanno richiesto copia cartella e consulenza legale. Allego documentazione completa.",
        "Alla Direzione, sottoscritto Dr. {medico}, responsabile Pronto Soccorso. Comunico con rammarico decesso paziente per mancata diagnosi di STEMI, dimesso con diagnosi errata di gastrite il {data}. Exitus a domicilio dopo 2 ore. Familiari hanno presentato esposto. Necessaria copertura assicurativa.",
        "Oggetto: Sinistro chirurgico {data}. Dr.ssa {medico}, chirurgo vascolare. Devo segnalare amputazione arto errato: consenso per arto dx ma errore nel controllo pre-operatorio ha portato ad amputare arto sx sano. Ammetto responsabilità. Paziente richiede risarcimento. Chiedo intervento compagnia.",
        "Spett.le assicurazione, Dr. {medico}, anestesista rianimatore. Comunico complicanza anestesiologica grave del {data}: lesione midollare da anestesia spinale con paraplegia conseguente. Tecnica corretta ma complicanza imprevedibile contestata dalla famiglia. Necessito supporto legale urgente.",
        "Egregi, sono il Dr. {medico}, allergologo in servizio. Segnalo decesso paziente per shock anafilattico da antibiotico il {data}. L'allergia era documentata in cartella ma non adeguatamente verificata prima somministrazione. Familiari hanno già nominato CTP. Chiedo attivazione polizza RC.",
        "Alla c.a. ufficio sinistri, Dr.ssa {medico}, ortopedico. Vi notifico errore chirurgico del {data}: rimossa protesi anca errata (dx invece di sx). Paziente informato della necessità di reintervento. Esprime rabbia e richiede spiegazioni formali. Allego relazione incident reporting.",
        "Spett.le compagnia, Dr. {medico}, interventista epatologo. Comunico complicanza iatrogena da biopsia epatica del {data}: emorragia massiva non controllata tempestivamente. Necessarie emotrasfusioni multiple. Paziente lamenta negligenza nella gestione emergenza. Richiedo valutazione sinistro.",
        "Oggetto: Sinistro oculistico - {data}. Sottoscritto Dr. {medico}, oftalmologo. Durante facoemulsificazione cataratta, caduta nucleo in camera vitrea con perdita funzione visiva permanente. Complicanza grave discussa con paziente che richiede risarcimento danni. Allego consenso informato e documentazione.",
        "Egregi Signori, Dr.ssa {medico}, neonatologa. Segnalo danno neurologico neonatale da uso improprio forcipe durante parto del {data}. Paralisi facciale permanente. I genitori contestano appropriatezza manovra ostetrica. Hanno già richiesto documentazione per perizia. Necessaria attivazione copertura.",
        "Spett.le ufficio, sono il Dr. {medico}, chirurgo generale. Comunico infezione grave post-operatoria del {data}: shock settico da strumenti non adeguatamente sterilizzati. Audit interno ha confermato deficit procedurale. Paziente ricoverato in TI per 15 giorni. Famiglia minaccia azioni legali.",
        "Alla Direzione sinistri, Dr. {medico}, chirurgo pediatrico. Vi informo di diagnosi tardiva appendicite acuta con peritonite in minore del {data}. Valutazione iniziale sottostimata. Genitori contestano ritardo diagnostico che ha messo a rischio vita del bambino. Allego tutta documentazione.",
        "Oggetto: Apertura pratica sinistro {data}. Dr.ssa {medico}, chirurgo plastico. Segnalo danno estetico permanente da mastoplastica: asimmetria grave e necrosi tissutale da errore nella pianificazione. Paziente molto insoddisfatta richiede revisione gratuita e risarcimento. Necessario vs parere.",
        "Spett.le compagnia, Dr. {medico}, nefrologo responsabile dialisi. Comunico evento gravissimo del {data}: utilizzo liquido dialisi contaminato con sepsi e arresto cardiaco paziente. Root cause analysis in corso. Famiglia ha già sporto denuncia penale. Urge attivazione copertura massimale.",
        "Egregi, sono il Dr. {medico}, responsabile blocco operatorio. Segnalo caduta paziente da barella durante trasferimento il {data}: trauma cranico e fratture multiple. Inchiesta interna ha evidenziato carenza personale. Famiglia richiede spiegazioni formali. Chiedo apertura sinistro.",
        "Alla c.a. ufficio, Dr.ssa {medico}, responsabile medicina trasfusionale. Comunico errore nel controllo pre-trasfusionale del {data}: sacca gruppo errato somministrata con emolisi grave e IRA. Paziente in prognosi riservata. Familiari assistiti da legale hanno chiesto sequestro documentazione.",
        "Spett.le assicurazione, Dr. {medico}, chirurgo generale. Vi notifico ustione chimica iatrogena del {data}: disinfettante lasciato su cute durante intervento con lesioni II grado. Paziente lamenta dolore persistente e chiede risarcimento per danno permanente. Allego foto lesioni.",
        "Oggetto: Sinistro ginecologico {data}. Sottoscritto Dr. {medico}, ginecologo. Devo comunicare isterectomia eseguita per errata interpretazione istologica: lesione era benigna. Paziente profondamente turbata per perdita utero evitabile. Ha già consultato tre legali. Necessaria immediata attivazione polizza.",
        "Egregi Signori, Dr.ssa {medico}, anestesista. Segnalo arresto respiratorio iatrogeno del {data} da sovradosaggio anestetico con danni cerebrali da ipossia. Errore nel calcolo posologico per peso. Famiglia informata richiede spiegazioni tecniche dettagliate. Chiedo supporto compagnia.",
        "Spett.le ufficio sinistri, Dr. {medico}, ortopedico artroscopista. Comunico lesione LCA iatrogena durante artroscopia diagnostica del {data}. Danno a struttura sana richiede ricostruzione chirurgica. Paziente atleta professionista valuta danno da interruzione carriera. Allego relazione.",
        "Alla Direzione, sono il Dr. {medico}, responsabile senologia. Vi informo di errore chirurgico grave del {data}: mastectomia eseguita su seno controlaterale sano. Marcatura pre-operatoria errata. Paziente sotto shock psicologico richiede risarcimento importante. Urge vs intervento.",
        "Oggetto: Sinistro ORL {data}. Dr.ssa {medico}, otorinolaringoiatra. Segnalo lesione nervo laringeo durante tiroidectomia con paralisi corde vocali permanente. Complicanza rara ma invalidante per paziente cantante professionista. Quantificazione danni molto elevata. Necessaria perizia assicurativa.",
        "Spett.le compagnia, Dr. {medico}, odontoiatra. Comunico complicanza odontoiatrica del {data}: perforazione ATM durante avulsione ottavo con danni permanenti. Paziente riferisce dolore cronico invalidante. Ha richiesto consulto maxillo-facciale e legale. Chiedo attivazione copertura RC professionale.",
        "Egregi, sottoscritto Dr. {medico}, rianimatore. Devo con grande dispiacere comunicare exitus paziente per embolia gassosa durante CVC il {data}. Tecnica di inserzione risultata non corretta da audit. Famiglia devastata ha già presentato esposto in Procura. Necessaria immediata gestione sinistro.",
        "Alla c.a. sinistri, Dr.ssa {medico}, ostetrica coordinatrice. Segnalo rottura uterina non diagnosticata tempestivamente durante travaglio del {data} con emorragia massiva materna. Esito favorevole ma paziente contesta ritardo riconoscimento. Allego CTG e documentazione completa caso.",
        "Spett.le ufficio, Dr. {medico}, oncologo medico. Vi informo di sovradosaggio chemioterapico del {data}: errore calcolo superficie corporea con tossicità multiorgano e neuropatia permanente. Paziente ricoverata in TI. Famiglia minaccia denuncia per lesioni gravissime. Urge apertura pratica.",
        "Oggetto: Sinistro neurochirurgico {data}. Sottoscritto Dr. {medico}, neurochirurgo. Comunico lesione midollare iatrogena durante discectomia con tetraplegia conseguente. Ho personalmente ammesso errore tecnico a famiglia. Paziente giovane, danni ingenti. Chiedo massima collaborazione compagnia.",
        "Egregi Signori, Dr.ssa {medico}, odontoiatra endodontista. Segnalo frattura strumento endodontico durante devitalizzazione del {data} con frammento irrecuperabile in osso mandibolare. Paziente riferisce dolore persistente e richiede risarcimento oltre a cure correttive. Allego radiografie.",
        "Spett.le assicurazione, Dr. {medico}, oculista. Comunico cecità bilaterale iatrogena da iniezione intravitreale errata del {data}: utilizzato farmaco chemioterapico invece di anti-VEGF per errore preparazione. Evento gravissimo. Paziente assistito da studio legale importante. Necessaria immediata gestione.",
        "Alla Direzione, sono il Dr. {medico}, geriatra responsabile RSA. Vi informo di decesso ospite per aspirazione durante alimentazione assistita il {data}. Paziente disfagico non rispettate indicazioni NPO. Familiari hanno richiesto sequestro cartella. Audit interno conferma responsabilità. Chiedo apertura sinistro.",
        "Oggetto: Sinistro ortopedico {data}. Dr.ssa {medico}, traumatologa. Segnalo frattura iatrogena durante osteosintesi: viti oversized hanno causato ulteriore danno osseo. Necessario reintervento. Paziente contesta appropriatezza tecnica chirurgica. Allego imaging pre e post operatorio.",
        "Spett.le compagnia, Dr. {medico}, gastroenterologo. Comunico perforazione esofagea durante EGDS del {data} con mediastinite e sepsi. Complicanza grave richiesto ricovero TI 3 settimane. Paziente stabilizzato ma lamenta conseguenze evitabili. Famiglia chiede spiegazioni dettagliate.",
        "Egregi, sottoscritto Dr. {medico}, elettrofisiologo. Vi notifico malfunzionamento pacemaker impiantato il {data}: parametri impostati erroneamente con episodi sincopali e arresto cardiaco. Necessaria sostituzione device. Paziente molto allarmato richiede garanzie e risarcimento. Allego scheda tecnica.",
        "Alla c.a. ufficio sinistri, Dr.ssa {medico}, neurologa. Segnalo complicanza da rachicentesi del {data}: ematoma epidurale con compressione midollare e paraparesi. Tecnica corretta ma evento avverso invalidante. Paziente richiede inquadramento responsabilità. Chiedo valutazione legale caso.",
        "Spett.le ufficio, Dr. {medico}, cardiochirurgo. Comunico utilizzo vena safena controlaterale durante bypass del {data}: prelievo da gamba sbagliata con insufficienza venosa iatrogena. Paziente lamenta doppio danno chirurgico. Ha già richiesto secondo parere. Necessaria attivazione polizza.",
        "Oggetto: Apertura sinistro {data}. Dr. {medico}, intensivista. Devo segnalare decesso per shock anafilattico da lattice nonostante allergia nota in anamnesi. Mancata verifica pre-operatoria. Familiari devastati hanno già sporto querela penale per omicidio colposo. Urge gestione legale caso."
    ]
    
    # Genera altre 200 varianti per arrivare a 250
    for i in range(200):
        templates_extra = [
            "Spett.le compagnia, Dr. {medico}. Segnalo evento avverso del {data} con richiesta danni da parte del paziente. Allego documentazione clinica per vs valutazione.",
            "Oggetto: Sinistro medico {data}. Sottoscritto Dr. {medico}. Comunico complicanza iatrogena con esiti invalidanti. Famiglia paziente ha manifestato intenzione di rivalsa legale.",
            "Egregi Signori, sono il Dr. {medico}. Vi notifico errore medico verificatosi il {data}. Il paziente è assistito da legale e richiede apertura pratica assicurativa.",
            "Alla Direzione Sinistri, Dr. {medico}. Comunico danno iatrogeno del {data} con conseguenze permanenti. Necessaria immediata attivazione copertura RC professionale."
        ]
        template = random.choice(templates_extra)
        medico = random.choice([
            "Rossi", "Bianchi", "Verdi", "Russo", "Ferrari", "Esposito", "Romano", 
            "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca"
        ])
        sinistri_iniziali.append(template.format(medico=medico, data="{data}"))
    
    for template in sinistri_iniziali[:250]:
        medico = random.choice([
            "Rossi", "Bianchi", "Verdi", "Russo", "Ferrari", "Esposito", "Romano", 
            "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca",
            "Mancini", "Costa", "Giordano", "Rizzo", "Lombardi", "Moretti", "Barbieri"
        ])
        emails.append({
            "testo": template.format(medico=medico, data=generate_random_date()),
            "tipologia": 0,
            "riferimento_temporale": 0
        })
    
    # ============================================================================
    # CATEGORIA 0-1: SINISTRI AVVENUTI - FOLLOW-UP (250 esempi)
    # ============================================================================
    
    # Template base per follow-up
    sinistri_followup_base = [
        "Rif. pratica {caso_id} - Dr. {medico}. Invio documentazione medica integrativa richiesta dal vs perito. Allego referto specialistico che conferma nesso causale tra procedura e danno lamentato dal paziente.",
        "In riferimento al sinistro {caso_id}, Dr.ssa {medico}. Vi aggiorno che il paziente è stato sottoposto a secondo intervento correttivo. La famiglia ha aggiornato la richiesta risarcitoria con nuove voci di danno.",
        "Oggetto: Integrazione pratica {caso_id}. Sottoscritto Dr. {medico}. Come richiesto invio cartella clinica completa e perizia medico-legale di parte che quantifica danno biologico permanente al 45%.",
        "Spett.le compagnia, rif. {caso_id} - Dr. {medico}. Comunico peggioramento condizioni cliniche paziente con necessità ricovero urgente per complicanze. Famiglia richiede aggiornamento valutazione danni.",
        "Pratica {caso_id}, Dr.ssa {medico}. Invio documentazione fotografica evoluzione lesioni e relazione consulente tecnico ospedaliero. Confermato danno estetico permanente come lamentato dalla paziente.",
    ]
    
    # Dizionari per variabilità
    aggiornamenti_clinici = [
        "il paziente ha sviluppato complicanza tardiva",
        "le condizioni cliniche sono peggiorate significativamente",
        "si è reso necessario ulteriore ricovero",
        "persistono gli esiti invalidanti lamentati",
        "è stato necessario nuovo intervento chirurgico",
        "il recupero funzionale è risultato parziale"
    ]
    
    sviluppi_legali = [
        "la famiglia ha depositato CTU presso il Tribunale",
        "è stata presentata querela penale in Procura",
        "l'ospedale ha ricevuto formale messa in mora",
        "è stato disposto sequestro della documentazione sanitaria",
        "sono state acquisite testimonianze del personale",
        "è in corso mediazione obbligatoria ex D.Lgs 28/2010"
    ]
    
    richieste_medico = [
        "Chiedo aggiornamento dello stato della pratica",
        "Necessito parere legale sulla gestione del caso",
        "Sollecito invio perito per sopralluogo",
        "Richiedo autorizzazione per proposta transattiva",
        "Necessaria vs valutazione sulla difendibilità",
        "Chiedo convocazione tavolo tecnico urgente"
    ]
    
    # Genera 250 follow-up con alta variabilità
    for i in range(250):
        medico = random.choice([
            "Rossi", "Bianchi", "Verdi", "Russo", "Ferrari", "Esposito", "Romano",
            "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti"
        ])
        
        if i < 50:
            template = random.choice(sinistri_followup_base)
            testo = template.format(caso_id=generate_case_id(), medico=medico)
        else:
            templates_variabili = [
                "Rif. {caso_id} - Dr. {medico}. Aggiorno che {aggiornamento_clinico}. {sviluppo_legale}. {richiesta}",
                "Pratica {caso_id}, Dr.ssa {medico}. Vi informo che {sviluppo_legale}. La famiglia ha presentato documentazione integrativa. {richiesta}",
                "Oggetto: Follow-up {caso_id}. Sottoscritto Dr. {medico}. {aggiornamento_clinico}. Il paziente ha formalizzato ulteriori contestazioni. Allego nuova documentazione.",
                "Spett.le ufficio, rif. {caso_id} - Dr. {medico}. Rispondo ai quesiti del vs consulente. {aggiornamento_clinico}. {richiesta}",
                "In merito a {caso_id}, Dr. {medico}. Invio relazione aggiornata: {aggiornamento_clinico}. {sviluppo_legale}. Resto a disposizione per chiarimenti."
            ]
            template = random.choice(templates_variabili)
            testo = template.format(
                caso_id=generate_case_id(),
                medico=medico,
                aggiornamento_clinico=random.choice(aggiornamenti_clinici),
                sviluppo_legale=random.choice(sviluppi_legali),
                richiesta=random.choice(richieste_medico)
            )
        
        emails.append({
            "testo": testo,
            "tipologia": 0,
            "riferimento_temporale": 1
        })
    
    # ============================================================================
    # CATEGORIA 1-0: CIRCOSTANZE POTENZIALI - FATTO INIZIALE (250 esempi)
    # ============================================================================
    circostanze_iniziali = [
        "Spett.le compagnia, Dr. {medico}, Risk Manager. Vi segnalo criticità rilevata durante audit: alcuni operatori non rispettano protocollo igiene mani. Temo possa generare infezioni nosocomiali e conseguenti richieste danni. Chiedo valutazione rischio potenziale.",
        "Oggetto: Segnalazione rischio clinico. Dr.ssa {medico}, Direttore Sanitario. Ho rilevato prescrizione contemporanea farmaci controindicati in cartella paziente. Intervenuta prima somministrazione ma segnalo per valutazione assicurativa rischio farmacologico in reparto.",
        "Egregi Signori, sono il Dr. {medico}, Primario Ortopedia. Nella cartella clinica di un paziente ho trovato annotazioni riferite ad altro paziente omonimo. Rischio elevato di errori terapeutici. Implementate azioni correttive ma segnalo per vostra conoscenza.",
        "Alla c.a. Risk Management, Dr. {medico}. Segnalo pavimento reparto costantemente bagnato con alto rischio cadute pazienti anziani. Già segnalato a direzione tecnica ma persiste. Temo possibile sinistro. Chiedo se necessarie azioni preventive dal punto di vista assicurativo.",
        "Spett.le ufficio, Dr.ssa {medico}, responsabile qualità. Un paziente mi ha segnalato che domani sarà operato da specializzando alla prima esperienza su quel tipo di intervento. Paziente preoccupato. Ho rassicurato ma segnalo potenziale contestazione futura.",
        "Oggetto: Segnalazione criticità. Dr. {medico}, Coordinatore DEA. Durante check pre-operatorio ho notato assenza raccolta allergie farmacologiche standardizzata. Potenziale rischio reazioni avverse non prevenibili. Chiedo se implementare nuova modulistica.",
        "Egregi, sottoscritto Dr. {medico}, responsabile reparto. Segnalo malfunzionamento sbarre di sicurezza in alcuni letti degenza. Già richiesta manutenzione ma temo cadute pazienti allettati nel frattempo. Vi informo per valutazione rischio assicurativo.",
        "Spett.le compagnia, Dr.ssa {medico}, chirurgo. Un paziente mi ha contestato che il consenso informato firmato ieri riguardava intervento diverso da quello ora programmato. Errore amministrativo corretto ma paziente sospettoso. Segnalo per vs conoscenza.",
        "Alla Direzione, Dr. {medico}, anestesista. Ho rilevato etichetta flebo con nome paziente diverso da quello della stanza. Infermiere ha confermato correttezza ma episodio ha allarmato familiari. Nessun danno ma segnalo potenziale contestazione.",
        "Oggetto: Alert rischio clinico. Dr. {medico}, Direttore UOC. Carenza cronica personale: pazienti allettati mobilizzati solo 1 volta/die con rischio lesioni da pressione. Ho segnalato a Direzione Generale ma temo future richieste danni. Necessaria vs valutazione.",
        "Spett.le ufficio, Dr.ssa {medico}, internista. Paziente politrattato con 15 farmaci/die. Consulente ha evidenziato rischio interazioni. Rivalutata terapia ma paziente ha espresso preoccupazione. Segnalo per documentazione rischio gestito.",
        "Egregi Signori, Dr. {medico}, farmacista ospedaliero. Durante controllo ho trovato farmaci scaduti in carrello reparto. Rimossi immediatamente ma segnalo per audit e valutazione se necessarie azioni preventive assicurative.",
        "Alla c.a. compagnia, Dr.ssa {medico}, responsabile informatica sanitaria. Sistema gestionale down per 48h: rischio prescrizioni non registrate. Ripristinato ma alcuni medici segnalano possibili incongruenze cartelle. Chiedo se aprire incident report formale.",
        "Spett.le ufficio, Dr. {medico}, Coordinatore infermieristico. Pulsante chiamata infermieri non funzionante in 3 stanze. Manutenzione programmata ma nel frattempo pazienti impossibilitati a chiamare in emergenza. Segnalo rischio potenziale.",
        "Oggetto: Segnalazione preventiva. Dr. {medico}, radiologo. Paziente contesta referto TAC definito 'non conclusivo'. Richiede ulteriori accertamenti pre-intervento. Ho disposto approfondimenti ma paziente diffidente. Potenziale futuro contenzioso.",
        "Egregi, sottoscritto Dr.ssa {medico}, responsabile sala operatoria. Strumenti chirurgici per intervento domani appoggiati su carrello scoperto in corridoio. Fatto rimuovere ma segnalo deficit procedurale. Temo contestazioni su sterilità.",
        "Spett.le compagnia, Dr. {medico}, legale rappresentante. Paziente lamenta consenso informato illeggibile. Effettivamente calligrafia poco chiara. Fornita copia dattiloscritta ma paziente ha espresso sfiducia. Segnalo per documentazione.",
        "Alla Direzione sinistri, Dr.ssa {medico}, responsabile degenze. Temperatura stanze costantemente sotto standard. Paziente immunodepresso teme maggior rischio infettivo. Sollecitata manutenzione ma segnalo lamentela formale ricevuta.",
        "Oggetto: Alert clinico. Dr. {medico}, diabetologo. Intervento paziente diabetica rinviato 3 volte. Prolungato digiuno potrebbe causare scompenso glicemico. Ho implementato protocollo ma paziente preoccupata. Segnalo potenziale contestazione gestione.",
        "Spett.le ufficio, Dr. {medico}, infettivologo. Infermiere ha posizionato accesso venoso senza disinfezione cutanea adeguata. Ho fatto rifare ma episodio osservato da familiari allarmati. Nessun danno ma segnalo per vs conoscenza.",
        "Egregi Signori, Dr.ssa {medico}, responsabile formazione. Specializzando ha eseguito TAC ripetute su stesso paziente. Supervisore ha dovuto intervenire. Familiari hanno chiesto spiegazioni su esposizione radiazioni. Chiarito ma segnalo diffidenza.",
        "Alla c.a. Risk Manager, Dr. {medico}, responsabile emergenze. Assenza segnaletica uscite sicurezza in reparto nuovo. In caso evacuazione rischio per pazienti allettati. Già segnalato a Direzione Lavori ma temo responsabilità su sicurezza.",
        "Spett.le compagnia, Dr.ssa {medico}, cardiologa. Monitor paziente critico allarma continuamente ma personale sottodimensionato non riesce a intervenire tempestivamente. Temo sottovalutazione rischi. Segnalo carenza organizzativa potenzialmente pericolosa.",
        "Oggetto: Segnalazione rischio. Dr. {medico}, geriatra. Paziente seguito da 4 specialisti con prescrizioni non coordinate. Rischio interazioni farmacologiche. Ho attivato consulto multidisciplinare ma paziente ha espresso preoccupazione. Documento situazione.",
        "Egregi, sottoscritto Dr. {medico}, chirurgo. Medicazione ferita chirurgica effettuata ogni 3 giorni per carenza materiale. Standard sarebbe quotidiano. Paziente teme infezione. Sollecitati approvvigionamenti ma segnalo deficit assistenziale.",
        "Spett.le ufficio, Dr.ssa {medico}, responsabile qualità. Defibrillatore reparto con spia malfunzionamento. Sostituzione programmata settimana prossima ma nel frattempo rischio in caso arresto cardiaco. Segnalo per valutazione copertura rischio.",
        "Alla Direzione, Dr. {medico}, Direttore Sanitario. Due interventi programmati stesso orario stessa sala. Errore gestionale corretto ma un paziente ha espresso timore che il suo sarà eseguito frettolosamente. Rassicurato ma segnalo diffidenza.",
        "Oggetto: Alert sicurezza. Dr.ssa {medico}, responsabile prevenzione. Bombole ossigeno in corridoio non ancorate a parete. Rischio caduta e incidenti. Fatto mettere in sicurezza ma segnalo deficit strutturale da risolvere definitivamente.",
        "Spett.le compagnia, Dr. {medico}, chirurgo. Domani devo operare ma ho sintomi influenzali. Ho informato paziente proponendo rinvio ma insiste per procedere. Accetto ma segnalo sua assunzione rischio contaminazione e possibile futura contestazione.",
        "Egregi Signori, Dr. {medico}, responsabile laboratorio. Scambio provette esami tra pazienti omonimi. Rilevato prima refertazione ma familiari presenti hanno assistito all'errore. Chiarito ma preoccupati per affidabilità. Segnalo incident.",
        "Alla c.a. ufficio, Dr.ssa {medico}, pneumologa. Saturimetro paziente dà letture variabili. Sostituito device ma nel frattempo familiari allarmati temono false sicurezze. Nessun danno ma segnalo sfiducia generata.",
        "Spett.le compagnia, Dr. {medico}, anestesista. Paziente mi ha contestato che non ho risposto esaustivamente a domande sui rischi anestesia. Ho integrato colloquio ma ha firmato consenso con riserve. Segnalo potenziale contestazione futura.",
        "Oggetto: Segnalazione preventiva. Dr. {medico}, oncologo. In sala attesa day hospital pazienti immunodepressi vicini a persone sintomatiche. Riorganizzati spazi ma alcuni pazienti hanno lamentato inadeguatezza protocolli anti-contagio.",
        "Egregi, sottoscritto Dr.ssa {medico}, responsabile PS. Paziente in attesa 6h in barella corridoio per sovraffollamento. Teme peggioramento condizioni. Ho garantito monitoraggio ma esprime insoddisfazione. Segnalo criticità organizzativa con potenziali implicazioni.",
        "Spett.le ufficio, Dr. {medico}, farmacista clinico. Infermiere ha preparato multiple siringhe senza etichettatura. Fatto correggere ma episodio visto da familiari che temono errori somministrazione. Rassicurati ma diffidenti.",
        "Alla Direzione sinistri, Dr. {medico}, responsabile igiene. Bagno stanza degenza non pulito da giorni per carenza personale ausiliario. Paziente lamenta rischio infettivo. Sollecitata pulizia straordinaria ma segnalo insoddisfazione.",
        "Oggetto: Alert farmacologico. Dr.ssa {medico}, internista. Prescritte compresse a paziente disfagico. Famiglia ha fatto notare inadeguatezza. Modificata prescrizione in formulazione liquida ma segnalo mancata valutazione iniziale che ha generato sfiducia.",
        "Spett.le compagnia, Dr. {medico}, responsabile medicina iperbarica. Porta camera iperbarica con difetto chiusura. Trattamenti sospesi ma alcuni pazienti hanno completato seduta con porta difettosa. Nessun incidente ma segnalo rischio corso.",
        "Egregi Signori, Dr. {medico}, ematologo. Paziente anemico sottoposto a prelievi ematici quotidiani. Famiglia contesta appropriatezza frequenza. Giustificata necessità clinica ma persistono dubbi. Segnalo contestazione protocollo diagnostico.",
        "Alla c.a. Risk Manager, Dr.ssa {medico}, responsabile pulizie. Personale usa stesso materiale per pavimenti e superfici pazienti. Richiamati su protocollo ma familiari hanno assistito. Timore contaminazione crociata. Segnalo deficit procedurale osservato.",
        "Spett.le ufficio, Dr. {medico}, diabetologo. Paziente diabetica riceve vassoi non conformi a dieta prescritta. Contestato più volte. Segnalato a ristorazione ma problema persiste. Temo responsabilità su scompenso glicemico.",
        "Oggetto: Segnalazione rischio infettivo. Dr. {medico}, urologo. Catetere vescicale in sede da 10 giorni oltre standard. Famiglia teme IVU. Programmata rimozione ma segnalo contestazione timing gestione device.",
        "Egregi, sottoscritto Dr.ssa {medico}, cardiologa. Sfigmomanometro reparto dà letture incoerenti. In attesa taratura. Nel frattempo familiari diffidenti su affidabilità monitoraggio PA. Nessun danno ma segnalo sfiducia dispositivi.",
        "Spett.le compagnia, Dr. {medico}, geriatra. Durante turno notte nessun controllo parametri vitali dalle 22 alle 6. Carenza personale. Famiglia ha espresso forte preoccupazione. Segnalo deficit assistenziale con potenziali implicazioni legali.",
        "Alla Direzione, Dr. {medico}, infettivologo. Personale usa stesso fonendoscopio su tutti pazienti senza disinfezione. Famiglia paziente immunodepresso allarmata. Forniti fonendoscopi monouso ma segnalo pratica scorretta osservata.",
        "Oggetto: Alert strutturale. Dr.ssa {medico}, ortopedica. Letto paziente scricchiola pericolosamente. Timore cedimento con conseguente caduta. Richiesta sostituzione urgente ma familiari molto preoccupati. Segnalo deficit manutenzione.",
        "Spett.le ufficio, Dr. {medico}, intensivista. Aria condizionata TI non funzionante. Compromesso controllo contaminazione ambientale. Manutenzione in corso ma familiari temono maggior rischio infettivo. Segnalo criticità impianti.",
        "Egregi Signori, Dr. {medico}, chirurgo. Usati guanti sterili con confezione già aperta per medicazione. Paziente ha contestato sterilità. Rifatta medicazione con materiale integro ma segnalo dubbi sollevati su procedure.",
        "Alla c.a. compagnia, Dr.ssa {medico}, infettivologa. Paziente con febbre persistente ma nessun approfondimento diagnostico per 4 giorni. Famiglia ha sollecitato. Ora prescritti esami ma segnalo insoddisfazione per ritardo percepito come negligente.",
        "Spett.le ufficio, Dr. {medico}, responsabile emotrasfusionale. Etichetta gruppo sanguigno cartella paziente discordante con quello comunicato. Verificato essere errore trascrizione, gruppo corretto. Ma paziente allarmato. Segnalo incident con impatto psicologico.",
        "Oggetto: Segnalazione preventiva. Dr. {medico}, rianimatore. Carrello emergenze aperto con farmaci mancanti. Ripristinato ma familiari presenti hanno notato. Timore inadeguatezza risposta emergenza. Nessun evento ma segnalo percezione negativa.",
        "Egregi, sottoscritto Dr.ssa {medico}, infettivologa. Paziente allocato in stanza con caso MRSA. Famiglia contesta rischio contagio. Giustificata necessità ma persistono timori. Segnalo contestazione appropriatezza gestione isolamenti.",
        "Spett.le compagnia, Dr. {medico}, responsabile tecnologie. Ventilatore meccanico stanza accanto emette rumori anomali da ore. Verificato funzionamento corretto ma familiari allarmati. Sostituito per precauzione ma segnalo allarme generato.",
        "Alla Direzione sinistri, Dr. {medico}, geriatra. Paziente trasferito 4 volte in 1 settimana tra reparti. Famiglia lamenta disagio e necessità ripetere anamnesi. Giustificata ottimizzazione posti letto ma segnalo insoddisfazione organizzativa.",
        "Oggetto: Alert dispositivi. Dr.ssa {medico}, chirurga. Sacchetto stomia paziente sempre troppo pieno. Famiglia contesta frequenza svuotamento inadeguata. Riorganizzato personale ma segnalo lamentela su qualità assistenza.",
        "Spett.le ufficio, Dr. {medico}, oncologo. Pompa infusionale chemio allarma ripetutamente. Personale silenzia senza verificare. Famiglia allarmata. Controllato corretto funzionamento ma segnalo gestione allarmi percepita come superficiale.",
        "Egregi Signori, Dr. {medico}, ortopedico. Paziente in dimissione ma non ancora autonomo nella deambulazione. Famiglia contesta prematurità. Garantito follow-up domiciliare ma persistono dubbi su appropriatezza timing dimissione."
    ]
    
    # Genera altre 200 varianti per arrivare a 250
    for i in range(200):
        templates_extra = [
            "Spett.le compagnia, Dr. {medico}. Segnalo situazione potenzialmente rischiosa nel mio reparto. Implementate azioni correttive ma ritengo opportuno informarvi per valutazione rischio assicurativo.",
            "Oggetto: Segnalazione preventiva. Dr. {medico}. Ho rilevato irregolarità procedurale che potrebbe generare contestazioni. Nessun danno verificato ma chiedo vs parere su gestione rischio.",
            "Egregi, Dr. {medico}. Paziente ha espresso preoccupazione per condizioni assistenziali. Ho fornito rassicurazioni ma segnalo potenziale insoddisfazione che potrebbe evolvere in reclamo.",
            "Alla c.a. Risk Management, Dr. {medico}. Durante audit ho rilevato criticità organizzativa. Avviate azioni correttive ma segnalo per documentazione e valutazione se necessarie ulteriori misure preventive."
        ]
        circostanze_iniziali.append(random.choice(templates_extra))
    
    for template in circostanze_iniziali[:250]:
        medico = random.choice([
            "Rossi", "Bianchi", "Verdi", "Russo", "Ferrari", "Esposito", "Romano",
            "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca"
        ])
        emails.append({
            "testo": template.format(medico=medico),
            "tipologia": 1,
            "riferimento_temporale": 0
        })
    
    # ============================================================================
    # CATEGORIA 1-1: CIRCOSTANZE POTENZIALI - FOLLOW-UP (250 esempi)
    # ============================================================================
    
    stati_evoluzione = [
        "la situazione persiste invariata nonostante solleciti",
        "registrato peggioramento della criticità segnalata",
        "parzialmente risolto ma permangono aspetti critici",
        "problema completamente eliminato grazie a vs intervento",
        "purtroppo si è verificato l'incidente che temevo",
        "altri colleghi confermano la stessa problematica"
    ]
    
    azioni_implementate = [
        "La Direzione ha avviato audit interno e azioni correttive",
        "Nessun intervento concreto è stato ancora implementato",
        "Sostituita tutta la strumentazione difettosa",
        "Erogata formazione specifica al personale",
        "Implementati nuovi protocolli operativi",
        "Situazione ancora in fase di monitoraggio"
    ]
    
    richieste_followup = [
        "Chiedo aggiornamento su copertura assicurativa rischio",
        "Necessito parere su opportunità chiusura segnalazione",
        "Sollecito vs intervento per risoluzione definitiva",
        "Vi ringrazio per supporto nella gestione criticità",
        "Chiedo se necessarie ulteriori azioni preventive",
        "Richiedo documentazione gestione rischio per audit"
    ]
    
    # Genera 250 follow-up circostanze potenziali
    for i in range(250):
        medico = random.choice([
            "Rossi", "Bianchi", "Verdi", "Russo", "Ferrari", "Esposito", "Romano",
            "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti"
        ])
        
        if i < 50:
            templates_base = [
                "Rif. segnalazione {caso_id} - Dr. {medico}. Vi aggiorno che la situazione da me segnalata persiste. Temo evoluzione in sinistro conclamato. Chiedo vs supporto per sollecito Direzione.",
                "In merito a segnalazione {caso_id}, Dr.ssa {medico}. Comunico che problema non ancora risolto. Familiari paziente sempre più insofferenti. Temo formale reclamo imminente.",
                "Oggetto: Follow-up {caso_id}. Sottoscritto Dr. {medico}. Positivo riscontro: criticità segnalata completamente risolta. Nessuna contestazione da pazienti. Vi ringrazio per celere intervento.",
                "Spett.le compagnia, rif. {caso_id} - Dr. {medico}. Purtroppo devo comunicare che si è verificato l'incidente che avevo paventato. Per fortuna senza gravi conseguenze ma conferma validità mia segnalazione preventiva.",
                "Pratica {caso_id}, Dr.ssa {medico}. Aggiorno che situazione parzialmente migliorata ma persistono criticità residue. Continuo monitoraggio. Chiedo se mantenere aperta segnalazione."
            ]
            testo = random.choice(templates_base).format(caso_id=generate_case_id(), medico=medico)
        else:
            templates_variabili = [
                "Rif. {caso_id} - Dr. {medico}. Aggiorno: {stato_evoluzione}. {azione_implementata}. {richiesta}",
                "Segnalazione {caso_id}, Dr.ssa {medico}. Vi informo che {stato_evoluzione}. Familiari hanno formalizzato lamentela scritta. {richiesta}",
                "Oggetto: Follow-up {caso_id}. Dr. {medico}. {stato_evoluzione}. {azione_implementata}. Documento per vs archivio gestione rischio.",
                "Spett.le ufficio, caso {caso_id} - Dr. {medico}. {azione_implementata}. Tuttavia {stato_evoluzione}. {richiesta}",
                "In merito a {caso_id}, Dr.ssa {medico}. {stato_evoluzione}. Audit interno ha confermato criticità. {azione_implementata}. {richiesta}"
            ]
            template = random.choice(templates_variabili)
            testo = template.format(
                caso_id=generate_case_id(),
                medico=medico,
                stato_evoluzione=random.choice(stati_evoluzione),
                azione_implementata=random.choice(azioni_implementate),
                richiesta=random.choice(richieste_followup)
            )
        
        emails.append({
            "testo": testo,
            "tipologia": 1,
            "riferimento_temporale": 1
        })
    
    # Converti in DataFrame
    df = pd.DataFrame(emails)
    
    # Mescola il dataset per evitare che sia ordinato per categoria
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df

def get_category_names():
    """Restituisce i nomi delle categorie per entrambe le dimensioni."""
    return {
        "tipologia": {
            0: "Sinistro Avvenuto",
            1: "Circostanza Potenziale"
        },
        "riferimento_temporale": {
            0: "Fatto Iniziale",
            1: "Follow-up"
        }
    }

def get_combined_category_name(tipologia, riferimento_temporale):
    """Restituisce il nome della categoria combinata."""
    categories = get_category_names()
    return f"{categories['tipologia'][tipologia]} - {categories['riferimento_temporale'][riferimento_temporale]}"

def get_dataset_statistics(df):
    """Restituisce statistiche dettagliate sul dataset."""
    stats = {
        "totale_email": len(df),
        "per_tipologia": {
            "sinistri_avvenuti": len(df[df['tipologia'] == 0]),
            "circostanze_potenziali": len(df[df['tipologia'] == 1])
        },
        "per_riferimento": {
            "fatti_iniziali": len(df[df['riferimento_temporale'] == 0]),
            "followup": len(df[df['riferimento_temporale'] == 1])
        },
        "per_combinazione": {
            "sinistro_iniziale": len(df[(df['tipologia'] == 0) & (df['riferimento_temporale'] == 0)]),
            "sinistro_followup": len(df[(df['tipologia'] == 0) & (df['riferimento_temporale'] == 1)]),
            "circostanza_iniziale": len(df[(df['tipologia'] == 1) & (df['riferimento_temporale'] == 0)]),
            "circostanza_followup": len(df[(df['tipologia'] == 1) & (df['riferimento_temporale'] == 1)])
        },
        "lunghezza_testo": {
            "media": df['testo'].str.len().mean(),
            "minima": df['testo'].str.len().min(),
            "massima": df['testo'].str.len().max(),
            "mediana": df['testo'].str.len().median()
        }
    }
    return stats

def export_to_csv(df, filename="dataset_medical_provider_1000.csv"):
    """Esporta il dataset in formato CSV."""
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✅ Dataset esportato in: {filename}")

def split_train_test(df, test_size=0.2, random_state=42):
    """Divide il dataset in training e test set mantenendo le proporzioni."""
    from sklearn.model_selection import train_test_split
    
    # Crea una colonna combinata per stratificazione
    df['combined_label'] = df['tipologia'].astype(str) + '_' + df['riferimento_temporale'].astype(str)
    
    train_df, test_df = train_test_split(
        df, 
        test_size=test_size, 
        random_state=random_state,
        stratify=df['combined_label']
    )
    
    # Rimuovi la colonna temporanea
    train_df = train_df.drop('combined_label', axis=1)
    test_df = test_df.drop('combined_label', axis=1)
    
    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)

if __name__ == "__main__":
    # Genera dataset
    df = create_mock_dataset()
    stats = get_dataset_statistics(df)
    
    print("=" * 80)
    print("DATASET EMAIL - PROSPETTIVA MEDICO/OSPEDALE (ASSICURATO)")
    print("CLASSIFICAZIONE MULTI-DIMENSIONALE SINISTRI MEDICAL MALPRACTICE")
    print("=" * 80)
    
    print(f"\n📊 STATISTICHE GENERALI:")
    print(f"   • Totale email: {stats['totale_email']}")
    print(f"   • Mittente: Sempre medico/struttura sanitaria (assicurato)")
    
    print(f"\n📋 DISTRIBUZIONE PER TIPOLOGIA:")
    print(f"   • Sinistri Avvenuti: {stats['per_tipologia']['sinistri_avvenuti']} ({stats['per_tipologia']['sinistri_avvenuti']/stats['totale_email']*100:.1f}%)")
    print(f"   • Circostanze Potenziali: {stats['per_tipologia']['circostanze_potenziali']} ({stats['per_tipologia']['circostanze_potenziali']/stats['totale_email']*100:.1f}%)")
    
    print(f"\n⏰ DISTRIBUZIONE PER RIFERIMENTO TEMPORALE:")
    print(f"   • Fatti Iniziali: {stats['per_riferimento']['fatti_iniziali']} ({stats['per_riferimento']['fatti_iniziali']/stats['totale_email']*100:.1f}%)")
    print(f"   • Follow-up: {stats['per_riferimento']['followup']} ({stats['per_riferimento']['followup']/stats['totale_email']*100:.1f}%)")
    
    print(f"\n🔀 DISTRIBUZIONE PER COMBINAZIONE:")
    print(f"   • Sinistro Avvenuto - Fatto Iniziale: {stats['per_combinazione']['sinistro_iniziale']}")
    print(f"   • Sinistro Avvenuto - Follow-up: {stats['per_combinazione']['sinistro_followup']}")
    print(f"   • Circostanza Potenziale - Fatto Iniziale: {stats['per_combinazione']['circostanza_iniziale']}")
    print(f"   • Circostanza Potenziale - Follow-up: {stats['per_combinazione']['circostanza_followup']}")
    
    print(f"\n📝 LUNGHEZZA TESTI:")
    print(f"   • Media: {stats['lunghezza_testo']['media']:.0f} caratteri")
    print(f"   • Mediana: {stats['lunghezza_testo']['mediana']:.0f} caratteri")
    print(f"   • Minima: {stats['lunghezza_testo']['minima']} caratteri")
    print(f"   • Massima: {stats['lunghezza_testo']['massima']} caratteri")
    
    print(f"\n📧 ESEMPI PER CATEGORIA:")
    
    categories = [
        (0, 0, "Sinistro Avvenuto - Fatto Iniziale (Medico segnala danno verificato)"),
        (0, 1, "Sinistro Avvenuto - Follow-up (Medico aggiorna su evoluzione)"),
        (1, 0, "Circostanza Potenziale - Fatto Iniziale (Medico segnala rischio)"),
        (1, 1, "Circostanza Potenziale - Follow-up (Medico aggiorna su situazione rischio)")
    ]
    
    for tip, rif, label in categories:
        print(f"\n   ▸ {label}:")
        sample = df[(df['tipologia'] == tip) & (df['riferimento_temporale'] == rif)].head(2)
        for idx, row in sample.iterrows():
            print(f"      • {row['testo'][:150]}...")
    
    # Split train/test
    train_df, test_df = split_train_test(df)
    
    print(f"\n📦 SPLIT DATASET:")
    print(f"   • Training set: {len(train_df)} email (80%)")
    print(f"   • Test set: {len(test_df)} email (20%)")
    
    print("\n" + "=" * 80)
    print("✅ Dataset generato con successo!")
    print("💡 Prospettiva: Medico/Ospedale → Compagnia Assicurativa")
    print("💡 Utilizzabile per classificazione multi-label o multi-output")
    print("=" * 80)
    
    # Esporta i dataset
    export_to_csv(df, "dataset_medical_provider_complete.csv")
    export_to_csv(train_df, "dataset_medical_provider_train.csv")
    export_to_csv(test_df, "dataset_medical_provider_test.csv")