<?php
    header('Content-Type: application/json');
    // IP or hostname of the server.
    $servername = "<server_ip>";
    // Username and password.
    $username = "<server_username>";
    $password = "<server_user_password>";
    // Name of the database.
    $dbName = "<server_database>";
    // Connect to the database.
    $conn = new mysqli($servername, $username, $password, $dbName);
    // Error check.
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }
    // SQL query. Change it accordingly if you have different tables.
    if($_GET["devicekey"]!="")
        {
            $query = "SELECT sd.DATE, ROUND(sd.DEVICETEMP*(1-dl.DEVICETEMPCALIB),1) AS DEVICETEMP, ROUND(sd.DEVICEHUM*(1-dl.DEVICEHUMCALIB),1) AS DEVICEHUM FROM sensor_data AS sd JOIN devices_list AS dl ON sd.DEVICEKEY = dl.DEVICEKEY WHERE sd.DEVICEKEY='".$_GET["devicekey"]."'";
        }
    else
        {
            $query = "SELECT sd.DATE, ROUND(sd.DEVICETEMP*(1-dl.DEVICETEMPCALIB),1) as DEVICETEMP, ROUND(sd.DEVICEHUM*(1-dl.DEVICEHUMCALIB),1) AS DEVICEHUM FROM sensor_data AS sd JOIN devices_list AS dl ON sd.DEVICEKEY = dl.DEVICEKEY;";
        }
    // Get the result of the query.
    $result = $conn->query($query);
    // Read the array of results.
    $data = array();
    foreach ($result as $row) {
       if(count($row) > 0)
        {
            $data[] = $row;
        };
    }
    $result->close();
    $conn->close();
    // Encore the result in a JSON format.
    print json_encode($data);

?>