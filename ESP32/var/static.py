"""
.. module:: var.static
   :platform: Unix, Windows
   :synopsis: Contains the static variables.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""

# DHT11 Variables.
DHT11_PIN = 14  # GPIO Pin number 14

# API URL.
SERVER_URL = 'http://<flask_ip>:5000'

# Wifi SSID.
SSID = '<your_ssdi>'

# Pin Out.
WIFI_LED_PIN = 2

# Device Parameters.
DEVICE_NAME = '<Sensor Name>'
DEVICE_LOCATION = 'Room 1'
DEVICE_KEY = 'Device 1'
DEVICE_DATA = {'DEVICE_KEY': DEVICE_KEY,
               'DEVICE_NAME': DEVICE_NAME,
               'DEVICE_LOCATION': DEVICE_LOCATION
               }
SLEEP_TIME = 60
