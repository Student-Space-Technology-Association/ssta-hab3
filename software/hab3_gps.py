#! /usr/bin/python
# Framework written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

# Modules
import os
from gps import *
from time import *
import time
import threading
import csv
import datetime

gps_data_dir = '/home/pi/hab3_gps/'
# Create a new csv file each time the script runs
csvfilename = time.strftime("%Y%m%d-%H%M%S",time.gmtime())

gpsd = None #setting the global variable

os.system('clear') #clear the terminal (optional)

class GpsPoller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global gpsd #bring it in scope
		gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
		self.current_value = None
		self.running = True #setting the thread running to true

	def run(self):
		global gpsd
		while gpsp.running:
			gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


if __name__ == '__main__':
	gpsp = GpsPoller() # create the thread
	try:
		gpsp.start() # start it up
		while True:
			#It may take a second or two to get good data
			#print gpsd.fix.latitude,', ',gpsd.fix.longitude,'	Time: ',gpsd.utc

			os.system('clear')

			print
			print ' GPS reading'
			print '----------------------------------------'
			print 'latitude    ' , gpsd.fix.latitude
			print 'longitude   ' , gpsd.fix.longitude
			print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
			print 'altitude (m)' , gpsd.fix.altitude
			print 'eps         ' , gpsd.fix.eps
			print 'epx         ' , gpsd.fix.epx
			print 'epv         ' , gpsd.fix.epv
			print 'ept         ' , gpsd.fix.ept
			print 'speed (m/s) ' , gpsd.fix.speed
			print 'climb       ' , gpsd.fix.climb
			print 'track       ' , gpsd.fix.track
			print 'mode        ' , gpsd.fix.mode
			print
			print 'sats        ' , gpsd.satellites

			# Open csv file for writing GPS data
			with open(gps_data_dir + 'GPS_Log_' + csvfilename + '.csv','a') as f:
				writer = csv.writer(f,quoting=csv.QUOTE_MINIMAL)
				writer.writerow([gpsd.utc,gpsd.fix.latitude,gpsd.fix.longitude,gpsd.fix.altitude,gpsd.fix.speed,gpsd.fix.climb,gpsd.fix.track])
				print 'Writing csv at ' , datetime.datetime.now().strftime("%H:%M:%S.%f")
			time.sleep(5) #set to whatever, 5 seconds in this case

	except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
		print "\nKilling Thread..."
		gpsp.running = False
		gpsp.join() # wait for the thread to finish what it's doing
	print "Done.\nExiting."
