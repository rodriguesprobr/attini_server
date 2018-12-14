#!/usr/bin/python
# -*- coding: utf8 -*-
from attini import experience
from attini import photo
from attini import util

from PIL import Image, ImageDraw, ImageFont
import subprocess
import sys
import os

if __name__ == '__main__':
    args = sys.argv
    action = args[1]
    if action == "create_image_buffer":
        img_path = util.get_config("timelapse_img_path")
        video_path = util.get_config("timelapse_video_path")
        exps = experience.select_all()
        
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        if not os.path.exists(video_path):
            os.makedirs(video_path)
        
        for exp in exps:
            util.log("Processing the experience #{0}".format(exp["id"]), "timelapse.py")
            
            exp_path = img_path + "/{0}".format(str(exp["id"]))
            if not os.path.exists(exp_path):
                os.makedirs(exp_path)
                
            photos = sorted(os.listdir(exp_path))
            last_photo_epoch = photos[-1][:-4] if len(photos) > 0 else 0
            
            photos = photo.select_all(\
                id = exp["id"],\
                last_photo_epoch = last_photo_epoch\
            )
            util.log("Photos: {0}".format(str(len(photos))), "timelapse.py")
            
            for photo_bin in photos:
                photo_bin_data = photo_bin["photo_bin"]
                photo_bin_file_path = exp_path + "/{0}.jpg".format(str(photo_bin["epoch"]))
                if len(photo_bin_data) == 0:
                    util.log("Null image: {0}. Skipping...".format(photo_bin["epoch"]), "timelapse.py")
                else:
                    if not os.path.isfile(photo_bin_file_path):
                        util.log("Creating image to {0} as {1} ".format(photo_bin["epoch"], photo_bin_file_path), "timelapse.py")
                        with open(photo_bin_file_path, "wb") as file_data:
                            file_data.write(photo_bin_data)
                        util.log("Injecting information box in {0} ".format(photo_bin_file_path), "timelapse.py")
                        photo_file = Image.open(photo_bin_file_path)
                        photo_file_draw = ImageDraw.Draw(photo_file)
                        photo_file_draw.rectangle(\
                            [0, 0, photo_file.size[0], 15],\
                            fill = (0, 0, 0, 120)\
                        )
                        photo_file_draw.text(\
                            (2,2),\
                            "Attini: {0} - {1}".format(\
                                exp["id"],\
                                util.epoch_to_datetime(photo_bin["epoch"])\
                            ),\
                            font = ImageFont.truetype(util.get_config("timelapse_font_truetype_file_path"), 12),\
                            fill = (255, 255, 255)\
                        )
                        photo_file.save(photo_bin_file_path)
                    else:
                        util.log("File exists to image to {0} as {1} ".format(photo_bin["epoch"], i), "timelapse.py")
    elif action == "create_video_files":
        img_path = util.get_config("timelapse_img_path")
        video_path = util.get_config("timelapse_video_path")
        exps = experience.select_all()
        
        for exp in exps:
            util.log("Processing the experience #{0}".format(exp["id"]), "timelapse.py")
            
            exp_path = img_path + "/{0}".format(str(exp["id"]))
            photos = sorted(os.listdir(exp_path))
            
            if not os.path.exists(video_path + "/" + exp["id"]):
                    os.makedirs(video_path + "/" + exp["id"])
            
            merge = False
            while len(photos) > 3600:
                merge = True
                util.log("More than 3600 photo files are found. Processing a new video...", "timelapse.py")
                templist_file = exp_path + "/templist.txt"
                with open(templist_file, "w") as file:
                    for photo_file in photos[:3600]:
                        file.write("file '" + exp_path + "/" + photo_file + "'\n")
                file.close()
                proc = subprocess.Popen(["ffmpeg", "-r", "60", "-f", "concat", "-safe", "0", "-i", templist_file, "-r", "60", "-y", "-vcodec", "libx264", "-q:v", "3", "{0}/{1}/{2}-{3}.mp4".format(video_path, exp["id"], photos[1][:-4], photos[3600][:-4])])
                proc.wait()
                for photo_file in photos[:3600]:
                    os.remove(exp_path + "/" + photo_file)
                os.remove(templist_file)
                photos = sorted(os.listdir(exp_path))
                util.log("Looping...", "timelapse.py")
            if merge == True:
                util.log("Merging generated videos...", "timelapse.py")
                videos = sorted(os.listdir(video_path + "/" + exp["id"]))
                templist_file = "{0}/{1}/templist_video-merge.txt".format(video_path, exp["id"])
                with open(templist_file, "w") as file:
                    if videos[-1] == "timelapse.mp4":
                        util.log("Found {0}/{1}/timelapse.mp4".format(video_path, exp["id"]), "timelapse.py")
                        file.write("file '{0}/{1}/timelapse.mp4'\n".format(video_path, exp["id"]))
                    for video_file in (videos if videos[-1] != "timelapse.mp4" else videos[:-1]):
                        file.write("file '{0}/{1}/{2}'\n".format(video_path, exp["id"], video_file))
                file.close()
                proc = subprocess.Popen(["ffmpeg", "-r", "60", "-f", "concat", "-safe", "0", "-i", templist_file, "-r", "60", "-y", "-vcodec", "libx264", "-q:v", "3", "{0}/{1}/temp.mp4".format(video_path, exp["id"])])
                proc.wait()
                with open(templist_file, "w") as file:
                    for video_file in (videos if videos[-1] != "timelapse.mp4" else videos[:-1]):
                        util.log("Removing {0}/{1}/{2}".format(video_path, exp["id"], video_file), "timelapse.py")
                        os.remove("{0}/{1}/{2}".format(video_path, exp["id"], video_file))
                util.log("Removing {0}/{1}/templist_video-merge.txt".format(video_path, exp["id"]), "timelapse.py")
                os.remove("{0}/{1}/templist_video-merge.txt".format(video_path, exp["id"]))
                if os.path.isfile("{0}/{1}/timelapse.mp4".format(video_path, exp["id"])):
                    util.log("Removing old {0}/{1}/timelapse.mp4".format(video_path, exp["id"]), "timelapse.py")
                    os.remove("{0}/{1}/timelapse.mp4".format(video_path, exp["id"]))
                util.log("Refreshing {0}/{1}/timelapse.mp4".format(video_path, exp["id"]), "timelapse.py")
                os.rename("{0}/{1}/temp.mp4".format(video_path, exp["id"]), "{0}/{1}/timelapse.mp4".format(video_path, exp["id"]))
