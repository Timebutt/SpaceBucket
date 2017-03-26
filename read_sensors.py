#!/usr/bin/python

import os, sys, Adafruit_DHT, time, subprocess, signal, logging, json
from Adafruit_ADS1x15 import ADS1x15
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler


path                    = "/home/pi/SpaceBucket/"
sensor                  = Adafruit_DHT.AM2302 #DHT11/DHT22/AM2302
GPIO_pin                = 4
sensor_name             = "SpaceBucket"
temperature_file_path   = "data/temperature_" + sensor_name + "_LOG.csv"
humidity_file_path      = "data/humidity_" + sensor_name + "_LOG.csv"
moisture_file_path      = "data/moisture_" + sensor_name + "_LOG.csv"
current_values_path     = "data/sensor_values.json"
log_file_path           = "log/SpaceBucket.log"
config_file_path	= "config/config.json"
power_file_path 	= "data/power.json"
csv_header_temperature  = "date,temperature\n"
csv_header_humidity     = "date,humidity\n"
csv_header_moisture     = "date,moisture\n"
csv_entry_format        = "{:%Y-%m-%d %H:%M:%S},{:0.1f}\n"
interval_sensors        = 60
interval_webcam         = 500
ADS1015                 = 0x00 # 12-bit ADC
ADS1115                 = 0x01	# 16-bit ADC
ADS_sps                 = 250  # 250 samples per second
ADS_gain                = 4096 # +/- 4.096V


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

# Create system LOG handler
logger = logging.getLogger('SpaceBucket')
logger.setLevel(logging.INFO)
hdlr = logging.FileHandler(path + log_file_path)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

# Read the config file
with open(path + config_file_path) as configFile:
    config = json.load(configFile)

# Create sensor LOG file handlers
file_handler_temperature = open_file_ensure_header(path + temperature_file_path, 'a', csv_header_temperature)
file_handler_humidity  = open_file_ensure_header(path + humidity_file_path, 'a', csv_header_humidity)
file_handler_moisture = open_file_ensure_header(path + moisture_file_path, 'a', csv_header_moisture)

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
#adc = ADS1x15(ic=ADS1115)

# Ignore first 2 sensor values to improve measurement quality"
for x in range(2):
    Adafruit_DHT.read_retry(sensor, GPIO_pin)

# Make sure every log uses the same timestamp (easier for plotting later on)
now = datetime.today()

# If a switch is on, add the time since last run of this script as 'on time'
with open(path + power_file_path) as powerFile:
    powerItems = json.load(powerFile)
    for powerItem in powerItems:
	if int(subprocess.check_output(['gpio', 'read', str(config['GPIO'][powerItem])])) == 0:
	    powerItems[powerItem] = powerItems[powerItem] + config['sensorInterval']
with open(path + power_file_path, 'w') as powerFile:
    json.dump(powerItems, powerFile)

# Check if any switch needs to be operated
with open(path + 'config/switches.json') as switchFile:
    switchConfig = json.load(switchFile)
    for switch in switchConfig:

        if switchConfig[switch]['enabled'] is True and switchConfig[switch]['vegetative']['on'] == (now.strftime('%H:%M') + ':00'):
		subprocess.call(['gpio', 'write', str(switchConfig[switch]['GPIO-PIN']), '0'])
		logger.info('Switch ' + switch + ' enabled. Rise and shine!')
        elif switchConfig[switch]['enabled'] is True and switchConfig[switch]['vegetative']['off'] == (now.strftime('%H:%M') + ':00'):
		subprocess.call(['gpio', 'write', str(switchConfig[switch]['GPIO-PIN']), '1'])
                logger.info('Switch ' + switch + ' disabled. Nighty night!')


# Read soil moisture sensor (ADC value)
# moisture = adc.readADCSingleEnded(0, gain, sps) / 1000
moisture = 68
if moisture is not None:
    write_value(file_handler_moisture, now, moisture)

# Read DHT22 sensor (temperature and humidity)
humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_pin)
if humidity is not None and temperature is not None:
    write_value(file_handler_temperature, now, temperature)
    write_value(file_handler_humidity, now, humidity)

# Write current values to JSON file (for easy access with front end)
sensor_data = {}
sensor_data['humidity'] = '{0:.2f}'.format(humidity)
sensor_data['temperature'] = '{0:.2f}'.format(temperature)
sensor_data['moisture'] = moisture
with open(path + current_values_path, 'w') as outfile:
    json.dump(sensor_data, outfile)

logger.info('Sensor values written')
