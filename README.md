# Progetto per l'esame di Sistemi Robotici
Lo studio volge l'attenzione alla descrizione e analisi del movimento di piattaforme multirotore tramite modellazione e simulazione grafica. In particolare si è analizzata la simulazione grafica (bidimensionale) di un multirotore, implementando il controllo in velocità e posizione dell’asse di roll e della z.
Per dimostrare la corretta taratura dei controllori si sono prodotti i grafici di velocità e posizione.
Il progetto ha inoltre come scopo la realizzazione di un ambiente bidimensionale popolato da ostacoli fissi e da oggetti da catturare.
Infine, in PHIDIAS, si è implementato l’algoritmo del cammino minimo e la strategia di movimento del drone. In particolare la strategia si compone delle due seguenti procedure:
1. generate() - che genera 10 blocchi da posizionare in 10 posizioni sul terreno stabilite a priori generando casualmente il colore2;
2. scan and pick() - che consente al multirotore di effettuare la scansione, blocco per blocco, ed il prelevamento del blocco solo se esso è di colore rosso o verde; il blocco catturato va poi depositato nel contenitore.
Per ulterioni informazioni consultare la [relazione di progetto](https://github.com/pierpaologumina/sistemiRoboticiExam/blob/main/report_sr.pdf)
