"""
.. module:: tools.sensors
   :platform: Unix, Windows
   :synopsis: Module containing the functions to export the sensor data.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""

from machine import Pin
import dht

from var.static import DHT11_PIN

# Start the connection with the DHT11 sensor.
DHT11_SENSOR = dht.DHT11(Pin(DHT11_PIN))


def get_dht11_data():
    """ Retrieve the DHT11 sensor data and format them into a dictionary with the temperature and humidity.

    :return: Dictionary with the temperature and humidity recorded by the sensor.
    """
    DHT11_SENSOR.measure()
    temp = DHT11_SENSOR.temperature()
    hum = DHT11_SENSOR.humidity()
    export_data = {'TEMPERATURE': temp,
                   'HUMIDITY': hum}
    return export_data
