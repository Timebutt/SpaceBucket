(function () {
    angular
        .module('app')
        .controller('SensorValuesController', [
			'$interval', '$http',
            SensorValuesController
        ]);

    function SensorValuesController($interval, $http) {
        var vm = this;

		// Initialize the sensor values
		vm.temperature = 0;
		vm.humidity = 0;
		vm.moisture = 0;

		// Periodically fetch the current new values
		refreshSensorData();
        $interval(refreshSensorData, 60000);

		// Function that fetches sensor data from sensor_values.json
		function refreshSensorData() {
			$http({
			  method: 'GET',
			  url: 'sensor_values.json'
			}).then(function(response) {
				vm.temperature = response.data.temperature;
				vm.humidity = response.data.humidity;
				vm.moisture = response.data.moisture;
			}, function(response) {
				console.error("Can't locate sensor_values.json")
			});
		}
    }
})();
