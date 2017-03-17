<?php

$currentRegime = 'flowering';

// Write something to the log file
function writeToLog($line) {
    $line = date("Y-m-d H:i:s") . " | " . $line . PHP_EOL;
    $fp = fopen('log/log.log', 'a');
    fwrite($fp, $line);
}

// Read current configuration from configuration.json
$str = file_get_contents('config/light-schedule.json');
$schedule = json_decode($str, true);

$str = file_get_contents('config/config.json');
$configuration = json_decode($str, true);

// Read current GPIO pin states
foreach($configuration['GPIO'] as $key => $value) {
	$states[$key] = exec("/usr/bin/gpio read " . $value['pin']);
}

// Check if any switch needs to be enabled
foreach($schedule as $key => $value) {

    if($value['enabled'] == true) {

        // Light is supposed to turn on right now
        if(strtotime(date('H:i')) - strtotime($value[$currentRegime]['on']) <= 60 && $states[$key] == 0) {
            exec("/usr/bin/gpio write " . $configuration['GPIO'][$key]['pin'] . " " . 1);
            writeToLog("GPIO pin " . $configuration['GPIO'][$key]['pin'] . " set to ON");
        }

        else if(strtotime(date('H:i')) - strtotime($value[$currentRegime]['off']) <= 60 && $states[$key] == 1) {
            exec("/usr/bin/gpio write " . $configuration['GPIO'][$key]['pin'] . " " . 0);
            writeToLog("GPIO pin " . $configuration['GPIO'][$key]['pin'] . " set to OFF");
        }
    }
    
}

 ?>
