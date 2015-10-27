import time
import picamera
from fractions import Fraction

imagedir = '/home/jbohling/'

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
        time.sleep(300) # Wait 5 minutes