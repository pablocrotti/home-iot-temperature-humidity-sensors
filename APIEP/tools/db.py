"""
.. module:: tools.db
   :platform: Unix, Windows
   :synopsis: Contains the connectors to the MySQL database.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""

import mysql.connector
from var.credentials import SQL_SERVER, SQL_USER, SQL_PASSWD, SQL_DB


def insert_sensor_data(data):
    """ Inset the data submitted via the GET method into the MySQL database.

    :param data: Dictionary with the data to insert into the MySQL database.
    :type data: Dictionary

    :return: Dictionary with the temperature and humidity recorded by the sensor.
    """
    try:
        connection = mysql.connector.connect(host=SQL_SERVER,
                                             user=SQL_USER,
                                             passwd=SQL_PASSWD,
                                             db=SQL_DB)
        # Start a cursor on the connection.
        cursor = connection.cursor()
        sensor_data_query = "INSERT INTO sensor_data (DEVICEKEY, DEVICENAME, DEVICELOC, DEVICETEMP, DEVICEHUM, DATE) " \
                            "VALUES ('{}', '{}', '{}', {}, {}, '{}');"
        sensor_data_query = sensor_data_query.format(data[0], data[1], data[2], data[3], data[4], data[5])
        # Execute the SQL query.
        cursor.execute(sensor_data_query)
        # Commit query.
        connection.commit()
        # Close the cursor and connection.
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(e)
