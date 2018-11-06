#!/usr/bin/python
# -*- coding: utf8 -*-
import attini.util as util
import MySQLdb
import MySQLdb.cursors

connection = None

def connect():
    try:
        util.log("Connecting to MySQL...", "attini/db.py", level = "debug")
        global connection
        if connection == None:
            connection = MySQLdb.connect(\
                host = util.get_config("db_ip"),\
                user = util.get_config("db_user"),\
                passwd = util.get_config("db_password"),\
                db = util.get_config("db_name"),\
                cursorclass = MySQLdb.cursors.DictCursor,\
                charset = 'utf8'\
            )
        else:
            util.log("Connected!", "attini/db.py", level = "debug")
    except MySQLdb.Error as e:
        util.log("Error: {0} - {1} ".format(str(e.args[0]),str(e.args[1])), "attini/db.py", level = "debug")

def disconnect():
    connection.close()
    util.log("Disconnected from MySQL.", "attini/db.py", level = "debug")

