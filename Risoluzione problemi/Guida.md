# Risoluzione dei problemi
Istruzioni per risolvere problemi con Cloudera

## Manager di pacchetti
Innanzitutto bisogna controllare che il manager di pacchetti `yum` funzioni correttamente lanciando il comando `yum update`; se vengono restituiti degli errori effettuare la procedura seguente.
- Scaricare i file `CentOS-Base.repo`, `cloudera-cdh5.repo` e `cloudera-manager.repo` dalla directory `File Cloudera` di questo repository.
- Rimuovere i corrispondenti file su Cloudera:
```
sudo rm /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/cloudera-cdh5.repo /etc/yum.repos.d/cloudera-manager.repo
```
- Trasferire su Cloudera i file scaricati:
```
docker cp --archive -L CentOS-Base.repo cloudera:/etc/yum.repos.d
docker cp --archive -L cloudera-cdh5.repo cloudera:/etc/yum.repos.d
docker cp --archive -L cloudera-manager.repo cloudera:/etc/yum.repos.d
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
- Scaricare `pip` tramite `curl`:
```
echo "[CityFan]
name=City Fan Repo
baseurl=http://www.city-fan.org/ftp/contrib/yum-repo/rhel$releasever/$basearch/
enabled=1
gpgcheck=0" > /etc/yum.repos.d/city-fan.repo

sudo yum install -y curl

curl -s https://bootstrap.pypa.io/pip/3.4/get-pip.py -o get-pip.py
```
- Installare ed aggiornare `pip`:
```
python3.4 get-pip.py
pip install --upgrade pip
```
- Installare la libreria hdfs e l'ultima versione della libreria numpy compatibile con Python 3.4:
```
pip install hdfs
pip install numpy==1.15.4
```