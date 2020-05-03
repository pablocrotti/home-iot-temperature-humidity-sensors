"""
.. module:: tools.connectors
   :platform: Unix, Windows
   :synopsis: Connectors for the WiFi module and DHT22.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""
import network
from machine import Pin
from var.static import SSID, WIFI_LED_PIN
from var.credentials import PSWD

# Set the network adapter as a global variable.
NET_ADAPTER = network.WLAN(network.STA_IF)
# Set the Access Point and disable it.
NET_AP = network.WLAN(network.AP_IF)
NET_AP.active(False)
# Set the LED Pin and turn it off (value:0).
WIFI_LED = Pin(WIFI_LED_PIN, Pin.OUT)
WIFI_LED.value(0)


def connect_wifi():
    """ Connect the pyFi board to your local wireless network.
        SSID and password as passed as global parameters from
        credentials.wifi
    """
    # If the network adapter isn't connected, start the connection process.
    if not NET_ADAPTER.isconnected():
        # Wake the adapter up.
        NET_ADAPTER.active(True)
        # Send connection request.
        NET_ADAPTER.connect(SSID, PSWD)
        # Turn On the LED.
        WIFI_LED.value(1)
        # Wait for the adapter to connect.
        while not NET_ADAPTER.isconnected():
            pass


def disconnect_wifi():
    """ Disonnect the pyFi board from the local wireless network.
    """
    # Disconnect the network adapter from the wifi.
    NET_ADAPTER.disconnect()
    # Turn Off the LED.
    WIFI_LED.value(0)


def ifconfig():
    """ Return the current interface configuration to the system.

        :return: Dictionary with local IP, subnet and gateway.
    """
    return NET_ADAPTER.ifconfig()
