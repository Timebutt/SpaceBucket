# Written by David Neuy
# Version 0.1.0 @ 03.12.2014
# This script was first published at: http://www.home-automation-community.com/
# You may republish it as is or publish a modified version only when you
# provide a link to 'http://www.home-automation-community.com/'.

import os, sys, Adafruit_DHT, time, subprocess, signal, logging, json
from Adafruit_ADS1x15 import ADS1x15
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler


sensor                       = Adafruit_DHT.AM2302 #DHT11/DHT22/AM2302
GPIO_pin                     = 4
sensor_name                  = "SpaceBucket"
temperature_file_path   	 = "data/temperature_" + sensor_name + "_LOG.csv"
humidity_file_path      	 = "data/humidity_" + sensor_name + "_LOG.csv"
moisture_file_path			 = "data/moisture_" + sensor_name + "_LOG.csv"
current_values_path			 = "data/sensor_values.json"
csv_header_temperature       = "date,temperature\n"
csv_header_humidity          = "date,humidity\n"
csv_header_moisture			 = "date,moisture\n"
csv_entry_format             = "{:%Y-%m-%d %H:%M:%S},{:0.1f}\n"
interval_sensors		     = 60
interval_webcam				 = 500
ADS1015 					 = 0x00 # 12-bit ADC
ADS1115						 = 0x01	# 16-bit ADC
ADS_sps						 = 250  # 250 samples per second
ADS_gain					 = 4096 # +/- 4.096V


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

# Convert the ADC moisture reading to a relative soil moisture level
def process_moisture_adc(sensor_reading):
    if sensor_reading >= 3:
        return 100;
    elif sensor_reading <= 0.5:
        return 0;
    else:
        # TO-DO: implement function
        return 50;

def read_sensors():
	# Make sure every log uses the same timestamp (easier for plotting later on)
    now = datetime.today()

    # Read soil moisture sensor (ADC value)
	#moisture = adc.readADCSingleEnded(0, gain, sps) / 1000
    moisture = 68
    if moisture is not None:
        write_value(file_handler_moisture, now, moisture)

	# Read DHT22 sensor (temperature and humidity)
	#humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_pin)
    humidity = 72;
    temperature = 17.2;
    if hum is not None and temp is not None:
        write_value(file_handler_temperature, now, temperature)
        write_value(file_handler_humidity, now, humidity)

	# Write current values to JSON file (for easy access with front end)
    sensor_data = {}
    sensor_data['humidity'] = humidity
    sensor_data['temperature'] = temperature
    sensor_data['moisture'] = moisture
    with open(current_values_path, 'w') as outfile:
        json.dump(sensor_data, outfile)

# Create system LOG handler
logger = logging.getLogger('SpaceBucket')
hdlr = logging.FileHandler('SpaceBucket.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

# Create sensor LOG file handlers
file_handler_temperature = open_file_ensure_header(temperature_file_path, 'a', csv_header_temperature)
file_handler_humidity  = open_file_ensure_header(humidity_file_path, 'a', csv_header_humidity)
file_handler_moisture = open_file_ensure_header(moisture_file_path, 'a', csv_header_moisture)

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
#adc = ADS1x15(ic=ADS1115)

# Ignore first 2 sensor values to improve measurement quality"
#for x in range(2):
#  Adafruit_DHT.read_retry(sensor, GPIO_pin)

# Schedule a job that records temperature and humidity data every {interval} seconds
logger.info('Initiating SpaceBucket')
scheduler = BackgroundScheduler()
scheduler.add_job(read_sensors, 'interval', seconds=interval_sensors)
scheduler.start()
logger.info('SpaceBucket successfully started!')
