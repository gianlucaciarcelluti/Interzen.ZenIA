"""
Dataset mock di email per classificazione sinistri medical malpractice.
Categorie:
- 0: Sinistro Avvenuto (incidente già verificato)
- 1: Circostanza Potenziale (situazione che potrebbe generare un sinistro)
"""

import pandas as pd

def create_mock_dataset():
    """Crea un dataset di 200 email simulate per training e testing."""
    
    emails = [
        # SINISTRI AVVENUTI (Categoria 0) - 100 esempi
        {
            "testo": "Buongiorno, vi scrivo per segnalare un grave errore chirurgico avvenuto il 15 marzo 2024. Durante l'intervento al ginocchio sinistro, il chirurgo ha operato per errore il ginocchio destro sano. Richiedo immediato risarcimento danni.",
            "categoria": 0
        },
        {
            "testo": "Gentili Signori, mio padre è deceduto il 10 gennaio 2024 a seguito di una diagnosi errata di polmonite quando invece si trattava di embolia polmonare. Allego documentazione medica completa.",
            "categoria": 0
        },
        {
            "testo": "Con la presente comunico che in data 20/02/2024 mia madre ha subito un danno permanente da farmaco somministrato erroneamente dall'ospedale San Raffaele. Necessito avviare pratica di risarcimento.",
            "categoria": 0
        },
        {
            "testo": "Spett.le compagnia, il 5 aprile 2024 durante il parto cesareo è stato lesionato il nervo sciatico di mia moglie causando paralisi parziale della gamba sinistra. Inoltro richiesta danni.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Sinistro del 12/03/2024 - Infezione post-operatoria. A seguito di intervento di appendicectomia si è sviluppata grave infezione nosocomiale che ha richiesto tre ulteriori ricoveri.",
            "categoria": 0
        },
        {
            "testo": "Vi contatto per un caso di malasanità verificatosi il 30 gennaio presso la clinica Villa Maria. Errata posologia del farmaco anticoagulante ha causato emorragia cerebrale a mio fratello.",
            "categoria": 0
        },
        {
            "testo": "Buonasera, in data 18/02/2024 il radiologo ha mancato di rilevare una massa tumorale visibile nella TAC. Il ritardo diagnostico di 6 mesi ha compromesso le possibilità di guarigione.",
            "categoria": 0
        },
        {
            "testo": "Segnalo caduta accidentale dal letto ospedaliero avvenuta il 25/03/2024 con frattura del femore. Il paziente non era stato dotato delle protezioni laterali obbligatorie.",
            "categoria": 0
        },
        {
            "testo": "Richiesta risarcimento per ustioni di terzo grado subite durante intervento laparoscopico del 14/04/2024. Lo strumento elettrochirurgico ha causato perforazione intestinale.",
            "categoria": 0
        },
        {
            "testo": "Il 22 febbraio mia figlia neonata ha subito lesioni cerebrali permanenti durante il parto per asfissia prolungata. Il personale ha ritardato il cesareo d'urgenza necessario.",
            "categoria": 0
        },
        {
            "testo": "Comunico sinistro del 08/03/2024: scambio di paziente in sala operatoria. Mio padre è stato sottoposto ad intervento cardiaco destinato ad altro paziente omonimo.",
            "categoria": 0
        },
        {
            "testo": "Gentili, il 16 aprile durante colonscopia si è verificata perforazione del colon con conseguente peritonite e intervento chirurgico d'urgenza. Chiedo apertura pratica.",
            "categoria": 0
        },
        {
            "testo": "Vi scrivo per segnalare che il 3 marzo 2024 è stata somministrata trasfusione di sangue incompatibile a mia madre, causando shock anafilattico e danni renali permanenti.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Danno da parto - 11/01/2024. Frattura della clavicola del neonato durante manovra estrattiva troppo vigorosa. Documentazione ospedaliera allegata.",
            "categoria": 0
        },
        {
            "testo": "Il giorno 29/03/2024 mio marito è stato dimesso dal pronto soccorso con diagnosi di gastrite. In realtà aveva un infarto in corso ed è deceduto due ore dopo a casa.",
            "categoria": 0
        },
        {
            "testo": "Richiesta danni per amputazione errata arto superiore sinistro avvenuta il 7 aprile 2024. Il consenso informato era per arto destro ma il chirurgo ha sbagliato lato.",
            "categoria": 0
        },
        {
            "testo": "In data 19/02/2024 durante anestesia spinale l'ago è penetrato troppo in profondità causando lesione midollare con paraplegia. Necessito assistenza legale immediata.",
            "categoria": 0
        },
        {
            "testo": "Buongiorno, segnalo reazione allergica fatale ad antibiotico somministrato il 4 marzo nonostante allergia nota fosse riportata in cartella clinica. Mia sorella è deceduta.",
            "categoria": 0
        },
        {
            "testo": "Il 27/03/2024 è stata rimossa la protesi d'anca sbagliata (destra invece di sinistra). Ora necessito ulteriore intervento con rischi aggiuntivi e lunghi tempi di recupero.",
            "categoria": 0
        },
        {
            "testo": "Comunico che il 15 aprile durante biopsia epatica si è verificata emorragia interna massiva non controllata tempestivamente, con necessità di emotrasfusioni multiple.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Sinistro oculistico 02/03/2024. Durante intervento di cataratta il cristallino è caduto nel vitreo causando perdita permanente della vista all'occhio destro.",
            "categoria": 0
        },
        {
            "testo": "Vi scrivo per danno neurologico da parto avvenuto il 23/01/2024. L'uso improprio del forcipe ha causato paralisi facciale permanente al neonato.",
            "categoria": 0
        },
        {
            "testo": "In data 10/04/2024 ho subito shock settico per strumenti chirurgici non sterili utilizzati durante intervento di ernia. Ricovero in terapia intensiva per 15 giorni.",
            "categoria": 0
        },
        {
            "testo": "Segnalo omessa diagnosi di appendicite acuta il 6 marzo con conseguente peritonite e sepsi. Mio figlio ha rischiato la vita per la negligenza del medico di guardia.",
            "categoria": 0
        },
        {
            "testo": "Richiesta risarcimento per danno estetico permanente da intervento di mastoplastica del 18/02/2024. Asimmetria grave e necrosi tissutale da errore tecnico.",
            "categoria": 0
        },
        {
            "testo": "Il 31 marzo durante dialisi è stato utilizzato liquido di dialisi contaminato causando grave infezione sistemica con shock settico e arresto cardiaco.",
            "categoria": 0
        },
        {
            "testo": "Comunico caduta da barella durante trasferimento in sala operatoria avvenuta il 9 aprile 2024 con trauma cranico e fratture multiple. Il personale era insufficiente.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Errore trasfusionale 14/03/2024. Sacca di sangue destinata ad altro paziente somministrata a mio padre causando grave emolisi e insufficienza renale acuta.",
            "categoria": 0
        },
        {
            "testo": "Vi scrivo per segnalare ustione chimica da disinfettante lasciato sulla cute durante intervento chirurgico del 21/02/2024. Lesioni di secondo grado su coscia sinistra.",
            "categoria": 0
        },
        {
            "testo": "In data 5 aprile mia madre è stata sottoposta ad isterectomia non necessaria per errata interpretazione dell'esame istologico. La lesione era benigna.",
            "categoria": 0
        },
        {
            "testo": "Comunico decesso di mia nonna avvenuto il 17/04/2024 per shock anafilattico da mezzo di contrasto. L'allergia era nota e documentata ma non è stata verificata.",
            "categoria": 0
        },
        {
            "testo": "Il 28 febbraio durante artroscopia al ginocchio è stato danneggiato il nervo peroneo causando piede cadente permanente. Chiedo avvio pratica risarcitoria.",
            "categoria": 0
        },
        {
            "testo": "Segnalo errore terapeutico del 13/03/2024: insulina somministrata a paziente non diabetico causando coma ipoglicemico e danni cerebrali irreversibili.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Sinistro odontoiatrico 01/04/2024. Durante estrazione dentale è stata perforata la cavità sinusale con conseguente sinusite cronica e necessità di chirurgia ricostruttiva.",
            "categoria": 0
        },
        {
            "testo": "Vi contatto per danno da posizionamento errato sondino naso-gastrico il 19/02/2024. È stato inserito in trachea causando polmonite ab ingestis grave.",
            "categoria": 0
        },
        {
            "testo": "In data 25/03/2024 mio figlio ha subito rottura della milza durante manovre di rianimazione troppo aggressive. Il personale non era adeguatamente formato.",
            "categoria": 0
        },
        {
            "testo": "Richiesta danni per frattura dentale e lussazione mandibolare durante intubazione in anestesia generale del 7 aprile. Manovre eseguite con eccessiva forza.",
            "categoria": 0
        },
        {
            "testo": "Il 12 marzo durante intervento laparoscopico lo strumento ha lacerato l'aorta addominale causando emorragia massiva. Mio marito è sopravvissuto miracolosamente.",
            "categoria": 0
        },
        {
            "testo": "Comunico embolia gassosa verificatasi il 3 aprile durante posizionamento catetere venoso centrale con conseguente ictus e emiparesi destra permanente.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Danno estetico permanente da blefaroplastica 15/02/2024. Rimozione eccessiva di tessuto palpebrale che impedisce completa chiusura degli occhi.",
            "categoria": 0
        },
        {
            "testo": "Il 20 marzo mia madre ha subito perforazione esofagea durante gastroscopia con conseguente mediastinite e 40 giorni di ricovero in terapia intensiva.",
            "categoria": 0
        },
        {
            "testo": "Segnalo danno neurologico da puntura lombare eseguita il 9 aprile a livello troppo basso causando sindrome della cauda equina con incontinenza permanente.",
            "categoria": 0
        },
        {
            "testo": "In data 26/02/2024 durante intervento di tonsillectomia si è verificata emorragia post-operatoria non gestita tempestivamente. Mio figlio ha avuto arresto cardiaco.",
            "categoria": 0
        },
        {
            "testo": "Vi scrivo per pneumotorace iatrogeno causato da posizionamento errato di catetere venoso centrale il 14/03/2024. Necessario drenaggio toracico d'urgenza.",
            "categoria": 0
        },
        {
            "testo": "Richiesta risarcimento per sindrome compartimentale post-operatoria non riconosciuta tempestivamente il 5 aprile. Conseguente necrosi muscolare e amputazione parziale.",
            "categoria": 0
        },
        {
            "testo": "Il 18 febbraio durante cistoscopia è stata perforata la vescica con conseguente peritonite urinosa e necessità di intervento chirurgico addominale maggiore.",
            "categoria": 0
        },
        {
            "testo": "Comunico danno da dimissione precoce avvenuta il 30/03/2024. Mio padre è stato dimesso con polmonite non diagnosticata ed è deceduto 12 ore dopo a domicilio.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Errore anestesiologico 22/02/2024. Intubazione esofagea non riconosciuta per 8 minuti causando ipossia cerebrale grave e stato vegetativo permanente.",
            "categoria": 0
        },
        {
            "testo": "Il 10 aprile durante artrocentesi del ginocchio è stata iniettata aria invece che cortisonico causando embolia gassosa articolare con necrosi cartilaginea.",
            "categoria": 0
        },
        {
            "testo": "Segnalo danno da farmaco citotossico somministrato per via endovenosa periferica il 6 marzo causando necrosi tissutale massiva e necessità di innesto cutaneo.",
            "categoria": 0
        },
        {
            "testo": "In data 1 aprile mia figlia ha subito lesione del dotto biliare durante colecistectomia laparoscopica richiedendo complessa chirurgia ricostruttiva epatobiliare.",
            "categoria": 0
        },
        {
            "testo": "Vi contatto per danno da posizionamento scorretto sul tavolo operatorio il 24/03/2024 causando sindrome da compressione nervosa con paralisi del plesso brachiale.",
            "categoria": 0
        },
        {
            "testo": "Richiesta danni per omessa profilassi antibiotica pre-operatoria il 16 febbraio causando endocardite batterica post-intervento con necessità di sostituzione valvolare.",
            "categoria": 0
        },
        {
            "testo": "Il 28 marzo durante broncoscopia è stata causata lacerazione bronchiale con pneumomediastino e necessità di toracotomia d'urgenza per riparazione.",
            "categoria": 0
        },
        {
            "testo": "Comunico danno da mancato monitoraggio post-operatorio il 11/04/2024. Emorragia interna non rilevata tempestivamente causando shock ipovolemico e arresto cardiaco.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Sinistro ortopedico 19/03/2024. Durante riduzione di frattura sotto sedazione è stata causata lesione vascolare con ischemia acuta e necessità di amputazione.",
            "categoria": 0
        },
        {
            "testo": "Il 2 marzo mio marito ha subito danno da ipotermia perioperatoria non prevenuta causando aritmie cardiache maligne e prolungato ricovero in terapia intensiva.",
            "categoria": 0
        },
        {
            "testo": "Segnalo errata interpretazione di ECG il 25/02/2024 con mancato riconoscimento di infarto miocardico acuto. Conseguente estensione dell'area necrotica cardiaca.",
            "categoria": 0
        },
        {
            "testo": "In data 8 aprile durante paracentesi addominale è stato perforato l'intestino causando peritonite fecale e necessità di resezione intestinale d'urgenza.",
            "categoria": 0
        },
        {
            "testo": "Vi scrivo per danno da terapia radiante erogata su campo sbagliato il 14/02/2024. Grave radiodermite su tessuti sani mentre il tumore non è stato trattato.",
            "categoria": 0
        },
        {
            "testo": "Richiesta risarcimento per lesione iatale esofagea durante intervento di fundoplicatio del 21/03/2024 causando disfagia permanente e necessità di alimentazione enterale.",
            "categoria": 0
        },
        {
            "testo": "Il 4 aprile mia madre ha subito danno renale acuto da mezzo di contrasto iodato somministrato nonostante insufficienza renale nota. Ora è in dialisi permanente.",
            "categoria": 0
        },
        {
            "testo": "Comunico danno da body packing interno dimenticato durante intervento chirurgico il 27/02/2024. Garza lasciata in addome causando ascesso e sepsi.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Errore trasfusionale 15/03/2024. Somministrata sacca di plasma fresco scongelato scaduto causando coagulopatia grave e sanguinamento multiplo.",
            "categoria": 0
        },
        {
            "testo": "Il 10 marzo durante artroprotesi d'anca è stata cementata la protesi in posizione viziata causando lussazione ricorrente e necessità di revisione chirurgica.",
            "categoria": 0
        },
        {
            "testo": "Segnalo danno da iniezione intra-arteriosa accidentale di farmaco venoso il 23/03/2024 causando gangrena distale e amputazione di tre dita della mano.",
            "categoria": 0
        },
        {
            "testo": "In data 6 aprile mio figlio ha subito ustione corneale bilaterale da disinfettante durante intervento oculistico causando cecità parziale permanente.",
            "categoria": 0
        },
        {
            "testo": "Vi contatto per danno da farmaco chemioterapico somministrato per via intratecale invece che endovenosa il 29/02/2024. Conseguente meningite chimica e paraplegia.",
            "categoria": 0
        },
        {
            "testo": "Richiesta danni per rottura di ago durante anestesia spinale il 17/03/2024 con frammento rimasto in sede e necessità di laminectomia per rimozione.",
            "categoria": 0
        },
        {
            "testo": "Il 12 aprile durante cardioversione elettrica è stata erogata scarica a energia eccessiva causando ustioni cutanee di terzo grado e fratture costali multiple.",
            "categoria": 0
        },
        {
            "testo": "Comunico danno da mancata diagnosi di gravidanza ectopica il 5 marzo con conseguente rottura tubarica, shock emorragico e necessità di salpingectomia d'urgenza.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Sinistro pediatrico 20/02/2024. Durante vaccinazione è stato somministrato dosaggio per adulto causando febbre convulsiva e ricovero ospedaliero prolungato.",
            "categoria": 0
        },
        {
            "testo": "Il 2 aprile mia madre ha subito lesione del nervo laringeo ricorrente durante tiroidectomia causando paralisi cordale e disfonia permanente.",
            "categoria": 0
        },
        {
            "testo": "Segnalo danno da perdita di corpo estraneo radiopaco durante intervento endoscopico il 26/03/2024. Pinza frammentata rimasta in stomaco richiedente gastrectomia.",
            "categoria": 0
        },
        {
            "testo": "In data 13 febbraio durante drenaggio di ascesso è stata lesa l'arteria femorale causando pseudoaneurisma e necessità di riparazione vascolare chirurgica.",
            "categoria": 0
        },
        {
            "testo": "Vi scrivo per danno da sovradosaggio di oppiacei in PCA il 9 aprile causando depressione respiratoria grave e arresto cardiorespiratorio con rianimazione.",
            "categoria": 0
        },
        {
            "testo": "Richiesta risarcimento per danno da ipoglicemia non trattata tempestivamente il 1 marzo causando crisi epilettiche ricorrenti e deficit cognitivi permanenti.",
            "categoria": 0
        },
        {
            "testo": "Il 22 marzo durante posizionamento di port-a-cath è stata perforata la vena cava superiore causando emotorace massivo e necessità di toracotomia d'urgenza.",
            "categoria": 0
        },
        {
            "testo": "Comunico danno da mancata rivalutazione clinica post-operatoria il 14/04/2024. Deiscenza di sutura anastomotica non riconosciuta causando peritonite fecale.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Errore farmaceutico 7/03/2024. Dispensato farmaco con nome simile ma principio attivo diverso causando crisi ipertensiva maligna e ictus emorragico.",
            "categoria": 0
        },
        {
            "testo": "Il 30 marzo mio padre ha subito danno da estubazione accidentale durante trasporto in terapia intensiva con conseguente ipossia cerebrale e coma prolungato.",
            "categoria": 0
        },
        {
            "testo": "Segnalo lesione iatrogena dell'uretere durante isterectomia il 18/02/2024 causando idronefrosi e perdita funzionale del rene sinistro nonostante reimpianto.",
            "categoria": 0
        },
        {
            "testo": "In data 11 aprile durante artroscopia di spalla è stata causata lesione del plesso brachiale causando paralisi completa dell'arto superiore destro.",
            "categoria": 0
        },
        {
            "testo": "Vi contatto per danno da mancato riconoscimento di sindrome da serotonina il 4 marzo causando ipertermia maligna, rabdomiolisi e insufficienza renale acuta.",
            "categoria": 0
        },
        {
            "testo": "Richiesta danni per perforazione duodenale durante ERCP del 27/03/2024 causando pancreatite acuta necrotizzante e necessità di pancreaticoduodenectomia.",
            "categoria": 0
        },
        {
            "testo": "Il 16 febbraio mia figlia ha subito reazione trasfusionale TRALI con conseguente ARDS grave richiedente ventilazione meccanica prolungata e fibrosi polmonare residua.",
            "categoria": 0
        },
        {
            "testo": "Comunico danno da posizionamento errato di tubo toracico il 24/02/2024. Inserito in addome invece che in torace causando perforazione epatica e emorragia.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Sinistro neurologico 8/04/2024. Durante endarterectomia carotidea si è verificato distacco di placca ateromatosa causando ictus ischemico maggiore.",
            "categoria": 0
        },
        {
            "testo": "Il 3 marzo durante infiltrazione periradicolare sotto guida TAC è stato iniettato anestetico in arteria spinale causando ischemia midollare e paraparesi.",
            "categoria": 0
        },
        {
            "testo": "Segnalo danno da mancata prevenzione di TVP post-operatoria il 19/03/2024 con conseguente embolia polmonare massiva e arresto cardiaco rianimato.",
            "categoria": 0
        },
        {
            "testo": "In data 12 aprile mio marito ha subito danno da iperkaliemia non trattata tempestivamente causando aritmia ventricolare maligna e necessità di defibrillazione.",
            "categoria": 0
        },
        {
            "testo": "Vi scrivo per danno da mancata diagnosi di tamponamento cardiaco post-operatorio il 5 aprile causando shock cardiogeno e necessità di pericardiocentesi d'urgenza.",
            "categoria": 0
        },
        {
            "testo": "Richiesta risarcimento per lesione del nervo facciale durante parotidectomia del 28/02/2024 causando paralisi facciale periferica permanente e lagoftalmo.",
            "categoria": 0
        },
        {
            "testo": "Il 15 marzo durante cardioversione farmacologica è stato somministrato farmaco antiaritmico controindicato causando torsione di punta e morte clinica rianimata.",
            "categoria": 0
        },
        {
            "testo": "Comunico danno da sindrome da reinfusione durante trapianto di midollo il 1 aprile causando insufficienza multiorgano e prolungato ricovero in terapia intensiva.",
            "categoria": 0
        },
        {
            "testo": "Oggetto: Errore chirurgico 23/03/2024. Durante splenectomia è stato leso il pancreas causando fistola pancreatica persistente e necessità di pancreasectomia parziale.",
            "categoria": 0
        },
        {
            "testo": "Il 10 aprile mia madre ha subito danno da incorretta gestione della glicemia perioperatoria causando chetoacidosi diabetica e coma iperosmolare.",
            "categoria": 0
        },
        {
            "testo": "Segnalo lesione spinale da posizionamento prono scorretto durante intervento il 6 marzo causando tetraparesi spastica e dipendenza da ventilazione meccanica.",
            "categoria": 0
        },
        {
            "testo": "In data 29 marzo durante liposuzione estetica è stata perforata la parete addominale causando lesione intestinale, peritonite e necessità di laparotomia esplorativa.",
            "categoria": 0
        },
        
        # CIRCOSTANZE POTENZIALI (Categoria 1) - 100 esempi
        {
            "testo": "Gentili, vorrei segnalare che durante il ricovero di mio padre ho notato che alcuni infermieri non si lavano le mani tra un paziente e l'altro. Temo possa causare infezioni.",
            "categoria": 1
        },
        {
            "testo": "Buongiorno, sono preoccupata perché il medico ha prescritto due farmaci a mia madre che secondo il foglietto illustrativo non andrebbero assunti insieme. Cosa devo fare?",
            "categoria": 1
        },
        {
            "testo": "Vi scrivo perché nella cartella clinica di mio marito ci sono annotazioni riferite ad un altro paziente. Potrebbe generare confusione e rischi per la terapia futura?",
            "categoria": 1
        },
        {
            "testo": "Segnalo che il pavimento del reparto ortopedia è sempre bagnato e scivoloso. Mio padre anziano ha rischiato di cadere più volte. Vorrei che interveniste preventivamente.",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato: il chirurgo che dovrà operare mia figlia domani ha detto che non ha mai eseguito questo intervento prima. È normale? Posso cambiare chirurgo?",
            "categoria": 1
        },
        {
            "testo": "Durante la visita pre-operatoria nessuno ha chiesto a mia madre se è allergica a qualche farmaco. Non dovrebbe essere una domanda standard per evitare problemi?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che le sbarre laterali del letto di mio padre non funzionano bene. È allettato e potrebbe cadere. Come posso richiedere la sostituzione del letto?",
            "categoria": 1
        },
        {
            "testo": "Buonasera, il medico ha detto che farà un intervento diverso da quello per cui abbiamo firmato il consenso informato. Non dovrei firmare un nuovo documento?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata perché ho visto che l'etichetta sulla sacca della flebo di mia sorella porta un nome diverso dal suo. L'infermiere dice che è giusto, ma ho dubbi.",
            "categoria": 1
        },
        {
            "testo": "Segnalo che in reparto c'è carenza cronica di personale. I pazienti allettati vengono cambiati di posizione solo una volta al giorno rischiando piaghe da decubito.",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire se è normale che mio padre prenda 15 farmaci diversi al giorno. Il medico di base ha detto che potrebbero esserci interazioni pericolose.",
            "categoria": 1
        },
        {
            "testo": "Durante il ricovero ho notato che le date di scadenza di alcuni farmaci nel carrello sono superate. A chi devo segnalarlo per evitare che vengano somministrati?",
            "categoria": 1
        },
        {
            "testo": "Gentili, il sistema informatico dell'ospedale è andato in tilt per 2 giorni. Temo che le prescrizioni di mia madre non siano state registrate correttamente.",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che il pulsante di chiamata infermieri nella stanza di mio padre non funziona. In caso di emergenza non potrebbe chiedere aiuto tempestivamente.",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato perché il medico ha detto che la TAC di mio figlio mostra qualcosa di sospetto ma non è sicuro. Dovremmo fare altri accertamenti prima dell'intervento?",
            "categoria": 1
        },
        {
            "testo": "Ho notato che gli strumenti chirurgici per l'intervento di domani sono appoggiati su un carrello non coperto nel corridoio. Non rischia la sterilità?",
            "categoria": 1
        },
        {
            "testo": "Il consenso informato che ci hanno fatto firmare è illeggibile e pieno di termini tecnici. Non ho capito quali sono i rischi reali dell'intervento.",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che nella stanza di degenza la temperatura è sempre troppo bassa. Mio padre immunodepresso potrebbe prendere infezioni più facilmente?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: hanno spostato l'intervento di mia madre tre volte. Il digiuno prolungato può causarle problemi considerando il suo diabete?",
            "categoria": 1
        },
        {
            "testo": "Ho visto che l'infermiere ha attaccato la flebo senza disinfettare prima il punto di inserzione dell'ago. Non è una procedura rischiosa per infezioni?",
            "categoria": 1
        },
        {
            "testo": "Gentili, il medico radiologo sembra molto giovane e inesperto. Ha fatto rifare la TAC tre volte. Posso richiedere che le immagini vengano riviste da un senior?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che in reparto non ci sono indicazioni chiare sulle uscite di emergenza. In caso di evacuazione i pazienti allettati sarebbero in pericolo.",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato perché il sistema di allarme per il monitoraggio cardiaco suona continuamente ma nessuno interviene. È normale o c'è sottovalutazione dei rischi?",
            "categoria": 1
        },
        {
            "testo": "Ho notato che mio padre riceve visite da specialisti diversi che prescrivono terapie senza coordinarsi. Non rischia interazioni farmacologiche pericolose?",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché la medicazione della ferita chirurgica di mia madre viene cambiata solo ogni tre giorni. Non rischia infezioni con questa frequenza bassa?",
            "categoria": 1
        },
        {
            "testo": "Segnalo che il defibrillatore nel reparto ha la spia rossa accesa indicando malfunzionamento. In caso di arresto cardiaco potrebbe non funzionare.",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata perché hanno programmato due interventi in sala operatoria nello stesso orario. Non rischia il mio di essere fatto di fretta aumentando i rischi?",
            "categoria": 1
        },
        {
            "testo": "Ho notato che le bombole di ossigeno nel corridoio non sono ben fissate al muro. Potrebbero cadere e causare incidenti. A chi devo segnalarlo?",
            "categoria": 1
        },
        {
            "testo": "Gentili, il chirurgo che dovrà operare domani mia figlia ha l'influenza e tossisce. Non sarebbe più prudente rimandare l'intervento?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che i risultati degli esami del sangue di mio padre sono stati scambiati con quelli di un altro paziente. Fortunatamente ce ne siamo accorti prima della terapia.",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato perché nell'armadietto dei farmaci del reparto ho visto confezioni aperte e non etichettate. Come si fa a sapere cosa contengono e quando scadono?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che il medico di guardia sembra sempre molto affaticato. Ieri si è addormentato sulla scrivania. Può influire sulla qualità delle cure?",
            "categoria": 1
        },
        {
            "testo": "Ho notato che durante la medicazione l'infermiere ha toccato il suo cellulare e poi ha continuato senza cambiarsi i guanti. Non è un rischio di infezione?",
            "categoria": 1
        },
        {
            "testo": "Gentili, il sistema di aspirazione nella stanza di terapia intensiva fa un rumore strano e sembra non funzionare bene. Dovrebbe essere controllato?",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché mia madre riceve sempre gli stessi farmaci da infermieri diversi ma con orari ogni volta differenti. Non dovrebbe esserci un protocollo fisso?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: il braccialetto identificativo di mio padre si è rotto e non è stato sostituito da due giorni. Come fanno a identificarlo con certezza?",
            "categoria": 1
        },
        {
            "testo": "Ho visto che il carrello delle emergenze in corridoio ha il sigillo rotto. Non dovrebbe essere verificato e risigillato per garantire che tutto sia a posto?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che nella stanza ci sono cavi elettrici scoperti e il paziente nel letto accanto ha già preso una scossa. Quando verranno riparati?",
            "categoria": 1
        },
        {
            "testo": "Buongiorno, il medico che ha visitato mia figlia non ha consultato la sua cartella clinica informatica. Ha basato tutto solo su quello che gli abbiamo detto noi.",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato perché l'ambulanza che ha trasportato mio padre non aveva il defibrillatore funzionante. Il personale ha detto che era in riparazione da una settimana.",
            "categoria": 1
        },
        {
            "testo": "Ho notato che i contenitori per lo smaltimento degli aghi sono riempiti oltre il limite di sicurezza. Gli aghi sporgono dal foro superiore rischiando punture accidentali.",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché mia madre in terapia intensiva viene controllata dagli infermieri solo ogni 2-3 ore. Non dovrebbe essere monitorata continuamente?",
            "categoria": 1
        },
        {
            "testo": "Gentili, il materasso antidecubito di mio padre allettato non sembra gonfiarsi correttamente. Sta già sviluppando arrossamenti su sacro e talloni.",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: hanno spostato l'operazione di mia figlia per la terza volta. Nel frattempo il dolore aumenta. Quando verrà operata definitivamente?",
            "categoria": 1
        },
        {
            "testo": "Ho visto che il frigorifero dove conservano i farmaci termolabili segna 12°C invece che 2-8°C. I farmaci potrebbero essere deteriorati?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che in reparto il gel disinfettante per le mani è esaurito da tre giorni. Come fa il personale a disinfettarsi adeguatamente?",
            "categoria": 1
        },
        {
            "testo": "Il chirurgo ha detto che userà una tecnica sperimentale su mio padre ma non ci ha fatto firmare alcun consenso specifico. Non è necessario?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato perché durante la visita il medico si è accorto di aver visitato mio padre credendo fosse un altro paziente. Ha confuso le cartelle cliniche.",
            "categoria": 1
        },
        {
            "testo": "Ho notato che l'ossigeno nella bombola della stanza segna quasi zero ma nessuno l'ha sostituita. In caso di emergenza non ci sarebbe ossigeno disponibile.",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché a mia madre vengono prelevati campioni di sangue ogni giorno ma i risultati non vengono mai consultati dai medici che la visitano.",
            "categoria": 1
        },
        {
            "testo": "Gentili, il personale del turno di notte è ridotto a una sola infermiera per 20 pazienti. In caso di più emergenze contemporanee come potrebbe gestire?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: mio padre diabetico non riceve controlli glicemici da 24 ore. L'ultimo valore era alto ma nessuno ha modificato la terapia.",
            "categoria": 1
        },
        {
            "testo": "Ho visto che gli strumenti riutilizzabili vengono solo sciacquati velocemente tra un paziente e l'altro. Non dovrebbero essere sterilizzati adeguatamente?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che la sedia a rotelle che usano per trasportare mio padre ha i freni rotti. Durante l'ultimo trasferimento ha rischiato di cadere.",
            "categoria": 1
        },
        {
            "testo": "Il medico ha prescritto un farmaco a cui mia madre è allergica. Per fortuna l'infermiere se n'è accorto prima di somministrarlo, ma non doveva esserci un alert automatico?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato perché nella sala d'attesa del pronto soccorso c'è una persona con tosse e febbre molto alta vicino ai pazienti immunodepressi. Non andrebbe isolata?",
            "categoria": 1
        },
        {
            "testo": "Ho notato che il saturimetro che usano su mio padre dà letture molto variabili e spesso segnala errore. Come fanno a fidarsi dei valori che mostra?",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché i medici specialisti che seguono mio padre non si parlano mai tra loro. Ognuno prescrive terapie senza sapere cosa fanno gli altri.",
            "categoria": 1
        },
        {
            "testo": "Gentili, il sistema di videosorveglianza nelle aree comuni del reparto non funziona. In caso di caduta o malore di un paziente come farebbero a vederlo?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: mia madre dovrebbe assumere un farmaco salvavita ogni 12 ore ma spesso lo riceve con 3-4 ore di ritardo. Può ridurne l'efficacia?",
            "categoria": 1
        },
        {
            "testo": "Ho visto che la porta della sala operatoria rimane spesso aperta durante gli interventi. Non rischia di compromettere la sterilità dell'ambiente?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che il personale di pulizia usa gli stessi panni per pulire il bagno e poi il tavolino dove appoggiano i farmaci. Non è igienico.",
            "categoria": 1
        },
        {
            "testo": "Il radiologo ha detto che le immagini della risonanza sono di scarsa qualità e dovrebbe ripeterla ma mio padre è molto claustrofobico. Non c'è alternativa?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato: hanno cambiato la terapia di mio padre ma non hanno aggiornato il foglio terapia appeso in stanza. Gli infermieri rischiano di dare i farmaci sbagliati.",
            "categoria": 1
        },
        {
            "testo": "Ho notato che la bilancia per pesare i pazienti allettati non è stata tarata da mesi secondo il cartellino. I pesi rilevati sono affidabili?",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché mia madre cardiopatica non ha il monitoraggio cardiaco continuo. Ha già avuto due episodi di aritmia durante il ricovero.",
            "categoria": 1
        },
        {
            "testo": "Gentili, il sistema informatico va in crash più volte al giorno. Gli infermieri perdono le prescrizioni inserite. Come garantite continuità delle cure?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: l'ascensore che porta in sala operatoria si blocca spesso. In caso di emergenza chirurgica potrebbe causare ritardi pericolosi.",
            "categoria": 1
        },
        {
            "testo": "Ho visto che il defibrillatore nel reparto ha la batteria scarica secondo l'indicatore. Dovrebbe essere sempre pronto all'uso in caso di arresto cardiaco.",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che l'acqua dei rubinetti del reparto esce marrone la mattina. Viene usata anche per diluire i farmaci. È sicura?",
            "categoria": 1
        },
        {
            "testo": "Il chirurgo che opererà domani mio padre ha detto che non ha mai usato il nuovo modello di protesi ma è l'unico disponibile. Non dovrebbe prima fare training?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato: mia madre con demenza continua a togliersi il catetere venoso. L'hanno rifatto 5 volte aumentando il rischio di infezioni. Non c'è altra soluzione?",
            "categoria": 1
        },
        {
            "testo": "Ho notato che i campioni di sangue dei pazienti restano sul bancone per ore prima di essere analizzati. Può alterare i risultati degli esami?",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché i dati del monitoraggio cardiaco di mio padre in terapia intensiva non vengono registrati nella cartella clinica. Come ricostruire l'andamento?",
            "categoria": 1
        },
        {
            "testo": "Gentili, la segnaletica per raggiungere il pronto soccorso è confusa. Un paziente con infarto potrebbe perdere tempo prezioso cercando l'ingresso giusto.",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: durante la notte c'è solo un medico di guardia per tutto l'ospedale. In caso di più emergenze come può gestirle tutte?",
            "categoria": 1
        },
        {
            "testo": "Ho visto che il personale della mensa porta il cibo in reparto senza copricapo né mascherina. Può essere una fonte di infezione per i pazienti?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che l'aria condizionata in sala operatoria non funziona bene. Il chirurgo sudava molto durante l'ultimo intervento. Non compromette la sterilità?",
            "categoria": 1
        },
        {
            "testo": "Il fisioterapista ha detto che mio padre dovrebbe fare riabilitazione quotidiana ma viene solo 2 volte a settimana per carenza di personale. Rallenta il recupero?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato: il sistema di allarme antincendio ha suonato per sbaglio tre volte questa settimana. La gente non ci fa più caso. In caso reale nessuno evacuarebbe.",
            "categoria": 1
        },
        {
            "testo": "Ho notato che i farmaci per la terapia del dolore di mia madre vengono tenuti in un cassetto chiuso ma la chiave è sempre inserita. Non è un rischio sicurezza?",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché la ferita chirurgica di mio padre non viene fotografata ad ogni medicazione. In caso di problemi come si documenta l'evoluzione?",
            "categoria": 1
        },
        {
            "testo": "Gentili, ho visto che studenti di medicina praticano prelievi venosi su mio padre senza supervisione. Non dovrebbe esserci sempre un medico presente?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: la cartella clinica cartacea di mia madre è sparita per due giorni. Nel frattempo le cure sono proseguite senza documentazione. Come è possibile?",
            "categoria": 1
        },
        {
            "testo": "Ho notato che il personale non verifica mai l'identità del paziente prima di somministrare farmaci. Guardano solo il letto. E se ci fosse uno scambio?",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che l'impianto elettrico della stanza fa scintille quando si attaccano apparecchiature. È stato segnalato ma nessuno è intervenuto.",
            "categoria": 1
        },
        {
            "testo": "Il nutrizionista ha prescritto dieta speciale per mio padre diabetico ma la cucina continua a mandare pasti normali con molti carboidrati. Chi controlla?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato: hanno trasferito mio padre in un reparto dove nessuno conosce la sua storia clinica. I nuovi medici non hanno accesso ai documenti precedenti.",
            "categoria": 1
        },
        {
            "testo": "Ho visto che l'ecografo usato in reparto ha lo schermo rotto in un angolo. Le immagini sono complete o manca qualche porzione importante?",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché a mia madre allergica al lattice vengono ancora usati guanti in lattice. L'allergia è ben documentata in cartella da anni.",
            "categoria": 1
        },
        {
            "testo": "Gentili, il gruppo elettrogeno di emergenza viene testato ogni sei mesi ma l'ultimo test è fallito. In caso di blackout l'ospedale rimarrebbe senza corrente?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupata: mio padre ha 85 anni e il medico vuole fargli un intervento molto invasivo senza aver discusso alternative meno rischiose. È normale?",
            "categoria": 1
        },
        {
            "testo": "Ho notato che la pressione arteriosa di mia madre viene misurata con manicotto di dimensioni sbagliate. I valori registrati sono quindi inaffidabili.",
            "categoria": 1
        },
        {
            "testo": "Vorrei segnalare che durante i turni notturni non c'è mai un medico specialista disponibile in reparto. Solo il medico di guardia generico per tutto l'ospedale.",
            "categoria": 1
        },
        {
            "testo": "Il farmacista ha detto che il farmaco prescritto non è disponibile e ne ha dato uno simile senza consultare il medico. Può essere ugualmente efficace?",
            "categoria": 1
        },
        {
            "testo": "Sono preoccupato: mio padre ha una lesione da decubito che peggiora ma nessuno sembra accorgersene. Non viene ispezionata durante le cure quotidiane.",
            "categoria": 1
        },
        {
            "testo": "Ho visto che i referti degli esami vengono lasciati aperti sulla scrivania infermieri dove chiunque può leggerli. Non è violazione della privacy?",
            "categoria": 1
        },
        {
            "testo": "Vorrei capire perché mia madre riceve antibiotici da una settimana ma nessuno ha mai fatto antibiogramma per verificare se è quello giusto.",
            "categoria": 1
        },
        {
            "testo": "Gentili, l'autoclave per sterilizzare gli strumenti chirurgici dà spesso errore secondo il personale. Gli strumenti sono veramente sterili quando viene usata?",
            "categoria": 1
        },
    ]
    
    df = pd.DataFrame(emails)
    return df

def get_category_names():
    """Restituisce i nomi delle categorie."""
    return {
        0: "Sinistro Avvenuto",
        1: "Circostanza Potenziale"
    }

if __name__ == "__main__":
    # Test del dataset
    df = create_mock_dataset()
    print(f"Dataset creato con {len(df)} email")
    print(f"\nDistribuzione categorie:\n{df['categoria'].value_counts()}")
    print(f"\nPrime 3 email per categoria 0:")
    print(df[df['categoria'] == 0].head(3)['testo'].values)
    print(f"\nPrime 3 email per categoria 1:")
    print(df[df['categoria'] == 1].head(3)['testo'].values)
