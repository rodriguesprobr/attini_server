#!/usr/bin/python
# -*- coding: utf8 -*-
import hashlib
import json
import logging
import random
import time

logging.basicConfig(level=logging.DEBUG)

configuration_path = "/opt/attini/server/config.json"

def log(
        message = "",\
        source = "N/A",\
        level = "info"\
):
    if get_config("log_enabled") == True:
        logger = logging.getLogger(source)
        if level == "debug":
            if get_config("debug") == True:
                logger.debug("["+str(int(time.time()))+"] " + message)
        else:
            logger.info("["+str(int(time.time()))+"] " + message)

def get_epoch():
    return int(time.time())
    
def get_md5(string):
    md5 = hashlib.md5()
    md5.update(string)
    return str(md5.hexdigest())
    
def get_config(attribute):
    global configuration_path
    return json.load(open(configuration_path, "r"))[attribute]
    
def get_random_int(value_min, value_max):
    random_int = random.randint(value_min, value_max)
    log("Random int generated from {0} - {1}: {2}".format(str(value_min), str(value_max), str(random_int)), "attini/util.py", level = "debug")
    return random_int
    
def get_random_record(recordsets):
    return random.choice(recordsets)
    
def sleep(value_min = 1, value_max = 1):
    value_random = get_random_int(value_min, value_max)
    if get_config("debug") == True:
        for seconds in range(0,value_random):
            log("{0}s".format(seconds), "attini/util.py", level = "debug")
            time.sleep(1)
    else:
        time.sleep(value_random)
