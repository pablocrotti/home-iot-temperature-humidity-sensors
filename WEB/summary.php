<?
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
    $query = "SELECT ROUND(sd.DEVICETEMP*(1-dl.DEVICETEMPCALIB),1) AS DEVICETEMP, ROUND(sd.DEVICEHUM*(1-dl.DEVICEHUMCALIB),1) AS DEVICEHUM, dl.DEVICELOC FROM sensor_data sd INNER JOIN (SELECT DEVICEKEY, MAX(DATE) AS MaxDateTime FROM sensor_data GROUP BY DEVICEKEY) groupedtt ON sd.DEVICEKEY = groupedtt.DEVICEKEY AND sd.DATE = groupedtt.MaxDateTime JOIN devices_list dl ON dl.DEVICEKEY = sd.DEVICEKEY;";
    // Get the result of the query.
    $result = $conn->query($query);
?>
<html>
<head>
    <meta http-equiv="refresh" content="30">
    <title>Current Overview</title>
</head>
<body>
    <table border=0>
      <tr>
    <?
      foreach ($result as $row) {
         if(count($row) > 0)
          {
            echo '<tr><td><b>'.$row["DEVICELOC"].'</b></td>';
            echo '<td>'.$row["DEVICETEMP"].'°C </td><td>'.$row["DEVICEHUM"].' %</td></tr>';
          }
        }
    ?>
  </tr></table>
<?
    $result->close();
    $conn->close();
?>
</body>
</html>