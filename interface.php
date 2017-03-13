<?php 

// Include the WiringPi PHP wrapper
ini_set("enable_dl","On");
include('wiringpi.php');

// Read current configuration from configuration.json
$str = file_get_contents('configuration.json');
$configuration = json_decode($str, true);

// Read current GPIO pin states
$states = {};
foreach($configuration['GPIO'] as $key => $value) {
	$states[$key] = (wiringpi::digitalRead($value) == 1) ? true : false;
}

// The script is requesting states for the currently configured GPIO pins, return them in JSON
if($_GET) {
	echo json_encode($states, JSON_PRETTY_PRINT);
}

// The front end posted some new values for the GPIO pins
else if($_POST) {
	
	// Read POST data
	$data = json_decode(file_get_contents('php://input'), true);

	// Read data from states.json
	$str = file_get_contents('states.json');
	$POST_states = json_decode($str, true);

	// Iterate over supplied sensor and set GPIO pins to their requested values
	foreach ($POST_states as $key => $value) {
		
		// Check if the value is different from the current state, and if so: execute BASH script and write JSON file
		if($states[$key] != $value['value']) {
			
			$result = ($value['value'] == true) ? 1 : 0;		
			wiringpi::digitalWrite($value['pin'], $result);
			//echo exec('bash /home/pi/bin/actor.sh ' . $value['pin']. ' ' . $result);
			echo $value['description'] . ": GPIO pin " . $value['pin'] . " set to " . $result . "<br />";	
		}		
	}

}


?>