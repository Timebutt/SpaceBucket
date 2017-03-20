(function () {

    angular
        .module('app')
        .controller('ControlPanelController', [
            '$scope', '$rootScope', '$interval', '$http',
            ControlPanelController
        ]);

    function ControlPanelController($scope, $rootScope, $interval, $http) {
        var vm = this;
	var timer = null;

	// Fetch system status
	function refreshData() {

		$http.get("/SpaceBucket/interface.php").then(function(response) { console.log(response.data);
			$scope.switch_main_light = response.data.main_light;
			$scope.switch_auxiliary_light = response.data.auxiliary_light;
			$scope.switch_fan = response.data.fan;
			$scope.switch_pump = response.data.pump;
		});

	}

	// Set periodic update
	refreshData();
	timer = $interval(function() {
		refreshData();
	}, 10000);

	// Save data to server when switch is clicked
	$scope.$watchGroup(['switch_main_light', 'switch_auxiliary_light', 'switch_fan', 'switch_pump'], function(newValues, oldValues, scope) {

		// Pause the refreshData() routine
		$interval.cancel(timer);

		// Prepare object to be posted
		var post = {
			"main_light": {
				"description": "Main Light",
				"pin": $rootScope.CONFIG['GPIO'].main_light,
				"value": $scope.switch_main_light
			},
			"auxiliary_light": {
				"description": "Auxiliary Light",
				"pin": $rootScope.CONFIG['GPIO'].auxiliary_light,
				"value": $scope.switch_auxiliary_light
			},
			"fan": {
				"description": "Fan",
				"pin": $rootScope.CONFIG['GPIO'].fan,
				"value": $scope.switch_fan
			},
			"pump": {
				"description": "Pump",
				"pin": $rootScope.CONFIG['GPIO'].pump,
				"value": $scope.switch_pump
			}
		}

		// Send the POST request
		$http.post("/SpaceBucket/interface.php", post)
		.then(
			function(response) {

			},
			function(error) {
				console.error("Couldn't POST values: " + error);
			});

		});

		// Resume the refreshData() routine
		timer = $interval(function() {
			refreshData();
		}, 10000);

	}

})();
