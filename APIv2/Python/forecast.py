import fc_api
import pprint

uri = 'https://api.fieldclimate.com/v2'

#take this keys from https://ng.fieldcliamte.com > User menu > API services > GENERATE NEW
publicKey = 'copy your public key'
privateKey = 'copy your private key'
station_id = '00000146'     # an example demo station

api = fc_api.FcApi(uri, publicKey, privateKey)

#weather forecast main variables:
# precipitation, temperature, r/h, global radiation, wet-bulb temperature, daily ET0,
# wind speed and direction, air pressure, sunshine duration, clouds

#weather forecast: 7x24 hours
response = api.post('/forecast/'+station_id, '{"name":"general7"}').json()

#weather forecast: 3x24 hours
response = api.post('/forecast/'+station_id, '{"name":"general3"}').json()

#get record timestamps
response['dates']

#filter one variable from record identifiers, return all values for the available dates (e.g. 3x24)
temp = list(filter(lambda x: x['name'] == "Temperature", response['data']))[0]['values']['result']
#plot the selected variable "Temperature" with related timestamps
print("{:>21} | {:6}".format("Date Time", "Temperature"))
["{} | {:4.2f}".format(t, v) for t, v in zip(response['dates'], temp)]

#number of forecast variables
len(response['data'])
#iterating through variables
["[{}] {}".format(i, v['name']) for i, v in enumerate(response['data'])]