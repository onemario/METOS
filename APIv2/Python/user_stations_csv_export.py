import fc_api
import json
import datetime as dt
import pytz
import csv

''' FC API config '''
uri = 'https://api.fieldclimate.com/v2/'
publicKey = '  you find your HMAC keypair on https://fieldclimate.com'
privateKey = '   > user menu > api services > FieldClimate'


################################################################
# Report all /user/station device settings and the device status
################################################################

''' helper function to load the mnc, mcc, country lookup file '''
def get_mcc_file():
    with open('mcc-mnc-table.json') as json_file:
        data = json.load(json_file)
    return data

''' helper function to produce the header line for the export file '''
def get_header():
    return(["index","serial","name",
            "longitude", "latitude", "altitude",
            "device","country","measuring_interval",
            "logging_interval","fixed_transfer_interval","min_date","max_date","last_communication","timezoneCode",
            "utc_offset","battery_level[mV]","rssi[%]","bearer_type","sim_id","hardware","firmware"])
            
''' helper function to produce the device content as a single line '''
def get_station(index, station, mcc_list):
    print('{}'.format(station['name']))
    cname = station['name']['custom'].strip()
    mcc_list = list(filter(lambda x: x["mcc"] == station['networking']['mcc'], mcc_list)) if 'networking' in station and 'mcc' in station['networking'] else []
    return(
        [index,
        station['name']['original'],
        cname,
        station['position']['geo']['coordinates'][0] if 'position' in station and station['position'] is not None and 'geo' in station['position'] and 'coordinates' in station['position']['geo'] and station['position']['geo']['coordinates'] != [] else '',
        station['position']['geo']['coordinates'][1] if 'position' in station and station['position'] is not None and 'geo' in station['position'] and 'coordinates' in station['position']['geo'] and station['position']['geo']['coordinates'] != [] else '',
        station['position']['altitude'] if 'position' in station and station['position'] is not None and 'altitude' in station['position'] else '',
        station['info']['device_name'],
        #get country from mcc using a lookup dictionary
        mcc_list[0]['country'] if mcc_list != [] and 'country' in mcc_list[0] else '',
        station['config']['measuring_interval'] if 'measuring_interval' in station['config'] else '',
        station['config']['logging_interval'] if 'logging_interval' in station['config'] else '',
        station['config']['fixed_transfer_interval'] if 'fixed_transfer_interval' in station['config'] else '',
        #show days only to be able to filter, sort and better see transmission problems
        station['dates']['min_date'].split(' ')[0] if 'min_date' in station['dates'] else '',
        station['dates']['max_date'].split(' ')[0] if 'max_date' in station['dates'] else '',
        station['dates']['last_communication'].split(' ')[0],
        station['position']['timezoneCode'] if station['position'] and 'timezoneCode' in station['position'] else '',
        dt.datetime.now(pytz.timezone(station['position']['timezoneCode'])).strftime('%z') if station['position'] and 'timezoneCode' in station['position'] and station['position']['timezoneCode'] else '',
        station['meta']['battery'] if station['meta'] and 'battery' in station['meta'] else '',
        station['networking']['rssi_pct'] if 'networking' in station and 'rssi_pct' in station['networking'] else '',
        station['networking']['type'] if 'networking' in station and 'type' in station['networking'] else '',
        station['networking']['simid'] if 'networking' in station and 'simid' in station['networking'] else '',
        station['info']['hardware'] if 'hardware' in station['info'] else '',
        station['info']['firmware'] if 'firmware' in station['info'] else ''])


# instantiate the FC API helper for your user account
api = fc_api.FcApi(uri, publicKey, privateKey)

''' writes a csv file for all your devices '''
def write_station_list_to_csv(filename='your_filename.csv'):
    # mobile network lookup file: helps to convert mobile network country code to country name
    mcc_list = get_mcc_file()
    # get devices information for your account
    stations = api.get('/user/stations').json()
    # create header and station information lines and serialize them
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t')
        csv_writer.writerow(get_header())
        for index, station in enumerate(stations):
            csv_writer.writerow(get_station(index, station, mcc_list))

#execute the serialization
write_station_list_to_csv()