# SpaceBucket
This project is a work in progress, using a Raspberry Pi 2 controller to closely monitor and control the growth of vegetation inside a Space Bucket. The very informative website [http://www.spacebuckets.com/](http://www.spacebuckets.com/) is your resource when it comes to the construction of the bucket itsself, the gallery is a great place to see what contraptions other people have come up with.

This repository will host all the code I currently use to run my own Space Bucket. As the project unfolds, I will update with images of the actual hardware configuration. Idea is to conceive a growth environment that can - up to certain extent - autonomously adapt certain parameters to enable optimal growth, and to ensure I can leave the Space Bucket alone for a few days (when I am away, forget watering the plant, ...). A configured light schedule assures our vegetation receives all the light it requires, a peristaltic pump waters the plant when the moisture sensor detects that there is not enough water in the soil. Ultimately, even fertilizer (diluted in water) could automatically be dispensed (currently not planned yet - but I know myself, too awesome to tinker with).

# Installation

As always, make sure your Raspberry is healthy and up to date:
```
sudo apt-get update
sudo apt-get upgrade
```

[Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT) is required to read the DHT22/AM2302 temperature/humidity sensor.
First, make sure your Raspberry Pi can compile Python scripts.

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
