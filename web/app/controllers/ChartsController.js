(function () {
    angular
        .module('app')
        .controller('ChartsController', [
			'$http', '$scope',
            ChartsController
        ]);

    function ChartsController($http, $scope) {

		// Get temperature data
		$http.get("/SpaceBucket/data/temperature_SpaceBucket_LOG.csv").then(function(response) {
			data = $.csv.toArrays(response.data);
			data.splice(0,1);
            data.splice(0, data.length - 100);

			$scope.labels = data.map(function(value,index) { return value[0]; });
			$scope.data[0] = data.map(function(value, index) { return value[1]; });
		});

		// Get humidity data
		$http.get("/SpaceBucket/data/humidity_SpaceBucket_LOG.csv").then(function(response) {
			data = $.csv.toArrays(response.data);
			data.splice(0,1);
            data.splice(0, data.length - 100);

			$scope.labels = data.map(function(value,index) { return value[0]; });
			$scope.data[1] = data.map(function(value, index) { return value[1]; });
		});

		// Get moisture data
		$http.get("/SpaceBucket/data/moisture_SpaceBucket_LOG.csv").then(function(response) {
			data = $.csv.toArrays(response.data);
			data.splice(0,1);
            data.splice(0, data.length - 100);

			$scope.labels = data.map(function(value,index) { return value[0]; });
			$scope.data[2] = data.map(function(value, index) { return value[1]; });
		});

		$scope.labels = [];
		$scope.series = ['Temperature', 'Humidity', 'Moisture'];
		$scope.data = [
			[0],
			[0],
			[0]
		];
		$scope.datasetOverride = [
            {
                yAxisID: 'A'
            },
            {
                yAxisID: 'B'
            },
            {
                yAxisID: 'B'
            }];
		$scope.options = {
			scales: {
				yAxes: [
				{
                    id: 'A',
                    type: 'linear',
                    display: true,
                    position: 'left',
                    ticks: {

                    }
				},
				{
				  id: 'B',
				  type: 'linear',
				  display: true,
				  position: 'right'
				}
				]
			}
		};

    }
})();
