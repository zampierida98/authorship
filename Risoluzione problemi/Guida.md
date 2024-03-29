# Risoluzione dei problemi
Istruzioni per risolvere problemi con Cloudera

## Manager di pacchetti
Innanzitutto bisogna controllare che il manager di pacchetti `yum` funzioni correttamente lanciando il comando `yum update`; se vengono restituiti degli errori effettuare la procedura seguente.
- Scaricare i file `CentOS-Base.repo`, `cloudera-cdh5.repo`, `cloudera-manager.repo` e `cloudera-accumulo.repo` dalla directory `Risoluzione problemi` di questo repository.
- Rimuovere i corrispondenti file su Cloudera:
```
sudo rm -f /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/cloudera-cdh5.repo /etc/yum.repos.d/cloudera-manager.repo /etc/yum.repos.d/cloudera-accumulo.repo
```
- Trasferire su Cloudera i file scaricati:
```
docker cp --archive -L CentOS-Base.repo cloudera:/etc/yum.repos.d/CentOS-Base.repo
docker cp --archive -L cloudera-cdh5.repo cloudera:/etc/yum.repos.d/cloudera-cdh5.repo
docker cp --archive -L cloudera-manager.repo cloudera:/etc/yum.repos.d/cloudera-manager.repo
docker cp --archive -L cloudera-accumulo.repo cloudera:/etc/yum.repos.d/cloudera-accumulo.repo
```

## Installazione di Python 3.4
Se il manager di pacchetti funziona correttamente è possibile installare Python 3.4 con i comandi seguenti.
- Installare Python 3.4 tramite `yum`:
```
sudo yum update
sudo yum install -y epel-release
sudo yum install -y python34
sudo yum install -y python34-setuptools
```
- Installare l'ultima versione di `pip` compatibile con Python 3.4:
```
sudo yum install -y wget
wget https://bootstrap.pypa.io/pip/3.4/get-pip.py -O get-pip.py
python3.4 get-pip.py
```