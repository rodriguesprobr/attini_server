       _   _   _       _                                
  __ _| |_| |_(_)_ __ (_)  ___  ___ _ ____   _____ _ __ 
 / _` | __| __| | '_ \| | / __|/ _ \ '__\ \ / / _ \ '__|
| (_| | |_| |_| | | | | | \__ \  __/ |   \ V /  __/ |   
 \__,_|\__|\__|_|_| |_|_| |___/\___|_|    \_/ \___|_|   
                                                        
by Fernando de Assis Rodrigues 
fernando at rodrigues dot pro dot br

More info at http://dadosabertos.info/projects/attini/?lang=en_EN

We suggest to use /opt/attini as default path installation.
Also, you may be able to schedule on cron the server starts and timelapse builder as mentioned above:

@reboot /usr/bin/python3 /opt/attini/server/attini.py start 
* */2 * * * /usr/bin/python3 /opt/attini/server/attini.py timelapse
