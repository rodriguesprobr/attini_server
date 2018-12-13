#!/usr/bin/python
# -*- coding: utf8 -*-
from attini import db
from attini import util

def execute(epoch, id, photo_bin, ip):
    try:
        db.connect()
        cursor = db.connection.cursor()
        sql = "INSERT INTO photo (epoch, id, photo_bin, ip) VALUES(%s, %s, %s, %s);"
        args = (epoch, id, photo_bin, ip)
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
            
def select_all(\
    id,\
    last_photo_epoch = 0\
):
    try:
        sql = """
            SELECT
                epoch,
                photo_bin
            FROM photo
            WHERE 1
        """
        sql = sql + " AND id = '{0}' ".format(id)
        if int(last_photo_epoch) > 0:
            sql = sql + " AND epoch > {0} ".format(last_photo_epoch)
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
