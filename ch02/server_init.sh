#!/bin/bash

# pip3 install
sudo apt-get update
sudo apt-get install -y python3-pip
pip3 --version

# python3, pip3 alternatives command
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# install python package
pip install pymongo requests flask beautifulsoup4

# mongodb-Import the public key used by the package management system
sudo apt-get install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -

# mongodb- Install
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org=5.0.2 mongodb-org-database=5.0.2 mongodb-org-server=5.0.2 mongodb-org-shell=5.0.2 mongodb-org-mongos=5.0.2 mongodb-org-tools=5.0.2
sudo mkdir -p /data/db

# Run Mongodb
sudo service mongod start
sleep 15
netstat -tnlp

# setting - create user
mongo admin --eval 'db.createUser({user: "likelion", pwd: "wearethefuture", roles:["root"]});'

# replace config - bindip,security 
sudo sh -c 'echo "security:\n  authorization: enabled" >> /etc/mongod.conf'
sudo sed -i "s,\\(^[[:blank:]]*bindIp:\\) .*,\\1 0.0.0.0," /etc/mongod.conf

# restart mongodb
sudo service mongod stop
sleep 7
sudo service mongod start
sleep 15
netstat -tnlp

# port forwarding
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5000
