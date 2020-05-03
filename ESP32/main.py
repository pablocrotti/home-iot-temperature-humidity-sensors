"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Main code to send temperature and humidity values to the API server.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""
import time
from tools.connectors import connect_wifi, disconnect_wifi
from tools.webtools import post_data
from tools.sensors import get_dht11_data
from var.static import SLEEP_TIME

if __name__ == '__main__':
    # Main loop of the module.
    while True:
        # Connect the ESP32 module to the network.
        connect_wifi()
        # Retrieve the data from the DHT11 sensors and send it to the API server.
        # Timeout set to 60 seconds for the sending of the data.
        try:
            post_data(get_dht11_data())
        except Exception as e:
            print(e)
        # Disconnect the ESP32 module from the wifi network.
        disconnect_wifi()
        # Wait 60 seconds.
        time.sleep(SLEEP_TIME)
