#!/usr/bin/python
# -*- coding: utf8 -*-
from attini import db
from attini import util

def select_all():
    try:
        sql = """
            SELECT
                id
            FROM readings
            GROUP BY id
            ORDER BY id ASC;
        """
        db.connect()
        cursor = db.connection.cursor()
        if util.get_config("debug") == True:
            util.log(sql, "attini/experience.py", level = "debug")
        cursor.execute(sql)
        recordsets = cursor.fetchall()
        cursor.close()
        return recordsets
    except IndexError as e:
        util.log("attini/experience.py IndexError: {0}".format(str(e.args)))
        return False
    except Exception as e:
        util.log("attini/experience.py error: {0} - {1} ".format(str(e.args[0]),str(e.args[1])))
        return False
