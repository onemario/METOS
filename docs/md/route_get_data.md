## Min, Max date/time of data: 
### **GET /data/{{STATION-ID}}**

Retrieve min and max date of device data availability. This request can be used to check if device has sent new data which you
can retrieve, by just memorizing last max_date and compare it with current one.

### Specifications

| Specification   | Value             |  
|-----------------|-------------------|
| method          | GET               |
| request         | /data/{{STATION-ID}} |


### URL Parameters

| Value                   | Optional/Required           |  Options                    | Description                |
|-------------------------|-----------------------------|-----------------------------|----------------------------|
| STATION-ID              | Required                    | STRING                      | Unique identifier of a device |

### Body & Schema

N/A

### Response

#### Response codes

| HTTP CODE               | Description                             | 
|-------------------------|-----------------------------------------|
| 200                     | OK                                 |
| 401                     | Unauthorized                            |
| 403                     | No permissions - No rights, CropView type of stations do not support this call              |

#### Response values

Values are self explanatory.