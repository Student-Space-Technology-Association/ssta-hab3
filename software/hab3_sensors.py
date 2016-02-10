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
    # This time is used for reporting purposes
    current_time = time.strftime("%H:%M:%S",time.gmtime())

    # These readings come from the SenseHat
    temp = sense.get_temperature() # temperature from humidity sensor
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()


    # Write Sensehat data to csv
    with open("sensehat_" + csvfilename + '.csv','a', newline='') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([current_time,temp,pressure,humidity])

    cur_time = time.time() # Update the 'current time'
    # Subtract the elapsed time from 10 to make each reading happen at 10 second intervals
    # Note: cur_time - ref_time is the elapsed time and will be extremely small.
    time.sleep(10.00 - (cur_time-ref_time))
    ref_time = time.time() # Update the 'previous time'
