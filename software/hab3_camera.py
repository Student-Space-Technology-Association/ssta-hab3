#!/usr/bin/python
# -*- coding: utf-8 -*-

# Image capture using Raspberry Pi camera module

import time
import picamera
from fractions import Fraction
import signal,sys

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


imagedir = '/home/pi/hab3-camera_data'

with picamera.PiCamera() as camera:
    camera.resolution = (2592,1944)
    
    #camera.framerate = Fraction(1,6)
    #camera.shutter_speed = 6000000
    #camera.exposure_mode = 'off'
    #camera.iso = 800

    camera.start_preview()
    time.sleep(10)
    
    for filename in camera.capture_continuous(imagedir + 'hab3_img{timestamp:%Y%m%d-%H%M%S}.jpg'):
        print('Captured %s' % filename)
        time.sleep(120) # Wait 2 minutes