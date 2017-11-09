# Environment Monitor

Monitors temperature and humidity using [MicroPython](http://micropython.org/)
on an [ESP8266](https://en.wikipedia.org/wiki/ESP8266) and a [RHT03 (DHT22)](https://cdn.sparkfun.com/datasheets/Sensors/Weather/RHT03.pdf)
sensor and sends the results to [ThingSpeak](https://thingspeak.com).

## Circuit

The following circuit diagram shows how I connected the sensor to a NodeMcu ESP8266 development board:

![Circuit diagram](https://github.com/chrisb2/environment/raw/master/environment-circuit.png "Circuit Diagram")

## Usage

Configure a ThingSpeak channel something like:

![ThingSpeak channel](https://github.com/chrisb2/environment/raw/master/thingspeak-channel-settings.png "ThingSpeak Channel Settings")

Download the [urequests](https://raw.githubusercontent.com/micropython/micropython-lib/master/urequests/urequests.py) HTTP library and create a file called _secrets.py_:
```python
"""Secret values required to connect to services."""
WIFI_SSID = 'XXXXXX'
WIFI_PASSPHRASE = 'XXXXXX'
THINGSPEAK_API_KEY = 'XXXXXX'
WUNDERGROUND_API_KEY = 'XXXXXX'
```
and copy with the rest of the python files to the ESP8266.

Run the following script from the REPL to load the wifi network.
```python
# Connect to WiFi router
import network
import secrets

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSPHRASE)
wlan.ifconfig()
```
Reboot the ESP8266 to automatically run the program.
