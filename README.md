# SpaceBucket
Controlling a Space Bucket using a Raspberry Pi 2

# Installation

As always, make sure your Raspberry is healthy and up to date:
```
sudo apt-get update
sudo apt-get upgrade
```

[Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT) is required to read the DHT22/AM2302 temperature/humidity sensor.
First, make sure you Raspberry Pi can compile Python scripts.

```
sudo apt-get install -y build-essential python-dev git
```

Next, install the library:

```
mkdir -p /home/pi/sources  
cd /home/pi/sources  
git clone https://github.com/adafruit/Adafruit_Python_DHT.git  
cd Adafruit_Python_DHT  
sudo python setup.py install 
```

The webcam uses the fswebcam library. Installation is pretty straightforward:
```
sudo apt-get install fswebcam
```
