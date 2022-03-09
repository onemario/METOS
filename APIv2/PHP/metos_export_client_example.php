<?php

require_once('metos_api_functions.php');

/* Default parameters */
$output_directory = "enter_your_output_path";

$logging_aggregation = 'hourly';
$use_timezone_info = true;

/* You find your HMAC API keys on https://fieldclimate.com - user menu - API services 
 */
$api_parameters = array(
	'url' => 'https://api.fieldclimate.com/v2',
	'public_key' => '  you find your HMAC keypair on https://fieldclimate.com',
	'private_key' => '   > user menu > api services > FieldClimate'
	);

$hours = 40;
$stations = array(
	'your_device_serialnumber'); // e.g. '0000A123'

/* Modify this array to manipulate your desired output.
 * The order of sensors reflects the order in the output.
 * Only sensors mentioned here are part of the output.
 * The "label" is what will be used as the title per sensor in the output file.
 * The "group" is the sensor group code to look for in the sensor data.
 * The "aggr" is the sensor value aggregation in case more raw values are available than reported.
 *    avg: the average within an interval, 
 *    sum: the summary of values over an interval,
 *    time: a time summary within the interval.
 */
$sensors_to_export = array(
	array(
		'label' => 'air_temperature',
		'group' => '1',
		'aggr' => 'avg'),
	array(
		'label' => 'relative_humidity',
		'group' => '2',
		'aggr' => 'avg'),
	array(
		'label' => 'precipitation',
		'group' => '5',
		'aggr' => 'sum'),
	array(
		'label' => 'wind_speed',
		'group' => '6',
		'aggr' => 'avg'),
	array(
		'label' => 'leaf_wetness',
		'group' => '12',
		'aggr' => 'time'),
	array(
		'label' => 'soil_temperature',
		'group' => '3',
		'aggr' => 'avg'));

/* Iterate through stations: Note: there is a /user/stations API route which gives you all available devices */
foreach($stations as $station) {
	echo "Exporting last ", $hours, " hours of data for ", $station, "\n";
	
	/* extract station timezone */
	$timezone = '';
	if ($use_timezone_info) {
		$station_route = "/station/".$station;
		$json_station_response = get_from_api($api_parameters, $station_route);
    	$station_response = json_decode($json_station_response, true);
		if (array_key_exists('position', $station_response)) {
			if (array_key_exists('timezoneCode', $station_response['position']))
				$timezone = $station_response['position']['timezoneCode'];
		} 	
	}
	/* extract station data */
	$data_route = "/data/".$station."/".$logging_aggregation."/last/".$hours;
	$json_data_response = get_from_api($api_parameters, $data_route);
    $data_response = json_decode($json_data_response, true);
	/* format and export station data */
	$rows = extract_records($sensors_to_export, $data_response, $timezone);
	serialize_records($output_directory."/".$station."_export.csv", $rows);
}

?>
