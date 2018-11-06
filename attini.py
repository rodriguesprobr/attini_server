#!/usr/bin/python
# -*- coding: utf8 -*-
from attini import experience
from attini import photo
from attini import read
from attini import util

import base64
import cgi
import http.server
import os
import subprocess
import sys

class httpHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()

    def do_POST(self):
        try:
            client_ip = self.client_address[0]
            util.log("GET from IP {0}".format(str(client_ip)), "attini.py")
            self._set_headers()
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'],})
        
            epoch = util.get_epoch()
            rpiid = str(form['rpiid'].value)
            air_humidity = str(form['air_humidity'].value)
            air_temperature = str(form['air_temperature'].value)
            soil_moisture = str(form['soil_moisture'].value)
            util.log("rpiid: {0} | Air Humidity {1} | Air Temperature {2} | Soil Moisture {3}".format(\
                str(rpiid),\
                str(air_humidity),\
                str(air_temperature),\
                str(soil_moisture)\
            ), "attini.py")
            inserts = []
            inserts.append([epoch, rpiid, "air_humidity", air_humidity, client_ip])
            inserts.append([epoch, rpiid, "air_temperature", air_temperature, client_ip])
            inserts.append([epoch, rpiid, "soil_moisture", soil_moisture, client_ip])
            read.insert(inserts)
            read.execute()
        except:
            util.log("Error processing POST.", "attini.py")
            self.wfile.write(bytes(str("-1"), "utf8"))

        try:
            photo_bin = base64.b64decode(form['photo_bin'].value.decode('utf8'))
            photo.execute(epoch, rpiid, photo_bin, client_ip)
            util.log("Processed POST image.", "attini.py")
            self.wfile.write(bytes(str("0"), "utf8"))
        except:
            util.log("Error processing POST image.", "attini.py")
            self.wfile.write(bytes(str("-2"), "utf8"))

if __name__ == '__main__':
    args = sys.argv
    action = args[1]
    if action == "start":
        while True:
            try:
                httpd = http.server.HTTPServer(\
                    (util.get_config("server_ip"), util.get_config("server_port")\
                ), httpHandler)
                httpd.serve_forever()
            except KeyboardInterrupt:
                httpd.server_close()
                sys.exit()
            except Exception as e:
                httpd.server_close()
                util.log("Waiting ~10 seconds to restart.", "attini.py")
                util.sleep(5,15)
                pass
    elif action == "timelapse":
        img_path = util.get_config("timelapse_img_path")
        video_path = util.get_config("timelapse_video_path")
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        if not os.path.exists(video_path):
            os.makedirs(video_path)
        
        exps = experience.select_all()
        for exp in exps:
            util.log("Processing the experience #{0}".format(exp["rpiid"]), "attini.py")
            
            exp_path = img_path + "/{0}".format(str(exp["rpiid"]))
            if not os.path.exists(exp_path):
                os.makedirs(exp_path)
            
            photos = photo.select_all(exp["rpiid"])
            util.log("Photos: {0}".format(str(len(photos))), "attini.py")
            
            i = 0;
            for photo_bin in photos:
                photo_bin_data = photo_bin["photo_bin"]
                photo_bin_file_path = exp_path + "/{0}.jpg".format(str(i))
                if len(photo_bin_data) == 0:
                    util.log("Null image: {0}. Skipping...".format(photo_bin["epoch"]), "attini.py")
                else:
                    if not os.path.isfile(photo_bin_file_path):
                        util.log("Creating image to {0} as {1} ".format(photo_bin["epoch"], i), "attini.py")
                        with open(photo_bin_file_path, "wb") as file_data:
                            file_data.write(photo_bin_data)
                    else:
                        util.log("File exists to image to {0} as {1} ".format(photo_bin["epoch"], i), "attini.py")
                    i = i + 1
            if len(photos) > 0:
                proc = subprocess.Popen(["ffmpeg", "-r", "60", "-i", exp_path + "/%d.jpg".format(exp["rpiid"]), "-r", "60", "-y", "-vcodec", "libx264", "-q:v", "3", "{0}/{1}.mp4".format(video_path, exp["rpiid"])])
