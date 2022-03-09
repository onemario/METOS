<?php

/** 
 * Generic GET function to fetch data from FieldClimate API.
 * HMAC authentication is used.
 * @param api_parameters API base URL, user access keys
 * @param route see https://api.fieldclimate.com/v2/docs for options
 * @return json object containing the API response
 */
function get_from_api($api_parameters, $route) {
	/* Date as per RFC2616 - Wed, 25 Nov 2014 12:45:26 GMT */
	$timestamp = gmdate('D, d M Y H:i:s T'); 
	$content_to_sign = "GET".$route.$timestamp.$api_parameters["public_key"];
	$signature = hash_hmac("sha256", $content_to_sign, $api_parameters["private_key"]);

	/* Add required HTTP headers
	 * Authorization: hmac public_key:signature
	 * Date: Wed, 25 Nov 2014 12:45:26 GMT
	 */
	$headers = [
		"Accept: application/json",
		"Authorization: hmac {$api_parameters["public_key"]}:{$signature}",
		"Date: {$timestamp}"
	];

	/* Prepare HTTP request using cURL */
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $api_parameters["url"].$route);
	if (array_key_exists('proxy', $api_parameters)) 
		curl_setopt($ch, CURLOPT_PROXY, $api_parameters["proxy"]);
	curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, FALSE );
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
	curl_getinfo($ch);

	$json_response = curl_exec($ch);
	curl_close($ch);
	return $json_response;
}

/**
 * Function to extract sensor data into a two dimensional array
 * 
 * Every row reprensents one timestamp of logged data = 1 record.
 * There are three optional rows at the beginning each of which is a comment:
 *    the first optionanl row contains sensor labels,
 *    the second optional row contains aggregation type per sensor,
 *    the third optional row contains sensor units.
 * Every column represets one sensor. 
 * The first column contains the timestamp, either as is, or in ISO8601 format if the timezone parameter is used.
 *    
 * The order and selection of sensors (sensor group) is defined in the sensors_to_export parameter.
 * @param sensors_to_export
 * @param data
 * @param timezone
 * @return records a two dimensional array with rows (one row per timestamp) and columns (one column per sensor)
 */
function extract_records($sensors_to_export, $data, $timezone='')
{
	/* Define the target column for the desired sensors to be exported.
	 * Index 0 is reserved for the date/time.
	 * A lookup table to find the appropriate sensor label, column and aggregation 
	 * comes from the sensors_to_export definition array 
	 */
	$group_lookup_table = array();
	$aggr_lookup_table = array();
	$used_datetime_cols = 1;
	$column_index = $used_datetime_cols;
	foreach($sensors_to_export as $sensor) {
		$group_lookup_table[$sensor['group']] = $column_index++;
		$aggr_lookup_table[$sensor['group']] = $sensor['aggr'];	
	}

	/* fixed number of columns for the export: target sensors + 1 (datetime); 
	   default value for sensors is null in case a desired sensor is not found in the data */
	$num_cols = count($sensors_to_export) + $used_datetime_cols;

	$records = array();
	$all_sensor_records = $data['data'];
	$all_dates = $data['dates'];

	/* optional header comment line: sensor names */
	$comment_char = '#';
	if (true) {
		$title_row = array();
		array_push($title_row, $comment_char.'date_time');
		foreach($sensors_to_export as $sensor) {
			array_push($title_row, $sensor['label']);
		}
		array_push($records, $title_row);
	}
	/* optional header comment line: logging period aggregation */
	if (true) {	
		$aggr_row = array();
		array_push($aggr_row, $comment_char);
		foreach($sensors_to_export as $sensor) {
			array_push($aggr_row, $sensor['aggr']);
		}
		array_push($records, $aggr_row);
	}
	/* optional header comment line: sensor unit */
	if (true) {	
		$unit_row = array_fill(0, $num_cols, null);
		$unit_row[0] = $comment_char;
		/* iterate through sensors and extract the unit in the appropriate column */
		foreach($all_sensor_records as $single_sensor_records) {
			if (array_key_exists('unit', $single_sensor_records) and
				array_key_exists('group', $single_sensor_records) and 
				array_key_exists($single_sensor_records['group'], $group_lookup_table)) 
			{
				$group = $single_sensor_records['group'];
				$sensor_column_index = $group_lookup_table[$group];
				$unit_row[$sensor_column_index] = $single_sensor_records['unit'];
			}
		}
		array_push($records, $unit_row);	
	}

	/* iterate through dates */
	foreach($all_dates as $data_index => $single_date) {
		$record = array_fill(0, $num_cols, null);
		/* Datetime is presented in local station timezone */
		$date_str = $single_date;
		if (!empty($timezone)) {
			$date_tmp = DateTime::createFromFormat('Y-m-d H:i:s', $single_date, new DateTimeZone($timezone));
			$date_str = $date_tmp->format(DateTime::ISO8601);
		}		
		$record[0] = $date_str;

		/* iterate through sensors and extract the desired ones in the appropriate column */
		foreach($all_sensor_records as $single_sensor_records) {
			if (array_key_exists('group', $single_sensor_records) and 
				array_key_exists($single_sensor_records['group'], $group_lookup_table)) 
			{
				$group = $single_sensor_records['group'];
				$sensor_column_index = $group_lookup_table[$group];
				$aggr = $aggr_lookup_table[$group];
				/* fill the record for a timestamp */
				$record[$sensor_column_index] = $single_sensor_records['values'][$aggr][$data_index];
			}
		}	
		array_push($records, $record);
	}
	return $records;
}

/**
 * Write all extracted rows (timestamps) and columns (sensors) to a text file in CSV format 
 * 
 * @param filename full path to file including extension
 * @param rows the two-dimensional array to be serialized
 * @param separator the used separator for the CSV serialization
 */
function serialize_records($filename, $rows, $separator = ";") {
	$fh = fopen($filename, 'w') or die("Can't open: $php_errormsg");
	foreach($rows as $row_index => $record) {
		if ($row_index != "0")
			fwrite($fh, "\n");
		$num_cols = count($record);
		/* Associative keys indicating the index (=order) are to be used to get the right order */ 
		for($col_index = 0; $col_index < $num_cols; ++$col_index) {
			if ($col_index == 0)
				fwrite($fh, $record[$col_index]);
			else
				fwrite($fh, $separator.$record[$col_index]);
		}
	}
	fclose($fh) or die("Can't close: $php_errormsg");
}

?>
