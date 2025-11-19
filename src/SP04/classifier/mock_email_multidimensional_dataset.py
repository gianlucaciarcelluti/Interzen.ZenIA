"""
Dataset mock di email per classificazione sinistri medical malpractice.
Versione espansa: 1000 email totali con classificazione multi-dimensionale

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
    return f"SIN{random.randint(10000, 99999)}"

def create_mock_dataset():
    """Crea un dataset di 1000 email simulate per training e testing."""
    
    emails = []
    
    # ============================================================================
    # CATEGORIA 0-0: SINISTRI AVVENUTI - FATTO INIZIALE (250 esempi)
    # ============================================================================
    sinistri_iniziali = [
        "Buongiorno, vi scrivo per segnalare un grave errore chirurgico avvenuto il {data}. Durante l'intervento al ginocchio sinistro, il chirurgo ha operato per errore il ginocchio destro sano. Richiedo immediato risarcimento danni.",
        "Gentili Signori, mio padre è deceduto il {data} a seguito di una diagnosi errata di polmonite quando invece si trattava di embolia polmonare. Allego documentazione medica completa.",
        "Con la presente comunico che in data {data} mia madre ha subito un danno permanente da farmaco somministrato erroneamente dall'ospedale San Raffaele. Necessito avviare pratica di risarcimento.",
        "Spett.le compagnia, il {data} durante il parto cesareo è stato lesionato il nervo sciatico di mia moglie causando paralisi parziale della gamba sinistra. Inoltro richiesta danni.",
        "Oggetto: Sinistro del {data} - Infezione post-operatoria. A seguito di intervento di appendicectomia si è sviluppata grave infezione nosocomiale che ha richiesto tre ulteriori ricoveri.",
        "Vi contatto per un caso di malasanità verificatosi il {data} presso la clinica Villa Maria. Errata posologia del farmaco anticoagulante ha causato emorragia cerebrale a mio fratello.",
        "Buonasera, in data {data} il radiologo ha mancato di rilevare una massa tumorale visibile nella TAC. Il ritardo diagnostico di 6 mesi ha compromesso le possibilità di guarigione.",
        "Segnalo caduta accidentale dal letto ospedaliero avvenuta il {data} con frattura del femore. Il paziente non era stato dotato delle protezioni laterali obbligatorie.",
        "Richiesta risarcimento per ustioni di terzo grado subite durante intervento laparoscopico del {data}. Lo strumento elettrochirurgico ha causato perforazione intestinale.",
        "Il {data} mia figlia neonata ha subito lesioni cerebrali permanenti durante il parto per asfissia prolungata. Il personale ha ritardato il cesareo d'urgenza necessario.",
        "Comunico sinistro del {data}: scambio di paziente in sala operatoria. Mio padre è stato sottoposto ad intervento cardiaco destinato ad altro paziente omonimo.",
        "Gentili, il {data} durante colonscopia si è verificata perforazione del colon con conseguente peritonite e intervento chirurgico d'urgenza. Chiedo apertura pratica.",
        "Vi scrivo per segnalare che il {data} è stata somministrata trasfusione di sangue incompatibile a mia madre, causando shock anafilattico e danni renali permanenti.",
        "Oggetto: Danno da parto - {data}. Frattura della clavicola del neonato durante manovra estrattiva troppo vigorosa. Documentazione ospedaliera allegata.",
        "Il giorno {data} mio marito è stato dimesso dal pronto soccorso con diagnosi di gastrite. In realtà aveva un infarto in corso ed è deceduto due ore dopo a casa.",
        "Richiesta danni per amputazione errata arto superiore sinistro avvenuta il {data}. Il consenso informato era per arto destro ma il chirurgo ha sbagliato lato.",
        "In data {data} durante anestesia spinale l'ago è penetrato troppo in profondità causando lesione midollare con paraplegia. Necessito assistenza legale immediata.",
        "Buongiorno, segnalo reazione allergica fatale ad antibiotico somministrato il {data} nonostante allergia nota fosse riportata in cartella clinica. Mia sorella è deceduta.",
        "Il {data} è stata rimossa la protesi d'anca sbagliata (destra invece di sinistra). Ora necessito ulteriore intervento con rischi aggiuntivi e lunghi tempi di recupero.",
        "Comunico che il {data} durante biopsia epatica si è verificata emorragia interna massiva non controllata tempestivamente, con necessità di emotrasfusioni multiple.",
        "Oggetto: Sinistro oculistico {data}. Durante intervento di cataratta il cristallino è caduto nel vitreo causando perdita permanente della vista all'occhio destro.",
        "Vi scrivo per danno neurologico da parto avvenuto il {data}. L'uso improprio del forcipe ha causato paralisi facciale permanente al neonato.",
        "In data {data} ho subito shock settico per strumenti chirurgici non sterili utilizzati durante intervento di ernia. Ricovero in terapia intensiva per 15 giorni.",
        "Segnalo omessa diagnosi di appendicite acuta il {data} con conseguente peritonite e sepsi. Mio figlio ha rischiato la vita per la negligenza del medico di guardia.",
        "Richiesta risarcimento per danno estetico permanente da intervento di mastoplastica del {data}. Asimmetria grave e necrosi tissutale da errore tecnico.",
        "Il {data} durante dialisi è stato utilizzato liquido di dialisi contaminato causando grave infezione sistemica con shock settico e arresto cardiaco.",
        "Comunico caduta da barella durante trasferimento in sala operatoria avvenuta il {data} con trauma cranico e fratture multiple. Il personale era insufficiente.",
        "Oggetto: Errore trasfusionale {data}. Sacca di sangue destinata ad altro paziente somministrata a mio padre causando grave emolisi e insufficienza renale acuta.",
        "Vi scrivo per segnalare ustione chimica da disinfettante lasciato sulla cute durante intervento chirurgico del {data}. Lesioni di secondo grado su coscia sinistra.",
        "In data {data} mia madre è stata sottoposta ad isterectomia non necessaria per errata interpretazione dell'esame istologico. La lesione era benigna.",
        "Segnalo errore anestesiologico del {data}. Dosaggio eccessivo di anestetico ha causato arresto respiratorio e danni cerebrali da ipossia prolungata.",
        "Il {data} durante artroscopia del ginocchio è stato danneggiato il legamento crociato anteriore sano. Necessaria ricostruzione chirurgica aggiuntiva.",
        "Comunico che in data {data} è stata eseguita mastectomia sul seno sbagliato. La paziente aveva tumore al seno destro, operato invece il sinistro sano.",
        "Richiesta danni per paralisi delle corde vocali avvenuta il {data} durante tiroidectomia. Il nervo laringeo ricorrente è stato lesionato irreversibilmente.",
        "Oggetto: Sinistro dentale {data}. Durante estrazione del dente del giudizio è stata perforata l'articolazione temporo-mandibolare con danni permanenti.",
        "Il {data} mio padre è deceduto per embolia gassosa durante intervento di cateterismo venoso centrale. Tecnica di inserzione non corretta.",
        "Segnalo che in data {data} durante parto vaginale si è verificata rottura d'utero non diagnosticata tempestivamente con grave emorragia materna.",
        "Vi scrivo per danno da chemioterapia sovradosata somministrata il {data}. Mia moglie ha sviluppato insufficienza multiorgano e neuropatia permanente.",
        "Il {data} durante intervento di ernia discale è stato lesionato il midollo spinale causando tetraplegia. Il neurochirurgo ha ammesso l'errore tecnico.",
        "Comunico sinistro odontoiatrico del {data}. Durante devitalizzazione lo strumento endodontico si è spezzato e conficcato nell'osso mandibolare.",
        "Richiesta risarcimento per cecità bilaterale causata da iniezione intravitreale errata eseguita il {data}. Utilizzo di farmaco sbagliato invece di anti-VEGF.",
        "In data {data} mia nonna è deceduta per aspirazione polmonare durante alimentazione. Era in coma e il personale ha ignorato il divieto di alimentazione orale.",
        "Oggetto: Errore ortopedico {data}. Durante intervento di osteosintesi sono state utilizzate viti di dimensione errata causando frattura iatrogena.",
        "Il {data} durante endoscopia digestiva si è verificata perforazione esofagea con mediastinite e sepsi. Ricovero in rianimazione per 3 settimane.",
        "Segnalo che il {data} è stato impiantato pacemaker con parametri errati. Mio padre ha avuto arresto cardiaco e necessita sostituzione del dispositivo.",
        "Vi contatto per danno neurologico da puntura lombare traumatica del {data}. Ematoma epidurale spinale con compressione midollare e paraparesi.",
        "Il {data} durante intervento di bypass coronarico è stata utilizzata vena safena sbagliata. L'altra gamba ora presenta insufficienza venosa grave.",
        "Comunico morte perioperatoria avvenuta il {data} per shock anafilattico da lattice. L'allergia era nota ma non sono stati usati guanti latex-free.",
        "Richiesta danni per perdita dell'udito bilaterale causata da farmaci ototossici somministrati il {data} nonostante insufficienza renale nota del paziente.",
        "In data {data} durante posizionamento di drenaggio toracico è stato perforato il polmone causando pneumotorace iperteso e arresto cardiorespiratorio."
    ]
    
    # Genera altre 200 varianti per arrivare a 250
    for i in range(200):
        templates_extra = [
            "Oggetto: Sinistro medico {data}. Durante procedura diagnostica si è verificato danno iatrogeno con conseguenze permanenti per il paziente.",
            "Segnalo grave errore medico avvenuto il {data}. Necessito aprire immediatamente pratica assicurativa per i danni subiti da mio familiare.",
            "In data {data} si è verificato evento avverso durante trattamento ospedaliero. Allego tutta la documentazione clinica per valutazione del caso.",
            "Richiesta risarcimento per complicanza iatrogena del {data}. Il danno subito ha comportato invalidità permanente e necessità di ulteriori interventi."
        ]
        sinistri_iniziali.append(random.choice(templates_extra))
    
    for template in sinistri_iniziali[:250]:
        emails.append({
            "testo": template.format(data=generate_random_date()),
            "tipologia": 0,  # Sinistro Avvenuto
            "riferimento_temporale": 0  # Fatto Iniziale
        })
    
    # ============================================================================
    # CATEGORIA 0-1: SINISTRI AVVENUTI - FOLLOW-UP (250 esempi)
    # ============================================================================
    sinistri_followup = [
        "Rif. pratica {caso_id}: invio ulteriore documentazione medica richiesta. Allego referto specialistico che conferma nesso causale tra intervento del {data} e danno permanente subito.",
        "In riferimento al sinistro {caso_id} comunicato in precedenza, vi informo che mio padre è stato sottoposto a secondo intervento correttivo. Aggiorno la richiesta di risarcimento con nuove spese mediche.",
        "Oggetto: Integrazione pratica {caso_id}. Come richiesto invio copia della cartella clinica completa e perizia medico-legale che quantifica il danno biologico permanente.",
        "Buongiorno, con riferimento alla mia precedente del {data} relativa al caso {caso_id}, vi comunico che le condizioni di salute di mia madre sono peggiorate. Necessario ricovero urgente per complicanze.",
        "Pratica {caso_id}: invio documentazione fotografica delle lesioni e relazione del consulente tecnico di parte. Il danno estetico è permanente come da perizia allegata.",
        "In merito al sinistro {caso_id} segnalato, aggiorno che mio figlio ha dovuto interrompere l'attività lavorativa. Allego certificazione per danno da lucro cessante.",
        "Rif. {caso_id}: rispondo alla vostra richiesta di chiarimenti. L'evento si è verificato esattamente come descritto nella denuncia iniziale. Allego testimonianza scritta del personale presente.",
        "Oggetto: Follow-up caso {caso_id}. Le analisi di laboratorio appena ricevute confermano l'errore farmacologico. Invio referto tossicologico e consulenza farmacologica.",
        "Con riferimento al sinistro {caso_id}, comunico che è stato necessario terzo ricovero ospedaliero per gestione complicanze. Aggiorno il conteggio delle spese mediche sostenute.",
        "Pratica {caso_id}: come anticipato telefonicamente, allego sentenza del tribunale che riconosce responsabilità medica. La perizia d'ufficio conferma il nesso causale.",
        "In riferimento al caso {caso_id}, vi informo che mio padre ha ottenuto riconoscimento di invalidità permanente al 75%. Allego verbale della commissione medica.",
        "Rif. sinistro {caso_id}: invio aggiornamento sullo stato di salute. Purtroppo le terapie riabilitative non hanno dato i risultati sperati. Il danno neurologico è irreversibile.",
        "Oggetto: Integrazione documentale pratica {caso_id}. Allego seconda opinione medica richiesta dalla compagnia. Anche il secondo specialista conferma l'errore chirurgico.",
        "Con riferimento alla pratica {caso_id}, comunico che abbiamo ricevuto richiesta di risarcimento anche dall'INAIL per infortunio sul lavoro. Coordinate con il vs ufficio legale.",
        "Pratica {caso_id}: invio fatture e ricevute delle spese mediche sostenute negli ultimi tre mesi come da vs richiesta. Totale aggiornato in allegato.",
        "In merito al sinistro {caso_id}, vi comunico che mia moglie ha iniziato percorso psicoterapeutico per elaborazione trauma. Allego certificazione per danno psicologico.",
        "Rif. {caso_id}: aggiornamento sulle condizioni cliniche. Purtroppo si è resa necessaria ulteriore chirurgia correttiva. Allego preventivo e consenso informato del nuovo intervento.",
        "Oggetto: Caso {caso_id} - Documentazione integrativa. Come richiesto invio cartelle cliniche di tutti i ricoveri successivi all'evento avverso iniziale.",
        "Con riferimento al sinistro {caso_id} del {data}, vi comunico che il paziente è deceduto ieri per complicanze tardive. Richiedo aggiornamento della pratica a exitus.",
        "Pratica {caso_id}: invio relazione del medico legale di parte che quantifica il danno complessivo. Richiesta di risarcimento aggiornata a €350.000.",
        "In merito al caso {caso_id}, allego documentazione fotografica dell'evoluzione delle lesioni come richiesto dal perito assicurativo durante il sopralluogo.",
        "Rif. sinistro {caso_id}: comunico che abbiamo depositato querela penale presso la Procura. Allego copia della denuncia per vs conoscenza e coordinamento.",
        "Oggetto: Follow-up pratica {caso_id}. Invio aggiornamento: mio padre è stato trasferito in struttura riabilitativa specializzata. Allego preventivo dei costi di degenza.",
        "Con riferimento al caso {caso_id}, rispondo ai quesiti del vs consulente. Confermo che non vi erano patologie pregresse che potessero causare tale complicanza.",
        "Pratica {caso_id}: aggiorno che è stato necessario coinvolgere ulteriore specialista. Allego consulenza neurochirurgica che conferma errore tecnico durante intervento.",
        "In merito al sinistro {caso_id}, comunico che mia madre ha ottenuto riconoscimento legge 210/92 per danno da trasfusione. Allego delibera ministeriale.",
        "Rif. {caso_id}: invio documentazione richiesta dal perito. Allego diario clinico completo e dichiarazioni del personale sanitario che ha assistito al fatto.",
        "Oggetto: Integrazione caso {caso_id}. Come anticipato, allego perizia cinematica che ricostruisce dinamica della caduta e conferma assenza di protezioni laterali.",
        "Con riferimento alla pratica {caso_id}, vi informo che sono emersi ulteriori elementi probatori. Allego email interna dell'ospedale che ammette l'errore.",
        "Pratica {caso_id}: aggiornamento spese legali. Allego parcelle dei consulenti tecnici di parte e copie delle spese vive sostenute per accertamenti.",
        "In merito al sinistro {caso_id}, comunico che il Tribunale ha disposto CTU. Il perito d'ufficio ha richiesto tutta la documentazione che vi invio in copia.",
        "Rif. {caso_id}: rispondo alla richiesta di chiarimenti su cronologia eventi. Allego timeline dettagliata con orari precisi di ogni intervento sanitario.",
        "Oggetto: Follow-up pratica {caso_id}. Vi informo che mio figlio dovrà sottoporsi a ulteriore intervento chirurgico. Allego relazione specialistica e preventivo.",
        "Con riferimento al caso {caso_id}, allego referto autoptico che conferma morte causata da errore terapeutico. La perizia esclude concause naturali.",
        "Pratica {caso_id}: invio aggiornamento stato psicologico del paziente. Allego certificazione di disturbo post-traumatico da stress conseguente all'evento.",
        "In merito al sinistro {caso_id}, comunico che abbiamo completato gli accertamenti richiesti. Allego tutti i referti di imaging e analisi di laboratorio.",
        "Rif. {caso_id}: aggiorno che mia madre è stata ricoverata nuovamente per complicanza tardiva dell'intervento. Siamo al quinto ricovero in sei mesi.",
        "Oggetto: Integrazione documentale {caso_id}. Invio testimonianza di altro paziente presente in corsia che ha assistito all'errore nella somministrazione farmaci.",
        "Con riferimento alla pratica {caso_id}, allego documentazione che prova omissione di intervento tempestivo. I tempi di attesa sono documentati in cartella.",
        "Pratica {caso_id}: come richiesto invio documentazione delle spese per adattamento domestico. Mio padre paraplegico necessita eliminazione barriere architettoniche.",
        "In merito al caso {caso_id}, vi informo che è stata disposta perizia collegiale. Allego nomina dei tre specialisti che valuteranno il danno permanente.",
        "Rif. sinistro {caso_id}: aggiornamento terapie. Allego prescrizioni di tutti i farmaci assunti per gestione dolore cronico conseguente all'errore medico.",
        "Oggetto: Follow-up {caso_id}. Invio relazione fisioterapista che certifica mancato recupero funzionale nonostante intenso percorso riabilitativo.",
        "Con riferimento al caso {caso_id}, comunico che abbiamo ottenuto cartella clinica completa dopo diffida legale. Emergono omissioni nelle annotazioni.",
        "Pratica {caso_id}: allego seconda perizia medico-legale richiesta dalla compagnia. Anche questa conferma nesso causale e quantifica danno biologico al 60%.",
        "In merito al sinistro {caso_id}, vi informo che mia moglie ha dovuto lasciare il lavoro. Allego certificazione di inidoneità permanente allo svolgimento mansioni.",
        "Rif. {caso_id}: invio aggiornamento sulle condizioni. Purtroppo l'infezione è cronicizzata e necessita terapia antibiotica a tempo indeterminato.",
        "Oggetto: Integrazione pratica {caso_id}. Allego relazione dello psichiatra che certifica sindrome ansioso-depressiva conseguente al trauma subito.",
        "Con riferimento al caso {caso_id}, comunico che il paziente è stato trasferito in hospice. Le cure sono ora esclusivamente palliative.",
        "Pratica {caso_id}: invio documentazione aggiornata delle spese. Allego anche fatture per assistenza domiciliare infermieristica che si renderà necessaria a vita."
    ]
    
    # Genera altre 200 varianti per arrivare a 250
    for i in range(200):
        templates_extra = [
            "Rif. pratica {caso_id}: invio ulteriore documentazione richiesta dal perito assicurativo. Allego referto aggiornato sulle condizioni cliniche attuali.",
            "In merito al sinistro {caso_id}, comunico peggioramento quadro clinico. Necessario aggiornare la valutazione del danno permanente.",
            "Oggetto: Follow-up {caso_id}. Come anticipato telefonicamente, invio documentazione integrativa richiesta per completamento istruttoria.",
            "Con riferimento al caso {caso_id}, allego nuovi elementi probatori emersi che confermano responsabilità sanitaria."
        ]
        sinistri_followup.append(random.choice(templates_extra))
    
    for template in sinistri_followup[:250]:
        emails.append({
            "testo": template.format(caso_id=generate_case_id(), data=generate_random_date()),
            "tipologia": 0,  # Sinistro Avvenuto
            "riferimento_temporale": 1  # Follow-up
        })
    
    # ============================================================================
    # CATEGORIA 1-0: CIRCOSTANZE POTENZIALI - FATTO INIZIALE (250 esempi)
    # ============================================================================
    circostanze_iniziali = [
        "Gentili, vorrei segnalare che durante il ricovero di mio padre ho notato che alcuni infermieri non si lavano le mani tra un paziente e l'altro. Temo possa causare infezioni.",
        "Buongiorno, sono preoccupata perché il medico ha prescritto due farmaci a mia madre che secondo il foglietto illustrativo non andrebbero assunti insieme. Cosa devo fare?",
        "Vi scrivo perché nella cartella clinica di mio marito ci sono annotazioni riferite ad un altro paziente. Potrebbe generare confusione e rischi per la terapia futura?",
        "Segnalo che il pavimento del reparto ortopedia è sempre bagnato e scivoloso. Mio padre anziano ha rischiato di cadere più volte. Vorrei che interveniste preventivamente.",
        "Sono preoccupato: il chirurgo che dovrà operare mia figlia domani ha detto che non ha mai eseguito questo intervento prima. È normale? Posso cambiare chirurgo?",
        "Durante la visita pre-operatoria nessuno ha chiesto a mia madre se è allergica a qualche farmaco. Non dovrebbe essere una domanda standard per evitare problemi?",
        "Vorrei segnalare che le sbarre laterali del letto di mio padre non funzionano bene. È allettato e potrebbe cadere. Come posso richiedere la sostituzione del letto?",
        "Buonasera, il medico ha detto che farà un intervento diverso da quello per cui abbiamo firmato il consenso informato. Non dovrei firmare un nuovo documento?",
        "Sono preoccupata perché ho visto che l'etichetta sulla sacca della flebo di mia sorella porta un nome diverso dal suo. L'infermiere dice che è giusto, ma ho dubbi.",
        "Segnalo che in reparto c'è carenza cronica di personale. I pazienti allettati vengono cambiati di posizione solo una volta al giorno rischiando piaghe da decubito.",
        "Vorrei capire se è normale che mio padre prenda 15 farmaci diversi al giorno. Il medico di base ha detto che potrebbero esserci interazioni pericolose.",
        "Durante il ricovero ho notato che le date di scadenza di alcuni farmaci nel carrello sono superate. A chi devo segnalarlo per evitare che vengano somministrati?",
        "Gentili, il sistema informatico dell'ospedale è andato in tilt per 2 giorni. Temo che le prescrizioni di mia madre non siano state registrate correttamente.",
        "Vorrei segnalare che il pulsante di chiamata infermieri nella stanza di mio padre non funziona. In caso di emergenza non potrebbe chiedere aiuto tempestivamente.",
        "Sono preoccupato perché il medico ha detto che la TAC di mio figlio mostra qualcosa di sospetto ma non è sicuro. Dovremmo fare altri accertamenti prima dell'intervento?",
        "Ho notato che gli strumenti chirurgici per l'intervento di domani sono appoggiati su un carrello non coperto nel corridoio. Non rischia la sterilità?",
        "Il consenso informato che ci hanno fatto firmare è illeggibile e pieno di termini tecnici. Non ho capito quali sono i rischi reali dell'intervento.",
        "Vorrei segnalare che nella stanza di degenza la temperatura è sempre troppo bassa. Mio padre immunodepresso potrebbe prendere infezioni più facilmente?",
        "Sono preoccupata: hanno spostato l'intervento di mia madre tre volte. Il digiuno prolungato può causarle problemi considerando il suo diabete?",
        "Ho visto che l'infermiere ha attaccato la flebo senza disinfettare prima il punto di inserzione dell'ago. Non è una procedura rischiosa per infezioni?",
        "Gentili, il medico radiologo sembra molto giovane e inesperto. Ha fatto rifare la TAC tre volte. Posso richiedere che le immagini vengano riviste da un senior?",
        "Vorrei segnalare che in reparto non ci sono indicazioni chiare sulle uscite di emergenza. In caso di evacuazione i pazienti allettati sarebbero in pericolo.",
        "Sono preoccupato perché il sistema di allarme per il monitoraggio cardiaco suona continuamente ma nessuno interviene. È normale o c'è sottovalutazione dei rischi?",
        "Ho notato che mio padre riceve visite da specialisti diversi che prescrivono terapie senza coordinarsi. Non rischia interazioni farmacologiche pericolose?",
        "Vorrei capire perché la medicazione della ferita chirurgica di mia madre viene cambiata solo ogni tre giorni. Non rischia infezioni con questa frequenza bassa?",
        "Segnalo che il defibrillatore nel reparto ha la spia rossa accesa indicando malfunzionamento. In caso di arresto cardiaco potrebbe non funzionare.",
        "Sono preoccupata perché hanno programmato due interventi in sala operatoria nello stesso orario. Non rischia il mio di essere fatto di fretta aumentando i rischi?",
        "Ho notato che le bombole di ossigeno nel corridoio non sono ben fissate al muro. Potrebbero cadere e causare incidenti. A chi devo segnalarlo?",
        "Gentili, il chirurgo che dovrà operare domani mia figlia ha l'influenza e tossisce. Non sarebbe più prudente rimandare l'intervento?",
        "Vorrei segnalare che i risultati degli esami del sangue di mio padre sono stati scambiati con quelli di un altro paziente. Fortunatamente ce ne siamo accorti prima della terapia.",
        "Buongiorno, ho notato che il monitor del saturimetro di mio padre dà letture molto variabili. Potrebbe essere difettoso e dare false sicurezze?",
        "Sono preoccupata perché l'anestesista non ha voluto rispondere alle mie domande sui rischi. Mi ha detto di firmare e basta. È corretto questo comportamento?",
        "Segnalo che nella sala d'attesa del day hospital ci sono pazienti oncologici immunodepressi vicini a persone con febbre e tosse. Non è rischioso?",
        "Vorrei capire perché mio padre deve aspettare 6 ore in barella nel corridoio del pronto soccorso. Non potrebbero peggiorare le sue condizioni?",
        "Ho notato che l'infermiere ha preparato diverse siringhe tutte insieme senza etichettarle. Come fa a distinguere quale farmaco è in ciascuna?",
        "Gentili, il bagno della stanza di degenza è sporco e maleodorante da giorni. Non è un rischio infettivo per i pazienti ricoverati?",
        "Sono preoccupato perché hanno dato a mia madre compresse da deglutire ma lei ha problemi di deglutizione. Non dovrebbero somministrarle in forma liquida?",
        "Segnalo che la porta della camera iperbarica è difettosa e non si chiude ermeticamente. Non è pericoloso durante i trattamenti?",
        "Vorrei capire perché continuano a prelevare sangue a mio padre ogni giorno. È già anemico e queste analisi continue potrebbero peggiorare la situazione.",
        "Ho notato che il personale di pulizia usa lo stesso straccio per pulire pavimenti e superfici vicino ai pazienti. Non è fonte di contaminazione?",
        "Buonasera, mia madre è diabetica ma le portano vassoi con pasta e dolci. La dieta prescritta non viene rispettata. A chi posso segnalarlo?",
        "Sono preoccupata perché il catetere vescicale di mio padre è in sede da 10 giorni. Non aumenta il rischio di infezioni urinarie?",
        "Segnalo che la macchina per la pressione arteriosa nel reparto dà letture sempre diverse a distanza di pochi minuti. Potrebbe essere guasta?",
        "Vorrei capire perché nessuno controlla i segni vitali di mia madre durante la notte. Passa dalle 22 alle 6 senza alcuna verifica.",
        "Ho notato che diversi infermieri usano lo stesso fonendoscopio su tutti i pazienti senza disinfettarlo. Non è veicolo di infezioni?",
        "Gentili, il letto di mio padre è rotto e scricchiola. Temo possa cedere improvvisamente causando una caduta. Come posso farlo sostituire?",
        "Sono preoccupato perché l'aria condizionata nel reparto di terapia intensiva non funziona. Non serve per controllare i batteri nell'aria?",
        "Segnalo che i guanti sterili usati dal medico per medicare la ferita chirurgica avevano la confezione già aperta. Erano davvero sterili?",
        "Vorrei capire perché mio padre continua ad avere febbre alta da giorni ma nessuno fa esami per cercare l'infezione. Non è preoccupante?"
    ]
    
    # Genera altre 200 varianti per arrivare a 250
    for i in range(200):
        templates_extra = [
            "Segnalo situazione potenzialmente rischiosa nel reparto. Vorrei che venisse verificata per prevenire possibili complicanze ai pazienti.",
            "Ho notato irregolarità nelle procedure che potrebbero compromettere la sicurezza. Chiedo un controllo preventivo prima che accada qualcosa.",
            "Sono preoccupato per alcune condizioni che ho osservato durante il ricovero. Potrebbero causare problemi se non corrette tempestivamente.",
            "Vorrei segnalare situazione che ritengo pericolosa per i pazienti. Sarebbe opportuno un intervento prima che si verifichino incidenti."
        ]
        circostanze_iniziali.append(random.choice(templates_extra))
    
    for template in circostanze_iniziali[:250]:
        emails.append({
            "testo": template,
            "tipologia": 1,  # Circostanza Potenziale
            "riferimento_temporale": 0  # Fatto Iniziale
        })
    
    # ============================================================================
    # CATEGORIA 1-1: CIRCOSTANZE POTENZIALI - FOLLOW-UP (250 esempi)
    # ============================================================================
    circostanze_followup = [
        "Rif. segnalazione {caso_id}: vi aggiorno che la situazione da me segnalata persiste. Gli infermieri continuano a non rispettare le procedure di igiene delle mani.",
        "In merito alla mia precedente del {data} riguardo il caso {caso_id}, vi comunico che nessuno ha ancora sostituito il letto difettoso. La situazione rimane pericolosa.",
        "Oggetto: Follow-up segnalazione {caso_id}. Purtroppo devo confermare che i farmaci scaduti sono ancora nel carrello. Nessuno ha provveduto alla rimozione.",
        "Con riferimento alla circostanza {caso_id} segnalata, vi informo che oggi mio padre è effettivamente caduto dal letto per assenza delle protezioni. Fortunatamente senza conseguenze gravi.",
        "Pratica {caso_id}: aggiorno che la situazione è peggiorata. Ora anche altri pazienti lamentano lo stesso problema con il personale poco attento.",
        "In merito al caso {caso_id}, vi comunico che ho parlato con il primario che ha confermato l'esistenza del problema. Mi ha assicurato che interverrà.",
        "Rif. {caso_id}: come temevo, si è verificato un piccolo incidente. Un altro paziente è scivolato sul pavimento bagnato che avevo segnalato. Per fortuna nulla di grave.",
        "Oggetto: Aggiornamento segnalazione {caso_id}. Vi ringrazio per aver preso in carico la problematica. Ho notato che hanno sostituito la strumentazione difettosa.",
        "Con riferimento alla mia segnalazione {caso_id}, devo purtroppo comunicare che nulla è cambiato. La carenza di personale persiste e i rischi aumentano.",
        "Pratica {caso_id}: invio documentazione fotografica della situazione pericolosa che avevo segnalato. Come potete vedere, il problema non è stato ancora risolto.",
        "In merito al caso {caso_id}, vi aggiorno che l'ospedale ha attivato un'indagine interna. Mi hanno chiesto di fornire ulteriori dettagli sulla circostanza.",
        "Rif. segnalazione {caso_id}: positivo riscontro! Hanno finalmente riparato il sistema di allarme che non funzionava. Grazie per l'intervento tempestivo.",
        "Oggetto: Follow-up {caso_id}. La situazione è stata parzialmente risolta ma persistono alcuni aspetti critici che meritano attenzione.",
        "Con riferimento al caso {caso_id}, comunico che il defibrillatore è stato sostituito. Tuttavia noto che la manutenzione preventiva non viene ancora fatta regolarmente.",
        "Pratica {caso_id}: aggiorno che ho incontrato il risk manager dell'ospedale. Ha preso nota di tutte le criticità e ha avviato azioni correttive.",
        "In merito alla circostanza {caso_id} segnalata, vi informo che altri familiari hanno confermato di aver notato le stesse problematiche.",
        "Rif. {caso_id}: purtroppo devo segnalare che oggi si è verificato esattamente quello che temevo. Per fortuna abbiamo evitato conseguenze gravi grazie alla nostra vigilanza.",
        "Oggetto: Aggiornamento caso {caso_id}. L'intervento è stato rimandato nuovamente. Sono preoccupata per i rischi del digiuno prolungato come segnalato.",
        "Con riferimento alla segnalazione {caso_id}, comunico che la direzione sanitaria ha disposto audit interno. Mi hanno convocata per audizione.",
        "Pratica {caso_id}: vi ringrazio per l'interessamento. Confermo che la situazione è migliorata dopo la vostra segnalazione alla struttura.",
        "In merito al caso {caso_id}, aggiorno che purtroppo mio padre ha sviluppato un'infezione. Potrebbe essere collegata alle carenze igieniche segnalate?",
        "Rif. segnalazione {caso_id}: invio verbale della riunione con la direzione sanitaria. Hanno riconosciuto le criticità e definito piano di miglioramento.",
        "Oggetto: Follow-up {caso_id}. La situazione permane invariata nonostante le rassicurazioni. Chiedo escalation ai vostri uffici competenti.",
        "Con riferimento alla circostanza {caso_id}, comunico che hanno finalmente formato il personale sulle procedure corrette. Noto già miglioramenti.",
        "Pratica {caso_id}: aggiorno che il problema segnalato si è ripresentato. Evidentemente le azioni correttive implementate non sono sufficienti.",
        "In merito al caso {caso_id}, vi informo che l'ospedale ha attivato sistema di segnalazione interna. Incoraggiano i familiari a riportare criticità.",
        "Rif. {caso_id}: positivo! Hanno sostituito tutto il personale del turno e la situazione è nettamente migliorata. Grazie per il supporto.",
        "Oggetto: Aggiornamento segnalazione {caso_id}. Devo purtroppo comunicare che altri pazienti hanno subito lo stesso problema che avevo anticipato.",
        "Con riferimento alla pratica {caso_id}, allego email di risposta della direzione sanitaria che riconosce le problematiche e si impegna a risolverle.",
        "Pratica {caso_id}: vi aggiorno che dopo la mia segnalazione hanno fatto manutenzione straordinaria. La situazione ora è sotto controllo.",
        "In merito alla circostanza {caso_id} segnalata, comunico che ho dovuto fare esposto formale alla direzione. La situazione era troppo rischiosa.",
        "Rif. {caso_id}: come temevo, si è verificato un near miss. Fortunatamente qualcuno se n'è accorto in tempo ma era esattamente lo scenario che avevo paventato.",
        "Oggetto: Follow-up caso {caso_id}. Vi ringrazio per l'attenzione. Confermo che le azioni intraprese hanno eliminato il rischio segnalato.",
        "Con riferimento alla segnalazione {caso_id}, aggiorno che purtroppo la situazione è degenerata. Ora è necessario intervento più strutturato.",
        "Pratica {caso_id}: invio documentazione aggiornata sulla situazione. Come vedrete, nonostante le segnalazioni il rischio permane elevato.",
        "In merito al caso {caso_id}, comunico che l'audit interno ha confermato tutte le mie osservazioni. Hanno definito piano correttivo urgente.",
        "Rif. segnalazione {caso_id}: aggiorno che hanno implementato doppio controllo sulla procedura critica che avevo segnalato. Ottimo risultato!",
        "Oggetto: Aggiornamento {caso_id}. La situazione rimane preoccupante. Chiedo vostro intervento presso la struttura ospedaliera.",
        "Con riferimento alla circostanza {caso_id}, vi informo che altri familiari hanno aderito alla segnalazione. Stiamo raccogliendo documentazione collettiva.",
        "Pratica {caso_id}: positivo riscontro dalla direzione. Hanno ringraziato per la segnalazione che ha permesso di prevenire un possibile incidente grave.",
        "In merito al caso {caso_id}, aggiorno che la situazione persiste. Sto valutando se fare segnalazione anche alle autorità sanitarie regionali.",
        "Rif. {caso_id}: vi comunico che dopo numerose sollecitazioni finalmente hanno risolto. La situazione pericolosa è stata eliminata.",
        "Oggetto: Follow-up segnalazione {caso_id}. Invio ulteriori elementi a supporto della criticità segnalata. La situazione merita massima attenzione.",
        "Con riferimento alla pratica {caso_id}, allego risposta dell'ospedale che nega le problematiche. Tuttavia la situazione che ho descritto è reale e documentabile.",
        "Pratica {caso_id}: aggiorno che hanno sostituito il responsabile del reparto. Il nuovo primario si è impegnato a risolvere tutte le criticità segnalate.",
        "In merito alla circostanza {caso_id}, comunico che l'intervento di mia madre è stato spostato in altra struttura proprio per i rischi che avevo segnalato.",
        "Rif. segnalazione {caso_id}: invio feedback positivo. Dopo le azioni correttive la situazione è migliorata sensibilmente. Continuo a monitorare.",
        "Oggetto: Aggiornamento caso {caso_id}. Purtroppo si è verificato incidente simile a quello che avevo paventato. Ora è diventato un sinistro vero e proprio.",
        "Con riferimento alla circostanza {caso_id} segnalata, vi ringrazio per l'escalation. La direzione generale ha preso in carico personalmente la questione.",
        "Pratica {caso_id}: aggiorno che la situazione è peggiorata. Ora non è più solo un rischio potenziale ma un problema concreto che necessita soluzione immediata."
    ]
    
    # Genera altre 200 varianti per arrivare a 250
    for i in range(200):
        templates_extra = [
            "Rif. segnalazione {caso_id}: aggiorno sullo stato della situazione. Purtroppo non si registrano miglioramenti significativi rispetto a quanto segnalato.",
            "In merito al caso {caso_id}, comunico che la circostanza persiste. Chiedo cortesemente un vostro intervento per sollecitare risoluzioni.",
            "Oggetto: Follow-up {caso_id}. Vi ringrazio per l'attenzione. La situazione è stata parzialmente risolta ma rimangono aspetti da monitorare.",
            "Con riferimento alla segnalazione {caso_id}, invio aggiornamento sulla situazione. Allego ulteriore documentazione a supporto."
        ]
        circostanze_followup.append(random.choice(templates_extra))
    
    for template in circostanze_followup[:250]:
        emails.append({
            "testo": template.format(caso_id=generate_case_id(), data=generate_random_date()),
            "tipologia": 1,  # Circostanza Potenziale
            "riferimento_temporale": 1  # Follow-up
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

def export_to_csv(df, filename="dataset_medical_malpractice_1000.csv"):
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
    print("DATASET EMAIL - CLASSIFICAZIONE MULTI-DIMENSIONALE SINISTRI MEDICAL MALPRACTICE")
    print("=" * 80)
    
    print(f"\n📊 STATISTICHE GENERALI:")
    print(f"   • Totale email: {stats['totale_email']}")
    
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
        (0, 0, "Sinistro Avvenuto - Fatto Iniziale"),
        (0, 1, "Sinistro Avvenuto - Follow-up"),
        (1, 0, "Circostanza Potenziale - Fatto Iniziale"),
        (1, 1, "Circostanza Potenziale - Follow-up")
    ]
    
    for tip, rif, label in categories:
        print(f"\n   ▸ {label}:")
        sample = df[(df['tipologia'] == tip) & (df['riferimento_temporale'] == rif)].head(2)
        for idx, row in sample.iterrows():
            print(f"      • {row['testo'][:120]}...")
    
    # Split train/test
    train_df, test_df = split_train_test(df)
    
    print(f"\n📦 SPLIT DATASET:")
    print(f"   • Training set: {len(train_df)} email (80%)")
    print(f"   • Test set: {len(test_df)} email (20%)")
    
    print("\n" + "=" * 80)
    print("✅ Dataset generato con successo!")
    print("💡 Utilizzabile per classificazione multi-label o multi-output")
    print("=" * 80)
    
    # Esporta i dataset
    export_to_csv(df, "dataset_medical_malpractice_complete.csv")
    export_to_csv(train_df, "dataset_medical_malpractice_train.csv")
    export_to_csv(test_df, "dataset_medical_malpractice_test.csv")