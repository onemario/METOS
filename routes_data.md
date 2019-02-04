## ROUTES - DATA

Retrieving your device, forecast and disease model data with help of VIEW (Please refer to **VIEW** documentation under **INFO** section). 

You are **limited** to retrieve MAX 10.000 data points.

### Schemas

| Schema                  | Function                    | 
|-------------------------|-----------------------------|
| schemas/View.json | Select your view    |

### Routes

| HTTP Method   |    Endpoint    | URL Params | Function                           |
| ------------- |----------------|------------| -----------------------------------|
| GET           | /data/*{{STATION-ID}}* | STATION-ID       | Min and Max date of data availability |
| GET           | /data/*{{STATION-ID}}*/*{{DATA-GROUP}}*/last/*{{TIME-PERIOD}}* | FORMAT, STATION-ID, DATA-GROUP, TIME-PERIOD       | Reading last data              |
| GET           | /data/*{{STATION-ID}}*/*{{DATA-GROUP}}*/from/*{{FROM-UNIX-TIMESTAMP}}*/to/*{{TO-UNIX-TIMESTAMP}}* | FORMAT, STATION-ID, DATA-GROUP, FROM-UNIX-TIMESTAMP, TO-UNIX-TIMESTAMP       | Reading data of specific time period           |
| POST          | /chart/*{{STATION-ID}}*/*{{DATA-GROUP}}* | TYPE, STATION-ID, DATA-GROUP       | Works only for forecast VIEWs |
| POST          | /data/*{{STATION-ID}}*/*{{DATA-GROUP}}*/last/*{{TIME-PERIOD}}* | FORMAT, STATION-ID, DATA-GROUP, TIME-PERIOD       | Select your VIEW      |
| POST          | /data/*{{STATION-ID}}*/*{{DATA-GROUP}}*/from/*{{FROM-UNIX-TIMESTAMP}}*/to/*{{TO-UNIX-TIMESTAMP}}* | FORMAT, STATION-ID, DATA-GROUP, FROM-UNIX-TIMESTAMP, TO-UNIX-TIMESTAMP       | Select your VIEW    |

### URL Parameters

| Value                   | Optional/Required           |  Options                    | Description                |
|-------------------------|-----------------------------|-----------------------------|----------------------------|
| STATION-ID              | Required                    | STRING                      | Unique identifier of a device |
| DATA-GROUP              | Required                    | raw, hourly, daily, monthly  | Device data grouped |
| TIME-PERIOD             | Required                    | Xh, Xd, Xw, Xm, X | X = Number, h = hours, d = days, w = weeks, m = months |
| FROM-UNIX-TIMESTAMP     | Required                    | Unix timestamp	| Date/Time in unix timestamp | 
| TO-UNIX-TIMESTAMP       | Optional                    | Unix timestamp  | Date/Time in unix timestamp, if not specified data will be taken till last available |