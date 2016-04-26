#!/usr/bin/python

import time
import picamera
from fractions import Fraction

imagedir = '/home/pi/hab3-camera_data/'

with picamera.PiCamera() as camera:
    vid_time=time.strftime("%H%M%S",time.gmtime())
    camera.resolution = (2592,1944)
    camera.start_preview()
    camera.start_recording(imagedir + 'hab3_video_' + vid_time + '.h264')
    camera.wait_recording(15)
    camera.capture(imagedir + 'hab3_img_' +vid_time + '.jpg', use_video_port=True)
    camera.wait_recording(15)
    camera.stop_recording()