"""
.. module:: app
   :platform: Unix, Windows
   :synopsis: Main app for flask to run.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""
import json
from flask import Flask, request, render_template
from var.devices import trusted_devices
from tools.db import insert_sensor_data
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # Retrieve the data sent from the ESP32 via a GET method.
    received_data = json.loads(request.data.decode("utf-8"))
    # Handshake to verify that the ESP32 is sending the correct information and
    # that it can register its data into the database.
    try:
        # Check that the data has the correct input.
        if ('TEMPERATURE' in received_data.keys()) and ('DEVICE_NAME' in received_data.keys()) and (
                'DEVICE_KEY' in received_data.keys()) and ('HUMIDITY' in received_data.keys()) and (
                'DEVICE_LOCATION' in received_data.keys() and (len(received_data.keys()) == 5)):
            # Check that the device key is authorised to send data to the database.
            if received_data['DEVICE_KEY'] in trusted_devices:
                # Register the current time.
                instantaneous_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
                # Inset the data in the database.
                insert_sensor_data(
                    [received_data['DEVICE_KEY'], received_data['DEVICE_NAME'], received_data['DEVICE_LOCATION'],
                     received_data['TEMPERATURE'], received_data['HUMIDITY'], instantaneous_datetime])
                # For logging purposes, print the output of the data.
                print(instantaneous_datetime, ' data inserted')
                # Return an empty tmeplate to get a 200 response.
                return render_template('index.html')
    except RuntimeError:
        # In case of error or bad access, display an error message.
        print('Wrong handshake')
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
