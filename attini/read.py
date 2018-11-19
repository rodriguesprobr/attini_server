#!/usr/bin/python
# -*- coding: utf8 -*-
from attini import db
from attini import util

tuples = []

def insert(inserts):
    global tuples
    tuples = inserts
    
def clean():
    global tuples
    tuples = []

def execute():
    try:
        global tuples
        if len(tuples) > 0:
            db.connect()
            cursor = db.connection.cursor()
            for t in tuples:
                sql = "INSERT INTO readings (epoch, id, type, read_value, ip) VALUES  ({0}, '{1}', '{2}', '{3}', '{4}');".format(\
                    t[0],\
                    t[1],\
                    t[2],\
                    t[3],\
                    t[4]\
                )
                if util.get_config("debug") == True:
                    util.log(sql, "attini/readings.py", level = "debug")
                cursor.execute(sql)
            db.connection.commit()
            cursor.close()
            return True
        else:
            util.log("Error: SQL ERROR", "attini/readings.py")
            return False
    except Exception as e:
        if e.args[0] == 1062:
            util.log("Warning: duplicate primary key", "attini/readings.py")
            return True
        else:
            util.log("Error: {0} - {1} ".format(str(e.args[0]),str(e.args[1])), "attini/readings.py")
            return False
