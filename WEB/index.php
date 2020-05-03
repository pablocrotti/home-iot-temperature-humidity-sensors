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
    $query = "SELECT DEVICEKEY, DEVICELOC FROM devices_list;";
    //Get the result of the query.
    $result = $conn->query($query);
?>
<html>
<head>
	<meta http-equiv="refresh" content="30">
    <title>Historical Values</title>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.5.0.min.js"></script>
    <script type="text/javascript" src="js/Chart.min.js"></script>

    <script type="text/javascript">
        function display(device_key, sensor_type){
                console.log(device_key)
                $(document).ready(function(){
          $.ajax({
            url : "get_data.php?devicekey="+device_key,
            type : "GET",
            success : function(data){

              var date_array = [];
              var sensor = [];

              for(var i in data) {
                date_array.push(data[i].DATE);
                if (sensor_type == 'temp'){
                  sensor.push(data[i].DEVICETEMP);
                }else{
                  sensor.push(data[i].DEVICEHUM);
                }
              }
              var lbl = "";
              if (sensor_type == 'temp'){
                  lbl = "Temperature";
                }else{
                  lbl = "Humidity";
                }
              var chartdata = {
                labels: date_array,
                datasets: [
                  {
                    label: lbl,
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(59, 89, 152, 0.75)",
                    borderColor: "rgba(59, 89, 152, 1)",
                    pointHoverBackgroundColor: "rgba(59, 89, 152, 1)",
                    pointHoverBorderColor: "rgba(59, 89, 152, 1)",
                    data: sensor
                  }
                ]
              };

              var ctx = $("#" + device_key + sensor_type);
              var lbldisp = "";
              if (sensor_type == 'temp'){
                  lbldisp = "C";
                }else{
                  lbldisp = "%";
                }
              var LineGraph = new Chart(ctx, {
                type: 'line',
                data: chartdata,
                options: {
              scales: {
                  yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: lbldisp
                      }
                  }]
              }     
            }
              });
            },
            error : function(data) {

            }
          });
        });};
    </script>
        <style>
      .chart-container {
        width: 800px;
      }
    </style>
</head>
<body>

    <div class="chart-container" align="center">
    <?
      foreach ($result as $row) {
         if(count($row) > 0)
          {
            echo '<b>'.$row["DEVICELOC"].'</b>';
            echo '<canvas id="'.$row["DEVICEKEY"].'temp" width="800px" height="400px"></canvas>';
            echo '<canvas id="'.$row["DEVICEKEY"].'hum" width="800px" height="400px"></canvas>';
            echo '<script type="text/javascript">display("'.$row["DEVICEKEY"].'", "temp");</script>';
            echo '<script type="text/javascript">display("'.$row["DEVICEKEY"].'", "hum");</script>';
          }
        }
    ?>
    </div>
<?
    $result->close();
    $conn->close();
?>
</body>
</html>