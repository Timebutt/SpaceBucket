(function(){
  'use strict';

	var app = angular.module('app', [ 'ngMaterial' ]);
	app.run(function($rootScope, $http) {

		// Fetch system configuration
		$http.get("/SpaceBucket/config/config.json").then(function(response) {

			$rootScope.CONFIG = response.data;

		});

	});

})();
