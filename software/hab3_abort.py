#!/usr/bin/python3

# This script implements abort/payload cutdown functionality for the HAB-III
# in accordance with FAA requirements.

import RPi.GPIO as GPIO
import sys

# Pick a GPIO pin to connect to the cutdown device
abort_pin = 23

# Setup GPIO as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(abort_pin, GPIO.OUT)

# Initialize output pin
GPIO.output(abort_pin, GPIO.LOW)

# Ask user to confirm abort
abort_confirm = input('Are you REALLY sure you want to abort? [y/n]')
if not abort_confirm or abort_confirm[0].lower() != 'y':
	print('Abort has been canceled.')
	sys.exit(1)

# Activate the relay to cut the balloon shrouds
GPIO.output(abort_pin, GPIO.HIGH)
print('The HAB3 payload is falling now...goodbye.')
sys.exit()