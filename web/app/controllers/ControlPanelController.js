(function () {

    angular
        .module('app')
        .controller('ControlPanelController', [
            '$scope', '$rootScope', '$interval', '$http',
            ControlPanelController
        ]);

    function ControlPanelController($scope, $rootScope, $interval, $http) {
        var vm = this;

		// Fetch system status
		function refreshData() {

			$http.get("states.json").then(function(response) {
				$scope.switch_main_light = response.data.main_light;
				$scope.switch_auxiliary_light = response.data.auxiliary_light;
				$scope.switch_fan = response.data.fan;
				$scope.switch_pump = response.data.pump;
			});

		}

		// Set periodic update
		refreshData();
		$interval(function() {
			refreshData();
		}, 1000);

		// Save data to server
		$scope.click_switch = function() {

			// Prepare object to be posted
			var post = {
				"main_light": {
					"description": "Main Light",
					"pin": $rootScope.CONFIG.GPIO_main_light,
					"value": true
				},
				"auxiliary_light": {
					"description": "Auxiliary Light",
					"pin": $rootScope.CONFIG.GPIO_auxiliary_light,
					"value": true
				},
				"fan": {
					"description": "Fan",
					"pin": $rootScope.CONFIG.GPIO_fan,
					"value": true
				},
				"pump": {
					"description": "Pump",
					"pin": $rootScope.CONFIG.GPIO_pump,
					"value": true
				}
			}

			// Send the POST request
			//$http.post("http://" + $rootScope.CONFIG.IP + ":" + $rootScope.CONFIG.port, post)
			$http.post("http://localhost/bash_execute.php", post)
			.then(
				function() {
					console.log("petse");
				},
				function(error) {
					console.error("Couldn't POST values: " + error);
				});

		};

    }

})();
