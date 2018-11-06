#!/usr/bin/python
# -*- coding: utf8 -*-
from attini import db
from attini import util

def execute(epoch, rpiid, photo_bin, ip):
    try:
        db.connect()
        cursor = db.connection.cursor()
        sql = "INSERT INTO photo (epoch, rpiid, photo_bin, ip) VALUES(%s, %s, %s, %s);"
        args = (epoch, rpiid, photo_bin, ip)
        if util.get_config("debug") == True:
            util.log(sql, "attini/photo.py", level = "debug")
            util.log(str(args), "attini/photo.py", level = "debug")
        cursor.execute(sql, args)
        db.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        if e.args[0] == 1062:
            util.log("Warning: duplicate primary key", "attini/photo.py")
            return True
        else:
            util.log("Error: {0} - {1} ".format(str(e.args[0]),str(e.args[1])), "attini/photo.py")
            return False
            
def select_all(rpiid):
    try:
        sql = """
            SELECT
                epoch,
                photo_bin
            FROM photo
            WHERE 1
        """
        sql = sql + " AND rpiid = '{0}' ".format(rpiid)
        sql = sql + " ORDER BY epoch ASC "
        db.connect()
        cursor = db.connection.cursor()
        if util.get_config("debug") == True:
            util.log(sql, "attini/photo.py", level = "debug")
        cursor.execute(sql)
        recordsets = cursor.fetchall()
        cursor.close()
        return recordsets
    except IndexError as e:
        util.log("attini/photo.py IndexError: {0}".format(str(e.args)))
        return False
    except Exception as e:
        util.log("attini/photo.py error: {0} - {1} ".format(str(e.args[0]),str(e.args[1])))
        return False
