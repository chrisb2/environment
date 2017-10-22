# Environment Monitor

Monitors temperature and humidity using [Micropython](http://micropython.org/)
on an [ESP8266](https://en.wikipedia.org/wiki/ESP8266) and a  [DHT22](https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf)
sensor and sends the results to [ThingSpeak](https://thingspeak.com).

## Usage

Configure a ThingSpeak channel something like:
![ThingSpeak channel](https://github.com/chrisb2/environment/raw/master/thingspeak-channel-settings.png "ThingSpeak Channel Settings")

Download the [urequests](https://raw.githubusercontent.com/micropython/micropython-lib/master/urequests/urequests.py) HTTP library and create a file called _secrets.py_:
```python
"""Secret values required to connect to services."""
WIFI_SSID = 'XXXXXX'
WIFI_PASSPHRASE = 'XXXXXX'
THINGSPEAK_API_KEY = 'XXXXXX'
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
