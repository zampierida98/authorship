# Authorship attribution
Progetto per l'esame del corso di Big Data

## Struttura del repository
- `texts`: directory contenente 250 testi scritti da 10 autori diversi (25 testi per ogni autore) usati per formare l'insieme degli autori noti
- `author_metrics`: directory contenente i file binari degli autori noti (rappresentano le caratteristiche di stile estratte dai testi da loro scritti)
- `analyze_files`: directory contenente 100 testi usati per testare la classificazione, di cui 50 testi sono di 10 autori già noti al sistema e altri 50 testi sono di 10 autori sconosciuti
- `main.py`: modulo principale da richiamare (ha il compito di eseguire i sottomoduli)
- `authorship.py`: sottomodulo che salva le caratteristiche di stile estratte da uno o più testi (anche di autori diversi) forniti in input
- `analysis.py`: sottomodulo che analizza i testi forniti in input ed esegue un processo di classificazione confrontando le loro caratteristiche di stile con quelle degli autori già noti al sistema

## Installazione
- Controllare che Java Runtime Environment e Python 3 siano installati.
- Controllare che le seguenti librerie Python siano installate (dovrebbero già essere presenti nella libreria Python standard): getopt, math, pickle, shutil, statistics
- Installare le seguenti librerie Python: numpy, hdfs
```
pip install numpy hdfs
```
- Scaricare Apache Spark 3 (per Hadoop 2.7) dal seguente link: https://spark.apache.org/downloads.html
- Estrarre in una directory il contenuto del file scaricato

## Esecuzione su Windows
- Aggiungere la directory in cui si è installato Spark alla variabile d'ambiente `PATH` (sostituire `x` a seconda della versione scaricata):
```
set PATH=%PATH%;<spark_installation_path>\spark-3.x.x-bin-hadoop2.7\bin
```
- Eseguire il file `main.py` tramite l'interprete Python, ad esempio per analizzare i testi in una directory:
```
python main.py -s analyze_files
```

## Esecuzione su Linux
- Aggiungere la directory in cui si è installato Spark alla variabile d'ambiente `PATH` (sostituire `x` a seconda della versione scaricata):
```
export PATH=$PATH:<spark_installation_path>/spark-3.x.x-bin-hadoop2.7/bin
```
- Eseguire il file `main.py` tramite l'interprete Python, ad esempio per analizzare i testi in una directory:
```
python main.py -s analyze_files
```

## Note
- Durante l'esecuzione potrebbero essere stampati a video numerosi warnings generati da Spark.
- Prestare attenzione alla versione di Python chiamata in quanto è necessario chiamare la versione 3; ad esempio potrebbe essere necessario specificare `python3.8`.
- L'esecuzione su Windows richiede tempi maggiori sia rispetto a quella su Linux sia rispetto a quella su Cloudera.