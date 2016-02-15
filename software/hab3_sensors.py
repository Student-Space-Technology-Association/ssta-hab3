#!/usr/bin/python

# Data collection for R.Pi SenseHat sensors (temperature, pressure, humidity)
# High Altitude Balloon, Series 3 (HAB3)
# Space Technology Student Association, University of Tennnessee, Knoxville, TN

# Necessary modules
from sense_hat import SenseHat
import csv
import time
import Adafruit_BMP.BMP085 as BMP085


# Create instances
sense = SenseHat()
BMP_sensor = BMP085.BMP085()

# Record to a new file each time the script runs
csvfilename = time.strftime("%Y%m%d-%H%M%S",time.gmtime())

# Set a repeat interval for the main loop, in seconds
loop_interval = 10

# Set a reference time at startup for calculating sleep duration in main loop
ref_time = time.time()

# Main sensor polling loop
while True:
    # This time is used for logging purposes in the CSV data file
    data_time = time.strftime("%H:%M:%S",time.gmtime())

    ### Readings from the SenseHat
    ## Environment sensors
    SH_temp = sense.get_temperature()           # value in degrees C
    SH_pressure = sense.get_pressure() * 100    # convert output from millibars to Pascals for consistency
    SH_humidity = sense.get_humidity()          # % relative humidity


    ## Orientation
    sense.set_imu_config(True,True,True)        # Enable compass, gyro, and accelerometer
    SH_orientation = sense.get_orientation()    # orientation of pitch, roll, yaw axes in degrees
    SH_orientation_x = SH_orientation['x']
    SH_orientation_y = SH_orientation['y']
    SH_orientation_z = SH_orientation['z']

    # Magnetometer data
    sense.set_imu_config(True,False,False)
    time.sleep(0.01) # sleep for 10 ms after changing configuration
    SH_compass_north = sense.get_compass()      # direction of magnetometer from North, in degrees
    SH_compass_raw = sense.get_compass_raw()    # magnetic intensity of x, y, z axes in microteslas
    SH_compass_raw_x = SH_compass_raw['x']
    SH_compass_raw_y = SH_compass_raw['y']
    SH_compass_raw_z = SH_compass_raw['z']

    # Gyro Data
    sense.set_imu_config(False,True,False)
    time.sleep(0.01) # sleep for 10 ms after changing configuration
    #SH_gyro = sense.get_gyroscope()             # orientation of pitch, roll, yaw axes in degrees
    SH_gyro_raw = sense.get_gyroscope_raw()     # rotational velocity of pitch, roll, yaw axes in radians per sec
    SH_gyro_raw_x = SH_gyro_raw['x']
    SH_gyro_raw_y = SH_gyro_raw['y']
    SH_gyro_raw_z = SH_gyro_raw['z']

    # Accelerometer data
    sense.set_imu_config(False,False,True)
    time.sleep(0.01) # sleep for 10 ms after changing configuration
    #SH_accel = sense.get_accelerometer()        # orientation of pitch, roll, yaw axes in degrees
    SH_accel_raw = sense.get_accelerometer_raw()    # acceleration intensity of pitch, roll, yaw axes in 'G's
    SH_accel_raw_x = SH_accel_raw['x']
    SH_accel_raw_y = SH_accel_raw['y']
    SH_accel_raw_z = SH_accel_raw['z']

    ## Readings from the BMP180 installed in the sealed box
    BMP_pressure = BMP_sensor.read_pressure()   # value in Pascals
    BMP_alt = BMP_sensor.read_altitude()        # value in meters
    BMP_temp = BMP_sensor.read_temperature()    # value in degrees C


    # Write environment sensor data to csv
    with open("environment_data_" + csvfilename + '.csv','a') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([data_time,SH_temp,BMP_temp,SH_pressure,BMP_pressure,BMP_alt,SH_humidity])

    # Write orientation sensor data to csv
    with open("orientation_data_" + csvfilename + '.csv','a') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([data_time,SH_orientation_x,SH_orientation_y,SH_orientation_z,SH_compass_north,SH_compass_raw_x,SH_compass_raw_y,SH_compass_raw_z,SH_gyro_raw_x,SH_gyro_raw_y,SH_gyro_raw_z,SH_accel_raw_x,SH_accel_raw_y,SH_accel_raw_z])










    cur_time = time.time() # Update the 'current time'

    # Subtract the elapsed time from 'loop_interval' to make each reading happens every 'loop_interval' seconds
    # Note: cur_time - ref_time is the elapsed time and will be extremely small.
    time.sleep(loop_interval - (cur_time-ref_time))
    ref_time = time.time() # Update the 'previous time'
