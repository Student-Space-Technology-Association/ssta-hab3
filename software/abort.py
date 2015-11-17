#!/usr/bin/python

# This script implements abort/payload cutdown functionality for the HAB-III as
# required by the FAA.

import RPi.GPIO as GPIO

# Setup GPIO as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

# Initialize output pin
GPIO.output(23, GPIO.LOW)
