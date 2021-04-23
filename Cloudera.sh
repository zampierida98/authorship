#!/bin/bash

sudo rm /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/cloudera-cdh5.repo /etc/yum.repos.d/cloudera-manager.repo

echo "[base]
name=CentOS-6.6 - Base
#mirrorlist=http://mirrorlist.centos.org/?release=6.6&arch=\$basearch&repo=os
baseurl=http://vault.centos.org/6.6/os/\$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6
#released updates 
[updates]
name=CentOS-6.6 - Updates
#mirrorlist=http://mirrorlist.centos.org/?release=6.6&arch=\$basearch&repo=updates
baseurl=http://vault.centos.org/6.6/updates/\$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6
#additional packages that may be useful
[extras]
name=CentOS-6.6 - Extras
#mirrorlist=http://mirrorlist.centos.org/?release=6.6&arch=\$basearch&repo=extras
baseurl=http://vault.centos.org/6.6/extras/\$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6
#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-6.6 - Plus
#mirrorlist=http://mirrorlist.centos.org/?release=6.6&arch=\$basearch&repo=centosplus
baseurl=http://vault.centos.org/6.6/centosplus/\$basearch/
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6
#contrib - packages by Centos Users
[contrib]
name=CentOS-6.6 - Contrib
#mirrorlist=http://mirrorlist.centos.org/?release=6.6&arch=\$basearch&repo=contrib
baseurl=http://vault.centos.org/6.6/contrib/\$basearch/
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6" > /etc/yum.repos.d/CentOS-Base.repo

echo "[cloudera-cdh5]
# Packages for Cloudera's Distribution for Hadoop, Version 5, on RedHat or CentOS 6 x86_64
name=Cloudera's Distribution for Hadoop, Version 5
baseurl=https://archive.cloudera.com/cdh5/redhat/6.6/x86_64/cdh/5/
gpgkey = https://archive.cloudera.com/cdh5/redhat/6.6/x86_64/cdh/RPM-GPG-KEY-cloudera
gpgcheck = 1
enabled=0" > /etc/yum.repos.d/cloudera-cdh5.repo

echo "[cloudera-manager]
name=Cloudera Manager, Version 5
baseurl=http://archive.cloudera.com/cm5/redhat/6/x86_64/cm/5/
gpgkey=http://archive.cloudera.com/cm5/redhat/6/x86_64/cm/RPM-GPG-KEY-cloudera
gpgcheck = 1
enabled=0" > /etc/yum.repos.d/cloudera-manager.repo

sudo yum update
sudo yum install -y epel-release
sudo yum install -y python34
sudo yum install -y python34-setuptools

sudo yum install -y wget
wget https://bootstrap.pypa.io/pip/3.4/get-pip.py -O get-pip.py
python3.4 get-pip.py
pip install --upgrade pip

pip install hdfs
pip install numpy==1.15.4