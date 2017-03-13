# SpaceBucket
This project is a work in progress, using a Raspberry Pi 2 controller to closely monitor and control the growth of vegetation inside a Space Bucket. The very informative website [http://www.spacebuckets.com/](http://www.spacebuckets.com/) is your resource when it comes to the construction of the bucket itsself, the gallery is a great place to see what contraptions other people have come up with.

This repository will host all the code I currently use to run my own Space Bucket. As the project unfolds, I will update with images of the actual hardware configuration. Idea is to conceive a growth environment that can - up to certain extent - autonomously adapt certain parameters to enable optimal growth, and to ensure I can leave the Space Bucket alone for a few days (when I am away, forget watering the plant, ...). A configured light schedule assures our vegetation receives all the light it requires, a peristaltic pump waters the plant when the moisture sensor detects that there is not enough water in the soil. Ultimately, even fertilizer (diluted in water) could automatically be dispensed (currently not planned yet - but I know myself, too awesome to tinker with).

# Installation

The code supplied in this repository was tested on a Raspberry Pi running the Jessie Debian distribution. As always, before starting make sure your Raspberry is healthy and up to date:
```
sudo apt-get update
sudo apt-get upgrade
```

[Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT) is required to read the DHT22/AM2302 temperature/humidity sensor.
First, make sure your Raspberry Pi can compile Python scripts, and easily add Python packages through PIP.

```
sudo apt-get install -y build-essential python-dev python-pip
```
Next, get the Python package:
```
pip install adafruit_python_dht
```

The webcam runs using the uv4l package. Installation is documented on the uv4l website, just to make things easier the instructions are repeated here as well:
```
curl http://www.linux-projects.org/listing/uv4l_repo/lrkey.asc | sudo apt-key add -
```
Next, we need to add a new repository to the _/etc/apt/sources.list_ file:
```
sudo nano /etc/apt/sources.list
```
If you are on Raspbian Wheezy, add:
```
deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ wheezy main
```

If you are on Raspbian Jessie, add this line:
```
deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ jessie main
```
Next, we can install the main uv4l package:
```
sudo apt-get update
sudo apt-get install uv4l uv4l-server uv4l-webrtc
```
If you plan on using the Raspberry Pi Camera Module, the following lines will install the required driver and invoque the camera:
```
sudo apt-get install uv4l-raspicam
uv4l --driver raspicam
```
In case you want to use a uvc compliant USB camera (I am using the Logitech C310 webcam), you first need to install the uvc driver:
```
sudo apt-get install uv4l-uvc
```
Next, you can use the ```lsusb``` command to find your specific device and find its device id. This [comprehensive list](http://www.linux-usb.org/usb.ids) can help to verify your device.
```
lsusb
uv4l --driver uvc --device-id 046d:081b
```
