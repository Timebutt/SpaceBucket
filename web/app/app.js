(function(){
  'use strict';

	var app = angular.module('app', [ 'ngMaterial' ]);
	app.run(function($rootScope, $http) {

		// Fetch system configuration
		$http.get("configuration.json").then(function(response) {

			$rootScope.CONFIG = response.data;

		});

	});

})();
