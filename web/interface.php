<?php

// Display all errors for this script (handy during development)
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Read current configuration from configuration.json
$str = file_get_contents('../config/config.json');
$configuration = json_decode($str, true);

// Read current GPIO pin states
foreach($configuration['GPIO'] as $key => $value) {
	$states[$key] = (exec("/usr/bin/gpio read " . $value) == '0') ? true : false;
}

// Read POST input
$input = file_get_contents('php://input');

// The script is requesting states for the currently configured GPIO pins, return them in JSON
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
	echo json_encode($states, JSON_PRETTY_PRINT);
}

// The front end posted some new values for the GPIO pins
elseif ($input != "") {

	// Read POST data
	$data = json_decode($input, true);

	// Iterate over supplied sensor and set GPIO pins to their requested values
	foreach ($data as $key => $value) {

		// Check if the value is different from the current state, and if so: execute BASH script and write JSON file

		if($states[$key] != $value['value']) {
			exec("/usr/bin/gpio write " . $value['pin'] . " " . (($value['value'] == false) ? "1" : "0"));
		}
	}

}


?>
