"""Monitor temperature and humidity (DHT22) and send results to ThingSpeak."""
from machine import Pin
from utime import sleep_ms, ticks_ms, ticks_diff
import urequests
import dht
import secrets


# Pin constants
_DHT22 = 4    # GPIO04, D2
_LED1 = 16    # GPIO16, D0, Nodemcu led

_THINGSPEAK_URL = ('https://api.thingspeak.com/update?api_key={}'
                   '&field1={}&field2={}&field3={}&field4={}')
_WEATHER_URL = \
    "http://api.wunderground.com/api/{}/conditions/q/NZ/addington.json"
_READING_DELAY_MS = 5 * 60 * 1000  # 5 Minutes

live_led = Pin(_LED1, Pin.OUT, value=1)
sensor = dht.DHT22(Pin(_DHT22))


def run():
    """Main entry point to execute this program."""
    # 1 sec delay to allow DHT22 sensor to start as per datasheet
    sleep_ms(1000)
    last_run = ticks_ms()
    _read()

    while True:
        if ticks_diff(ticks_ms(), last_run) > _READING_DELAY_MS:
            last_run = ticks_ms()
            _read()

        _signal_alive()
        sleep_ms(1000)


def _read():
    try:
        sensor.measure()
        centigrade = sensor.temperature()
        humidity = sensor.humidity()
        print("%.1fC, %.1f%%" % (centigrade, humidity))
        outside_centigrade, outside_humidity = _read_from_wunderground()
        _send_to_thingspeak(centigrade, humidity,
                            outside_centigrade, outside_humidity)
    except Exception as e:
        # Ignore so that program continues running
        print('HTTP request or sensor read failed', e)


def _send_to_thingspeak(temperature, humidity,
                        outside_centigrade, outside_humidity):
    url = _THINGSPEAK_URL.format(secrets.THINGSPEAK_API_KEY,
                                 temperature, humidity,
                                 outside_centigrade, outside_humidity)
    req = urequests.get(url)
    req.close()


def _read_from_wunderground():
    url = _WEATHER_URL.format(secrets.WUNDERGROUND_API_KEY)
    req = urequests.get(url)
    json = req.json()
    req.close()
    outside_temp = json.get('current_observation')['temp_c']
    # Get RH, removing tailing % symbol and converting to integer
    outside_rh = int(json.get('current_observation')['relative_humidity'][:-1])
    return outside_temp, outside_rh


def _signal_alive():
    live_led(False)
    sleep_ms(5)
    live_led(True)
