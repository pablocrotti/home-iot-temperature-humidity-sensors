Quick project to monitor the temperature and humidity in your rooms and display the current and historical values in your browser.


# Summary

This project runs Micropython on an ESP32 (not tested on ESP8266) using a DHT11 humidity and temperature sensor.
Each device connects onto your private wifi network and sends a reading of temperature and humidity every 60 seconds.
The readings are received via a pseudo API server (here a Raspberry PI 3) which then sends them onto a database (here using MariDB). A simple PHP/JS then displays charts with historical and current temperature/humidity values.

Here the, API endpoint is functions as a simple interface between the ESP32 and the SQL server. It is, de facto, not a real a (REST) API. The term API is used for simplicity.

I have designed and 3D printed a case to host the ESP32 and the DHT11 module. The STL file is available in the `STL` section.

![](https://github.com/pablocrotti/home-iot-temperature-humidity-sensors/blob/master/IMG/esp32_dht11.png | width=100)

![](https://github.com/pablocrotti/home-iot-temperature-humidity-sensors/blob/master/IMG/esp32_3dcase.png | width=100)


# Install

## ESP32

The DHT sensor is connected to the GPIO Pin 14 on the ESP32. You can use any other GPIO pin but you will need to adjust the `DHT11_PIN` value in `ESP32/var/static.py`. A good tutorial for ESP32 and DHT11 is available [here](https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/) .

This part contains the Python files and modifications required to run the ESP32 with the DHT11 (also works with DHT22) and send the temperature and humidity values onto your wifi network and to the API endpoint.

- Install the MicroPython framework and the correct IDF (here using v4) framework. More on this [here](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html).

- Each device needs a unique key (defined in `ESP32/var/static.py`) in order to connect to the "API" server.
Always change the key when you add a new device onto your network
- Add your wifi network SSID in `ESP32/var/static.py` and ESP32/ and its password in `ESP32/var/credentials.py`.
- Upload the content of the ESP32 folder onto your ESP32. Make sur that the dependencies only starts within the ESP32 folder, i.e., when uploading to the ESP32, it should show, e.g., var/tools/sensors.py and not `ESP32/var/toos/sensors.py`

## "API" endpoint

The endpoint functions on a Python flask server. In order to set flask to work as a production server you will need to edit the WSGI configuration file. This is not treated here but you can find information on [this link](https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/).

- Modify the list of authorised devices in `WEB/var/devices.py`
- Modify the database (here MariaDB/MySQL) in `WEB/var/credentials.py`
- Run the Flask instance in the console with: `flask run -h 0.0.0.0 &`  (you can start it using screen if you want to keep the server alive in the background)

## MariaDB

In order to save the data coming from the sensors, you will need to enable a MariaDB/MySQL database. The schemas are available in `MariaDB`.

You can create the sensor_data table with:
~~~~
CREATE TABLE `sensor_data` (
                  `Id` int(11) NOT NULL AUTO_INCREMENT,
                  `DEVICEKEY` varchar(64) NOT NULL,
                  `DEVICENAME` longtext NOT NULL,
                  `DEVICELOC` longtext NOT NULL,
                  `DEVICETEMP` decimal(10,0) NOT NULL,
                  `DEVICEHUM` decimal(10,0) NOT NULL,
                  `DATE` datetime NOT NULL,
                  PRIMARY KEY (`Id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
~~~~
and the device_lists table with:
~~~~
CREATE TABLE `devices_list` (
                  `ID` int(11) NOT NULL AUTO_INCREMENT,
                  `DEVICEKEY` longtext NOT NULL,
                  `DEVICELOC` longtext NOT NULL,
                  `DEVICETEMPCALIB` float NOT NULL,
                  `DEVICEHUMCALIB` float NOT NULL,
                  PRIMARY KEY (`ID`)
                ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
~~~~

## Web Page

These are a simple PHP/JS scripts to display historical values as time series in `WEB/index.php` or the latest inputs in `summary.php`.

- Modify the credentials at the top of each PHP pages in order to conenct to your MariaDB/MySQL server.
- Add the Chart.js [library](https://www.chartjs.org/docs/latest/) in a `js` folder.

If you haven't followed the previous steps in the MariaDB sections, you will need to change the name of the tables in all three php pages.


