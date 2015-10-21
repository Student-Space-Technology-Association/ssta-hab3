#!/usr/bin/python3

from sense_hat import SenseHat
import csv
import time
import picamera

sense = SenseHat()

with open('sensor-data.csv','w', newline='') as f:
    writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
    startloop = time.time()

    # Main sensor polling loop
    while True:

        for count in list(range(6)):
            temp = sense.get_temperature()
            pressure = sense.get_pressure()
            humidity = sense.get_humidity()
            cur_time = time.strftime("%H:%M:%S",time.gmtime())
            writer.writerow([cur_time,temp,pressure,humidity])
            time.sleep(10.00 - ((time.time() - startloop) % 10.00))

        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            camera.capture_continuous('img{timestamp:%H-%M-%S}.jpg')

