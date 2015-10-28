#!/usr/bin/python3

# Data collection for R.Pi SenseHat sensors (temperature, pressure, humidity)
# High Altitude Balloon, Series 3 (HAB3)
# Space Technology Student Association, University of Tennnessee, Knoxville, TN


from sense_hat import SenseHat
import csv
import time

sense = SenseHat()

# Record to a new file each time the script runs
csvfilename = time.strftime("%Y%m%d-%H%M%S",time.gmtime())

# Set a reference time at startup for calculating sleep duration in main loop
ref_time = time.time()

# Main sensor polling loop
while True:

    temp = sense.get_temperature() # temperature from humidity sensor
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()
    current_time = time.strftime("%H:%M:%S",time.gmtime())

    with open("sensehat_" + csvfilename + '.csv','a', newline='') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([current_time,temp,pressure,humidity])

    time.sleep(10.00 - ((time.time() - ref_time) % 10.00))
