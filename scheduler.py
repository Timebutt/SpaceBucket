# Written by David Neuy
# Version 0.1.0 @ 03.12.2014
# This script was first published at: http://www.home-automation-community.com/
# You may republish it as is or publish a modified version only when you 
# provide a link to 'http://www.home-automation-community.com/'. 

#install dependency with 'sudo easy_install apscheduler' NOT with 'sudo pip install apscheduler'
import os, sys, Adafruit_DHT, time, subprocess
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler

sensor                       = Adafruit_DHT.AM2302 #DHT11/DHT22/AM2302
GPIO_pin                     = 4
sensor_name                  = "SpaceBucket"
temperature_file_path   	 = "data/temperature_" + sensor_name + "_log_" + str(date.today().year) + ".csv"
humidity_file_path      	 = "data/humidity_" + sensor_name + "_log_" + str(date.today().year) + ".csv"
csv_header_temperature       = "Timestamp, Temperature in Celsius\n"
csv_header_humidity          = "Timestamp, Relative Humidity\n"
csv_entry_format             = "{:%Y-%m-%d %H:%M:%S},{:0.1f}\n"
interval_temp			     = 60
interval_webcam				 = 500

def write_header(file_handle, csv_header):
  file_handle.write(csv_header)

def write_value(file_handle, datetime, value):
  line = csv_entry_format.format(datetime, value)
  file_handle.write(line)
  file_handle.flush()

def open_file_ensure_header(file_path, mode, csv_header):
  f = open(file_path, mode, os.O_NONBLOCK)
  if os.path.getsize(file_path) <= 0:
    write_header(f, csv_header)
  return f

def log_DHT_reading():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_pin)
    if hum is not None and temp is not None:
		write_value(file_handler_temperature, datetime.today(), latest_temperature)
		write_value(file_handler_humidity, datetime.today(), latest_humidity)

# Create both file handlers
file_handler_temperature = open_file_ensure_header(hist_temperature_file_path, 'a', csv_header_temperature)
file_handler_humidity  = open_file_ensure_header(hist_humidity_file_path, 'a', csv_header_humidity)

# Ignore first 2 sensor values to improve measurement quality"
for x in range(2):
  Adafruit_DHT.read_retry(sensor, GPIO_pin)

print "Creating interval timer. This step takes almost 2 minutes on the Raspberry Pi..."
# Schedule a job that records temperature and humidity data every {interval} seconds
scheduler = BackgroundScheduler()
scheduler.add_job(log_DHT_reading, 'interval', seconds=interval)
scheduler.start()
print "Started interval timer which will be called the first time in {0} seconds.".format(interval);

try:
  
except (KeyboardInterrupt, SystemExit):
  scheduler.shutdown()

