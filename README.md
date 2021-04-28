# Authorship attribution
Progetto per l'esame del corso di Big Data

## Struttura del repository
- `texts`: directory contenente 250 testi scritti da 10 autori diversi (25 testi per ogni autore) usati per formare l'insieme degli autori noti
- `author_metrics`: directory contenente i file binari degli autori noti (rappresentano le caratteristiche di stile estratte dai testi da loro scritti)
- `analyze_files`: directory contenente 100 testi usati per testare la classificazione, di cui 50 testi sono di 10 autori già noti al sistema e altri 50 testi sono di 10 autori sconosciuti
- `main.py`: modulo principale da richiamare (ha il compito di eseguire i sottomoduli)
- `authorship.py`: sottomodulo che salva le caratteristiche di stile estratte da uno o più testi (anche di autori diversi) forniti in input
- `analysis.py`: sottomodulo che analizza i testi forniti in input ed esegue un processo di classificazione confrontando le loro caratteristiche di stile con quelle degli autori già noti al sistema

## Esecuzione su Cloudera
Istruzioni per l'esecuzione del progetto su Cloudera

### Installazione di Docker
- Scaricare Docker con il seguente comando (su Linux):
```
sudo curl -sSL https://get.docker.com/ | sh
```
Nota: per installare Docker su Windows si veda https://docs.docker.com/docker-for-windows/install/
- Controllare che la versione di Docker scaricata sia successiva alla 17:
```
docker --version
```
- Importare l'immagine di Cloudera QuickStart:
```
service docker start
docker pull cloudera/quickstart:latest
```
- Lanciare il container (per la prima volta):
```
docker run --hostname=quickstart.cloudera --privileged=true -t -i -p 8888:8888 -p 80:80 -p 7180:7180 --name cloudera cloudera/quickstart /usr/bin/docker-quickstart
```
- Lanciare il container (dopo l'installazione) e interagire con esso:
```
docker ps -a
docker start <CONTAINER_ID>
docker exec -it cloudera /bin/bash
```
- Fermare il container e Docker:
```
docker stop <CONTAINER_ID>
service docker stop
```

### Predisposizione dell'ambiente virtuale con Python 3
Su Cloudera Pyspark gira di default su Python 2.6; siccome il progetto è stato sviluppato usando Python 3 è necessario installare Python 3.4 (l'ultima versione disponibile per Cloudera) e predisporre un ambiente virtuale in cui Pyspark possa girare su tale versione.

Prima di fare ciò è necessario risolvere alcuni problemi legati al manager di pacchetti `yum`; a questo proposito è stato realizzato uno script bash che permette di automatizzare alcuni passaggi.
- Scaricare il file `Cloudera.sh` contenente lo script bash
- Copiare il file nel container:
```
docker cp --archive -L Cloudera.sh cloudera:/<directory>
```
- Eseguire lo script nella bash di Cloudera:
```
sh ./Cloudera.sh
```
Se tutto è andato a buon fine si dovrebbe essere in grado di richiamare il comando `python3.4`; in caso contrario provare a seguire le istruzioni passo passo descritte in questa [guida](https://github.com/zampierida98/authorship/tree/main/Risoluzione%20problemi/Guida.md).
- Attivare l'ambiente virtuale in una nuova directory:
```
mkdir <directory>
pyvenv <directory>
source <directory>/bin/activate
```
- Aggiornare `pip` per installare la libreria hdfs e l'ultima versione della libreria numpy compatibile con Python 3.4:
```
pip install --upgrade pip
pip install hdfs
pip install numpy==1.15.4
```
A questo punto richiamando `pyspark` ci si può rendere conto che esso ora usa Python 3.4 mentre è in esecuzione.

### Trasferimento del progetto nel container
Una volta attivato l'ambiente virtuale con Python 3 è possibile trasferire l'applicativo nel container per cominciare ad utilizzarlo.
- Copiare i file del progetto nel container (eseguire il comando nella directory della macchina fisica in cui si è scaricato il progetto stesso):
```
docker cp --archive -L authorship-main.zip cloudera:/<directory>
```
- Oppure scaricare il progetto direttamente nel container:
```
wget https://github.com/zampierida98/authorship/archive/refs/heads/main.zip -O authorship-main.zip
```
- Estrarre i file del progetto:
```
unzip ./authorship-main.zip
```
- Se si vogliono utilizzare i file autore già allenati durante la fase di test di questo progetto è necessario prima trasferirli su HDFS lanciando il seguente script Python:
```
python3.4 transfer_author_metrics.py
```
- Eseguire il file `main.py` per analizzare nuovi testi sconosciuti (i testi passati in input verranno automaticamente spostati su HDFS):
```
python3.4 main.py -s <dir_testi_sconosciuti>
```
- Oppure eseguire il file `main.py` per aggiungere metriche di nuovi testi ai file degli autori noti (i testi passati in input verranno automaticamente spostati su HDFS):
```
python3.4 main.py -a <dir_testi>
```

### Note
- Durante l'esecuzione potrebbero essere stampati a video numerosi warnings generati da Spark.
- Si ricordano i seguenti comandi utilizzabili per creare nuove directory e per spostare file su HDFS:
```
hadoop fs -mkdir -p /<directory>
hadoop fs -put -f <URI_file_1 ... URI_file_n> /<directory>
```
