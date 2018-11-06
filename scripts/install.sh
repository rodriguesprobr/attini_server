#!/bin/bash

sudo apt-get install git python3-pip python3-dev -y
cd ~/
git clone https://github.com/rodriguesprobr/attini_server.git
sudo mkdir -p /opt/attini
sudo chown user:user /opt/attini 
mv attini_server /opt/attini/server
sudo -H pip3 install /opt/attini/server
