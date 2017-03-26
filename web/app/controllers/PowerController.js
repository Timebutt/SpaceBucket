(function () {
    angular
        .module('app')
        .controller('PowerController', [
			'$http', '$scope', '$rootScope', '$interval',
            PowerController
        ]);

    function PowerController($http, $scope, $rootScope, $interval) {
        var vm = this;

        // Fetch system status
    	function refreshData() {

    		$http.get("/SpaceBucket/data/power.json").then(function(response) {

                // Set run time per consumer (in hours)
                $scope.hoursMainLight = (response.data['main_light'] / 60).toFixed(2)
                $scope.hoursAuxiliaryLight = (response.data['auxiliary_light'] / 60).toFixed(2)
                $scope.hoursPump = (response.data['pump'] / 60).toFixed(2)
                $scope.hoursFan = (response.data['fan'] / 60).toFixed(2)

                // Calculate power consumption (in kWh)
                $scope.powerMainLight = (response.data['main_light'] / 60 * $rootScope.CONFIG['powerConsumption'].main_light / 1000).toFixed(2);
                $scope.powerAuxiliaryLight = (response.data['auxiliary_light'] / 60 * $rootScope.CONFIG['powerConsumption'].auxiliary_light / 1000).toFixed();
                $scope.powerPump = (response.data['pump'] / 60 * $rootScope.CONFIG['powerConsumption'].pump / 1000).toFixed(2);
                $scope.powerFan = (response.data['fan'] / 60 * $rootScope.CONFIG['powerConsumption'].fan / 1000).toFixed(2);

    		});

    	}

    	// Set periodic update
    	refreshData();
    	timer = $interval(function() {
    		refreshData();
    	}, 10000);

    }
})();
