"""
.. module:: boot
   :platform: Unix, Windows
   :synopsis: Contains the functions loaded when the ESP32 boots.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""
from tools.connectors import connect_wifi

# Connect to the wifi network
connect_wifi()
