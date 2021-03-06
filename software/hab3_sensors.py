#!/usr/bin/python
# -*- coding: utf-8 -*-

# Data monitoring and recording for Raspberry Pi 2 sensors
# High Altitude Balloon, Series 3 (HAB3)
# Space Technology Student Association, University of Tennnessee, Knoxville, TN

# Necessary modules
from sense_hat import SenseHat
import csv
import time
import Adafruit_BMP.BMP085 as BMP085
import signal, sys
from Adafruit_ADS1x15 import ADS1x15
import RPi.GPIO as GPIO

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        GPIO.cleanup()
        time.sleep(0.01)
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# ADC setup
ADS1015 = 0x00  # 12-bit ADC
gain = 4096     # gain setting for +/- 4.096V range
sps = 250       # 250 samples per second

# Servo and buzzer setup
GPIO.setmode(GPIO.BCM)
buzzer_pin = 4
GPIO.setup(buzzer_pin,GPIO.OUT)
GPIO.output(buzzer_pin,GPIO.LOW)


# Create instances
sense = SenseHat()
BMP_sensor = BMP085.BMP085()
adc = ADS1x15(ic=ADS1015)
pwm = GPIO.PWM(servo_pin,50)

# Set data output directory
data_dir='/home/pi/hab3_sensor_data/'

# Record to a new file each time the script runs
csvfilename = time.strftime("%Y%m%d-%H%M%S",time.gmtime())

# Create CSV files for data recording and write header rows
with open(data_dir + "environment_data_" + csvfilename + '.csv','w') as f:
    writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Time','SenseHat Temperature (°C)','BMP Temperature (°C)','SenseHat Pressure (Pa)','BMP Pressure (Pa)','BMP Altitude (m)','SenseHat Humidity (rel. %)'])

with open(data_dir + "voltage_data" + csvfilename + '.csv','w') as f:
    writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Time','Battery Voltage (V)','Bus A Voltage (V)','Bus B Voltage (V)','Bus C Voltage'])

with open(data_dir + "orientation_data_" + csvfilename + '.csv','a') as f:
    writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Time','Orientation/Pitch (deg)','Orientation/Roll (deg)','Orientation/Yaw (deg)','Direction to Compass North (deg)','Magnetic Intensity/x (uT)','Magnetic Intensity/y (uT)','Magnetic Intensity/z (uT)','Rot. Velocity/x (rad/s)','Rot. Velocity/y (rad/s)','Rot. Velocity/z (rad/s)','Acceleration/x (g)','Acceleration/y (g)','Acceleration/z (g)'])


# Set a repeat interval for the main loop, in seconds
loop_interval = 10

# Set a lower limit on altitude to activate "finding aids" (smoke grenade and buzzer) on descent
altitude_limit = 3048 # meters
BMP_alt = 0 # initialize
finding_activated = 0
activated = 0

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


    # Orientation
    sense.set_imu_config(True,True,True)        # Enable compass, gyro, and accelerometer
    SH_orientation = sense.get_orientation()    # orientation of pitch, roll, yaw axes in degrees
    SH_orientation_x = SH_orientation.get('x')
    SH_orientation_y = SH_orientation.get('y')
    SH_orientation_z = SH_orientation.get('z')

    # Magnetometer data
    #sense.set_imu_config(True,False,False)
    time.sleep(0.01) # sleep for 10 ms after changing IMU configuration
    SH_compass_north = sense.get_compass()      # direction of magnetometer from North, in degrees
    SH_compass_raw = sense.get_compass_raw()    # magnetic intensity of x, y, z axes in microteslas
    SH_compass_raw_x = SH_compass_raw.get('x')
    SH_compass_raw_y = SH_compass_raw.get('y')
    SH_compass_raw_z = SH_compass_raw.get('z')

    # Gyro Data
    #sense.set_imu_config(False,True,False)
    time.sleep(0.01) # sleep for 10 ms after changing IMU configuration
    #SH_gyro = sense.get_gyroscope()             # orientation of pitch, roll, yaw axes in degrees
    SH_gyro_raw = sense.get_gyroscope_raw()     # rotational velocity of pitch, roll, yaw axes in radians per sec
    SH_gyro_raw_x = SH_gyro_raw.get('x')
    SH_gyro_raw_y = SH_gyro_raw.get('y')
    SH_gyro_raw_z = SH_gyro_raw.get('z')

    # Accelerometer data
    #sense.set_imu_config(False,False,True)
    time.sleep(0.01) # sleep for 10 ms after changing IMU configuration
    #SH_accel = sense.get_accelerometer()        # orientation of pitch, roll, yaw axes in degrees
    SH_accel_raw = sense.get_accelerometer_raw()    # acceleration intensity of pitch, roll, yaw axes in 'G's
    SH_accel_raw_x = SH_accel_raw.get('x')
    SH_accel_raw_y = SH_accel_raw.get('y')
    SH_accel_raw_z = SH_accel_raw.get('z')

    ## Readings from the BMP180 installed in the sealed box
    BMP_pressure = BMP_sensor.read_pressure()   # value in Pascals
    BMP_temp = BMP_sensor.read_temperature()    # value in degrees C

    # Altitude readings
    BMP_prev_alt = BMP_alt # keep the previous altitude reading for comparison later
    BMP_alt = BMP_sensor.read_altitude()        # value in meters


    ## Readings from the ADC to monitor battery and bus voltages
    bus_bat = (adc.readADCSingleEnded(3, gain, sps) / 1000) * (3)
    bus_a = (adc.readADCSingleEnded(0, gain, sps) / 1000) * (3)
    bus_b = (adc.readADCSingleEnded(1, gain, sps) / 1000) * (3)
    bus_c = (adc.readADCSingleEnded(2, gain, sps) / 1000) * (3)


    ## Write data to files

    # Write environment sensor data to csv
    with open(data_dir + "environment_data_" + csvfilename + '.csv','a') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([data_time,SH_temp,BMP_temp,SH_pressure,BMP_pressure,BMP_alt,SH_humidity])

    # Write orientation sensor data to csv
    with open(data_dir + "orientation_data_" + csvfilename + '.csv','a') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([data_time,SH_orientation.get('x'),SH_orientation_y,SH_orientation_z,SH_compass_north,SH_compass_raw_x,SH_compass_raw_y,SH_compass_raw_z,SH_gyro_raw_x,SH_gyro_raw_y,SH_gyro_raw_z,SH_accel_raw_x,SH_accel_raw_y,SH_accel_raw_z])
    
    # Write voltage data from ADC to csv
    with open(data_dir + "voltage_data" + csvfilename + '.csv','a') as f:
        writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
        writer.writerow([data_time,bus_bat,bus_a,bus_b,bus_c])


    ## Check if it's time to activate smoke grenade and buzzer
    if BMP_alt < altitude_limit:
        if (BMP_prev_alt - BMP_alt) > 2: # check to see if we are really descending (not measurement fluctuations)--at least 2 meter difference
            if finding_activated < 1:
                GPIO.output(buzzer_pin,GPIO.HIGH)
                print 'Buzzer has been activated.'
                activated = 1



    # Print data to terminal
    print('===========================================')
    print('Time is: '),data_time
    print('-------------------------------------------')
    print('Bus Bat (V): '),bus_bat
    print('Bus A (V):   '),bus_a
    print('Bus B (V):   '),bus_b
    print('Bus C (V):   '),bus_c
    print('-------------------------------------------')
    print('SenseHat temp (°C):      '),SH_temp
    print('BMP180 temp (°C):        '),BMP_temp
    print('SenseHat pressure (Pa):  '),SH_pressure
    print('BMP180 pressure (Pa):    '),BMP_pressure
    print('BMP180 alt (m):          '),BMP_alt
    print('SenseHat humidity (%):   '),SH_humidity
    print('--------------------------------------')
    print('Pitch (deg):  '),SH_orientation_x
    print('Roll (deg):   '),SH_orientation_y
    print('Yaw (deg):    '),SH_orientation_z
    # print('-------------------------------------------')
    # print('Direction to compass north (degrees):    '),SH_compass_north
    # print('Magnetic intensity, x axis (uT):    '),SH_compass_raw_x
    # print('Magnetic intensity, y axis (uT):    '),SH_compass_raw_y
    # print('Magnetic intensity, z axis (uT):    '),SH_compass_raw_z
    print('-------------------------------------------')
    print('Rotat. velocity, x axis (rad/s):   '),SH_gyro_raw_x
    print('Rotat. velocity, y axis (rad/s):   '),SH_gyro_raw_y
    print('Rotat. velocity, z axis (rad/s):   '),SH_gyro_raw_z
    print('-------------------------------------------')
    print('Buzzer and smoke activation status = '),activated
    print('===========================================')

    ## Timekeeping for the loop
    cur_time = time.time() # Update the 'current time' after finishing all tasks

    # Subtract the elapsed time from 'loop_interval' to make each reading happens every 'loop_interval' seconds
    # Note: cur_time - ref_time is the elapsed time and will be extremely small.
    time.sleep(loop_interval - (cur_time-ref_time))
    ref_time = time.time() # Update the 'previous time'
