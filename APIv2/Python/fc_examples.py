import fc_api
import pprint

uri = 'https://api.fieldclimate.com/v2'

#take this keys from https://ng.fieldcliamte.com > User menu > API services > GENERATE NEW
publicKey = 'copy your public key'
privateKey = 'copy your private key'

station_id = '00000146'     # an example demo station

api = fc_api.FcApi(uri, publicKey, privateKey)

pprint.pprint(api.get('/user/stations').json())

pprint.pprint(api.get('/station/'+station_id).json())
pprint.pprint(api.get('/data/'+station_id+'/raw/from/1574985549/to/1574988303').json())
pprint.pprint(api.get('/data/'+station_id+'/raw/last/24h').json()['data'])
pprint.pprint(api.get('/data/'+station_id+'/hourly/last/2d').json()['data'])
pprint.pprint(api.get('/data/'+station_id+'/daily/last/7d').json()['data'])

pprint.pprint(api.get('/chart/highchart/'+station_id+'/hourly/last/1d').json())
pprint.pprint(api.get('/chart/image/'+station_id+'/raw/last/16').json())