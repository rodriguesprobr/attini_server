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
import simplejson
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
            util.log("POST from IP {0}".format(str(client_ip)), "attini.py")

            self._set_headers()

            util.log("- Host: {0}".format(str(self.headers['Host'])), "attini.py")
            util.log("- User-Agent: {0}".format(str(self.headers['User-Agent'])), "attini.py")
            util.log("- Connection: {0}".format(str(self.headers['Connection'])), "attini.py")
            util.log("- Content-Type: {0}".format(str(self.headers['Content-Type'])), "attini.py")
            util.log("- Content-Length: {0}".format(str(self.headers['Content-Length'])), "attini.py")
            
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            util.log("- Data: {0}".format(str(self.data_string)), "attini.py")
            
            self.send_response(200)
            self.end_headers()
            
            data = simplejson.loads(self.data_string.decode('utf8'))
            util.log("- JSON Data: {0}".format(str(data)), "attini.py")
            
            util.log("Processing JSON...", "attini.py")
            if 'id' in data:
                json_return = "{\"code\": \"0\", \"message\":\"Sent data was stored on server.\"}\r\n";
                
                read_inserts = []
                
                id = data['id']            
                util.log("ID: {0}".format(id), "attini.py")
                
                epoch = util.get_epoch()
                util.log("Epoch time: {0}".format(epoch), "attini.py")
                
                if 'photo_bin' in data:
                    if str(data['photo_bin']) != '0':
                        photo.execute(epoch, id, base64.b64decode(data['photo_bin'].encode('utf8')), client_ip)
                    else:
                        json_return = "{\"code\": \"-7\", \"message\":\"Photo datum was not found on dataset sent.\" }\r\n";
                        self.wfile.write(bytes(str(json_return), "utf8"))
                else:
                    json_return = "{\"code\": \"-6\", \"message\":\"Photo datum was not found on dataset sent.\" }\r\n";
                    self.wfile.write(bytes(str(json_return), "utf8"))
                
                if 'air_humidity' in data:
                    read_inserts.append([epoch, id, "air_humidity", str(data['air_humidity']), client_ip])
                else:
                    json_return = "{\"code\": \"-5\", \"message\":\"Air humidity datum was not found on dataset sent.\" }\r\n";
                    self.wfile.write(bytes(str(json_return), "utf8"))
                    
                if 'air_temperature' in data:
                    read_inserts.append([epoch, id, "air_temperature", str(data['air_temperature']), client_ip])
                else:
                    json_return = "{\"code\": \"-4\", \"message\":\"Air temperature datum was not found on dataset sent.\" }\r\n";
                    self.wfile.write(bytes(str(json_return), "utf8"))
                    
                if 'soil_moisture' in data:
                    read_inserts.append([epoch, id, "soil_moisture", str(data['soil_moisture']), client_ip])
                else:
                    json_return = "{\"code\": \"-3\", \"message\":\"Soil moisture datum was not found on dataset sent.\" }\r\n";
                    self.wfile.write(bytes(str(json_return), "utf8"))
                    
                read.insert(read_inserts)
                read.execute()
                util.log("Saved.", "attini.py")
                util.log("Return JSON is {0}.".format(str(json_return)), "attini.py")
                self.wfile.write(bytes(str(json_return), "utf8"))
            else:
                util.log("ID not found. Error: -2", "attini.py")
                json_return = "{\"code\": \"-2\", \"message\":\"ID datum was not found on dataset sent.\" }\r\n";
                self.wfile.write(bytes(str(json_return), "utf8"))
        except Exception as e:
            util.log("Error: {0}".format(str(e)), "attini.py")
            util.log("Error processing POST. Error: -1", "attini.py")
            json_return = "{\"code\": \"-1\", \"message\":\"Something gone wrong when dataset was processing.\" }\r\n";
            self.wfile.write(bytes(str(json_return), "utf8"))

if __name__ == '__main__':
    args = sys.argv
    action = args[1]
    if action == "start":
        while True:
            try:
                util.log("Starting Attini server at {0}:{1}".format(util.get_config("server_ip"), util.get_config("server_port")), "attini.py", "debug")
                httpd = http.server.HTTPServer((\
                    util.get_config("server_ip"),\
                    util.get_config("server_port")\
                ), httpHandler)
                util.log("Serving forever at {0}:{1}".format(util.get_config("server_ip"), util.get_config("server_port")), "attini.py", "debug")
                httpd.serve_forever()
            except KeyboardInterrupt:
                util.log("Closing service at {0}:{1}".format(util.get_config("server_ip"), util.get_config("server_port")), "attini.py", "debug")
                httpd.server_close()
                sys.exit()
            except Exception as e:
                util.log("Closing service at {0}:{1}".format(util.get_config("server_ip"), util.get_config("server_port")), "attini.py", "debug")
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
            util.log("Processing the experience #{0}".format(exp["id"]), "attini.py")
            
            exp_path = img_path + "/{0}".format(str(exp["id"]))
            if not os.path.exists(exp_path):
                os.makedirs(exp_path)
            
            photos = photo.select_all(exp["id"])
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
                proc = subprocess.Popen(["ffmpeg", "-r", "60", "-i", exp_path + "/%d.jpg".format(exp["id"]), "-r", "60", "-y", "-vcodec", "libx264", "-q:v", "3", "{0}/{1}.mp4".format(video_path, exp["id"])])
