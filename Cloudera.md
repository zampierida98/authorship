# Esecuzione su Cloudera
Istruzioni per l'esecuzione del progetto su Cloudera

## Installazione di Docker
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

## Manager di pacchetti
Innanzitutto bisogna controllare che il manager di pacchetti `yum` funzioni correttamente lanciando il comando `yum update`. Se vengono restituiti degli errori effettuare la seguente procedura:
- Scaricare i file `CentOS-Base.repo`, `cloudera-cdh5.repo` e `cloudera-manager.repo` dalla directory `File Cloudera` di questo repository.
- Rimuovere i corrispondenti file su Cloudera:
```
sudo rm /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/cloudera-cdh5.repo /etc/yum.repos.d/cloudera-manager.repo
```
- Trasferire su Cloudera i file scaricati:
```
docker cp --archive -L CentOS-Base.repo cloudera:/etc/yum.repos.d/CentOS-Base.repo
docker cp --archive -L cloudera-cdh5.repo cloudera:/etc/yum.repos.d/cloudera-cdh5.repo
docker cp --archive -L cloudera-manager.repo cloudera:/etc/yum.repos.d/cloudera-manager.repo
```
A questo punto il manager di pacchetti dovrebbe funzionare correttamente.

## Predisposizione dell'ambiente virtuale con Python 3
Su Cloudera Pyspark gira di default su Python 2.6; siccome il progetto è stato sviluppato usando Python 3 è necessario installare Python 3.4 (l'ultima versione disponibile per Cloudera) e predisporre un ambiente virtuale in cui Pyspark possa girare su tale versione.
- Installare Python 3.4 tramite `yum`:
```
sudo yum install -y epel-release
sudo yum install -y python34
sudo yum install -y python34-setuptools
```
- Installare ed aggiornare `pip`:
```
curl https://bootstrap.pypa.io/pip/3.4/get-pip.py -o get-pip.py
python3.4 get-pip.py
pip install --upgrade pip
```
- Installare l'ultima versione della libreria numpy compatibile con Python 3.4:
```
pip install numpy==1.15.4
```
- Attivare l'ambiente virtuale in una nuova directory:
```
mkdir <directory>
pyvenv <directory>
source <directory>/bin/activate
```

## Trasferimento del progetto nel container
Una volta attivato l'ambiente virtuale con Python 3 è possibile trasferire il progetto nel container per eseguirlo.
- Copiare i file del progetto nel container (eseguire il comando nella directory della macchina fisica in cui si è scaricato il progetto stesso):
```
docker cp --archive -L authorship-main.zip cloudera:/<directory>/authorship-main.zip
```
- Passare al terminale del container per estrarre i file del progetto appena trasferiti:
```
unzip /<directory>/authorship-main.zip
```
- Eseguire il file `main_hadoop.py` tramite l'interprete Python 3.4 (tale file si occupa anche di spostare su HDFS i testi passati in input):
```
python3.4 main_hadoop.py -s analyze_files
```
Nota: si ricordano i seguenti comandi utilizzabili per creare nuove directory e per spostare file su HDFS
```
hadoop fs -mkdir -p /<directory>
hadoop fs -put -f <URI_file_1 ... URI_file_n> /<directory>
```
