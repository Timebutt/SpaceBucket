(function(){

  angular
		.module('app')
		.controller('ConfigurationController', [
			'$scope',
			ConfigurationController
		]);

	function ConfigurationController() {
		var vm = this;

		console.log("alive!");
	}

})();
