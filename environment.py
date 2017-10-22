"""Monitor temperature and humidity (DHT22) and send results to Thingspeak."""
from machine import Pin
from utime import sleep_ms, ticks_ms, ticks_diff
import urequests
import dht
import secrets


# Pin constants
_DHT22 = 4    # GPIO04, D2
_LED1 = 16    # GPIO16, D0, Nodemcu led

_THINGSPEAK_URL = \
    "https://api.thingspeak.com/update?api_key={}&field1={}&field2={}"
_READING_DELAY_MS = 5 * 60 * 1000  # 5 Minutes

live_led = Pin(_LED1, Pin.OUT, value=1)
sensor = dht.DHT22(Pin(_DHT22))


def run():
    # 1 sec delay to allow DHT22 sensor to start as per datasheet
    sleep_ms(1000)
    last_run = ticks_ms()
    read()

    while True:
        if ticks_diff(ticks_ms(), last_run) > _READING_DELAY_MS:
            last_run = ticks_ms()
            read()

        signal_alive()
        sleep_ms(1000)


def read():
    try:
        sensor.measure()
        centigrade = sensor.temperature()
        humidity = sensor.humidity()
        print("%.1fC, %.1f%%" % (centigrade, humidity))
        send_to_thingspeak(centigrade, humidity)
    except Exception as e:
        # Ignore so that program continues running
        print('HTTP request or sensor read failed', e)


def send_to_thingspeak(temperature, humidity):
    url = _THINGSPEAK_URL.format(secrets.THINGSPEAK_API_KEY,
                                 temperature, humidity)
    req = urequests.get(url)
    req.close()


def signal_alive():
    live_led(False)
    sleep_ms(10)
    live_led(True)
