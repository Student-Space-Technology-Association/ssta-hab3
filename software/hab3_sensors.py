#!/usr/bin/python3

# Data collection for SenseHat sensors (temperature, pressure, humidity)

from sense_hat import SenseHat
import csv
import time
import datetime

sense = SenseHat()

csvfilename = time.strftime("%Y%m%d-%H%M%S",time.gmtime())
with open("sensehat_" + csvfilename + '.csv','w', newline='') as f:
    writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
    startloop = time.time()

    # Main sensor polling loop
    while True:

        temp = sense.get_temperature()
        pressure = sense.get_pressure()
        humidity = sense.get_humidity()
        cur_time = time.strftime("%H:%M:%S",time.gmtime())
        writer.writerow([cur_time,temp,pressure,humidity])
        time.sleep(10.00 - ((time.time() - startloop) % 10.00))

