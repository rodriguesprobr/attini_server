[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) 
[![CRAN/METACRAN](https://img.shields.io/cran/l/devtools.svg)](http://www.gnu.org/licenses/gpl-3.0.html)

# Attini Environment

[Server (Linux x64 - Python 3.6+ - MySQL/MariaDB)](https://github.com/rodriguesprobr/attini_server "Attini Server x64") | [Client RPi3 (Linux arm - Python 3.6+)](https://github.com/rodriguesprobr/attini_client_rpi3 "Attini Client - RPi 3")

## Server to GNU/Linux

**Author:** Fernando de Assis Rodrigues 
**Contact:** fernando at rodrigues dot pro dot br
**Project from:** [dadosabertos.info](http://dadosabertos.info/projects/attini)

## Clean installation

### Requirements
+ MariaDB or MySQL Server 5+
+ Updated GNU/Linux distro with a seeting network connection and MariaDB/SSH access
+ Python 3.5+
+ Git client

### Clean installation Recipe

We suggest to use /opt/attini as default path installation.
This is the 101 recipe to a clean installation on RPi3/Raspbian:
```
sudo apt-get install git python3-pip python3-dev -y
cd ~/
git clone https://github.com/rodriguesprobr/attini_server.git
sudo mkdir -p /opt/attini
sudo chown user:user /opt/attini 
mv attini_server /opt/attini/server
sudo -H pip3 install /opt/attini/server
```
Also, you may be able to schedule the server at the boot using cron capabilites, as mentioned above:
```
@reboot /usr/bin/python3 /opt/attini/server/attini.py start
# To rebuild timelapse videos every 1 hour, run: 
* */1 * * * /usr/bin/python3 /opt/attini/server/attini.py timelapse
```
