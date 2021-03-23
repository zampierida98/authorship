# Riconoscimento di authorship
Progetto per l'esame del corso di Big Data

## Installazione
- Controllare che le seguenti librerie Python siano installate:
	* numpy
	* pickle
	* statistics
	* math
	* timeit
Nota: la maggior parte di queste dovrebbe già essere presente nella libreria standard
- Scaricare Apache Spark 3 (per Hadoop 2.7) dal seguente link: https://spark.apache.org/downloads.html
- Estrarre in una directory il contenuto del file scaricato

## Esecuzione su Windows
- Aggiungere la directory in cui si è installato Spark alla variabile d'ambiente `PATH`:
```
set PATH=%PATH%;<spark_installation_path>\spark-3.x.x-bin-hadoop2.7\bin
```
- Eseguire il file `main.py` tramite l'interprete Python, ad esempio:
```
python main.py -f analyze_files/unknown___1.txt
```

## Esecuzione su Linux
- Aggiungere la directory in cui si è installato Spark alla variabile d'ambiente `PATH`:
```
export PATH=$PATH:<spark_installation_path>/spark-3.x.x-bin-hadoop2.7/bin
```
- Eseguire il file `main.py` tramite l'interprete Python, ad esempio:
```
python main.py -f analyze_files/unknown___1.txt
```
Nota: prestare attenzione alla versione di Python chiamata in quanto è necessario chiamare la versione 3 (ad esempio: `python3.8`)
