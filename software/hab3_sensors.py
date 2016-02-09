#!/usr/bin/python3

# Data collection for R.Pi SenseHat sensors (temperature, pressure, humidity)
# High Altitude Balloon, Series 3 (HAB3)
# Space Technology Student Association, University of Tennnessee, Knoxville, TN


from sense_hat import SenseHat
import serial
import csv
import time

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

#ser.open()
#ser.isOpen()

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

    # Get altitude and pressure from the BMP180
    ser.write('a')
    raw_bmp_info = ''
    while ser.inWaiting() > 0:
        raw_bmp_info += ser.read(1)
    raw_bmp_info = raw_bmp_info.split(',')

    # Write Sensehat data to csv
    with open("sensehat_" + csvfilename + '.csv','a', newline='') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([current_time,temp,pressure,humidity])

    # Write BMP180 data to csv
    with open("bmp180_" + csvfilename + '.csv','a', newline='') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([raw_bmp_info[0],raw_bmp_info[1]])

    # This is assuming we want a separate file for the different sensors
    #with open("bmp180_" + csvfilename + '.csv', 'a', newline='') as f:
    #    writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
    #    writer.writerow([current_time,bmp_info[0],bmp_info[1]])

    cur_time = time.time() # Update the 'current time'
    # Subtract the elapsed time from 10 to make each reading happen at 10 second intervals
    # Note: cur_time - ref_time is the elapsed time and will be extremely small.
    time.sleep(10.00 - (cur_time-ref_time))
    ref_time = time.time() # Update the 'previous time'
