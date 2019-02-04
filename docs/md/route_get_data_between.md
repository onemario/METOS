##  Get data between period
### **GET /data/{{STATION-ID}}/{{DATA-GROUP}}/from/{{FROM-UNIX-TIMESTAMP}}/to/{{TO-UNIX-TIMESTAMP }}**

Retrieve data between specified time periods. We recommend calling **/data/{{STATION-ID}}** first so you can see if
there is any new data. Times from and to need to be specified in unix timestamp.

You are **limited** to retrieve MAX 10.000 data points.

### Specifications

| Specification   | Value             |  
|-----------------|-------------------|
| method          | GET               |
| request         | /data/{{STATION-ID}}/{{DATA-GROUP}}/from/{{FROM-UNIX-TIMESTAMP}}/to/{{TO-UNIX-TIMESTAMP }} |


### URL Parameters

| Value                   | Optional/Required           |  Options                    | Description                |
|-------------------------|-----------------------------|-----------------------------|----------------------------|
| STATION-ID              | Required                    | STRING                      | Unique identifier of a device |
| DATA-GROUP              | Required                    | raw, hourly, daily, monthly  | Device data grouped |
| FROM-UNIX-TIMESTAMP     | Required                    | Unix timestamp	| Date/Time in unix timestamp | 
| TO-UNIX-TIMESTAMP       | Optional                    | Unix timestamp  | Date/Time in unix timestamp, if not specified data will be taken till last available  |

### Body & Schema

N/A

### Response

#### Response codes

| HTTP CODE               | Description                             | 
|-------------------------|-----------------------------------------|
| 200                     | OK                                 |
| 400                     | Data over limit                         |
| 401                     | Unauthorized                            |
| 403                     | No permissions - No rights              |
| 406                     | Specified params are not acceptable     |

#### Response values

Values are self explanatory.