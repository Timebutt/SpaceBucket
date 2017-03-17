(function () {
    angular
        .module('app')
        .controller('ChartsController', [
			'$http', '$scope',
            ChartsController
        ]);

    function ChartsController($http, $scope) {
        var vm = this;

		// Get temperature data
		$http.get("/SpaceBucket/data/temperature_SpaceBucket_LOG.csv").then(function(response) {
			data = $.csv.toArrays(response.data);
			data.splice(0,1);

			$scope.labels = data.map(function(value,index) { return value[0]; });
			$scope.data[0] = data.map(function(value, index) { return value[1]; });
		});

		// Get humidity data
		$http.get("/SpaceBucket/data/humidity_SpaceBucket_LOG.csv").then(function(response) {
			data = $.csv.toArrays(response.data);
			data.splice(0,1);

			$scope.labels = data.map(function(value,index) { return value[0]; });
			$scope.data[1] = data.map(function(value, index) { return value[1]; });
		});

		// Get moisture data
		$http.get("/SpaceBucket/data/moisture_SpaceBucket_LOG.csv").then(function(response) {			
			data = $.csv.toArrays(response.data);
			data.splice(0,1);

			$scope.labels = data.map(function(value,index) { return value[0]; });
			$scope.data[2] = data.map(function(value, index) { return value[1]; });
		});

		$scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
		$scope.series = ['Temperature', 'Humidity', 'Moisture'];
		$scope.data = [
			[0],
			[0],
			[0]
		];
		$scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
		$scope.options = {
			scales: {
				yAxes: [
				{
				  id: 'y-axis-1',
				  type: 'linear',
				  display: true,
				  position: 'left'
				},
				{
				  id: 'y-axis-2',
				  type: 'linear',
				  display: true,
				  position: 'right'
				}
				]
			}
		};

    }
})();
