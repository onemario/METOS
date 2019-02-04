##  Get last data
### **GET /data/{{STATION-ID}}/{{DATA-GROUP}}/last/{{TIME-PERIOD}}**

Retrieve last data that device sends. We recommend calling **/data/{{STATION-ID}}** first so you can see if
there is any new data.

**NOTE that time period gives you flexibility:**

- Read only X amount of elements
- Read Xh which means X amount of hours
- Read Xd which means X amount of days
- Read Xw which means X amount of weeks
- Read Xm which means X amount of months

You are **limited** to retrieve MAX 10.000 data points.

### Specifications

| Specification   | Value             |  
|-----------------|-------------------|
| method          | GET               |
| request         | /data/{{STATION-ID}}/{{DATA-GROUP}}/last/{{TIME-PERIOD}} |


### URL Parameters

| Value                   | Optional/Required           |  Options                    | Description                |
|-------------------------|-----------------------------|-----------------------------|----------------------------|
| STATION-ID              | Required                    | STRING                      | Unique identifier of a device |
| DATA-GROUP              | Required                    | raw, hourly, daily, monthly  | Device data grouped |
| TIME-PERIOD             | Required                    | Xh, Xd, Xw, Xm, X | X = Number, h = hours, d = days, w = weeks, m = months |

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