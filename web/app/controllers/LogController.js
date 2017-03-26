(function () {
    angular
        .module('app')
        .controller('LogController', [
			'$http', '$scope',
            LogController
        ]);

    function LogController($http, $scope) {
        var vm = this;

        $http.get("/SpaceBucket/log/SpaceBucket.log").then(function(response) {

            result = response.data.replace(/(?:\r\n|\r|\n)/g, '<br />');
            result = result.replace(/INFO/g, '<b>INFO</b>');
            result = result.replace(/ERROR/g, '<span style="color: red;"><b>ERROR</b></span>');
            result = result.replace(/enabled/g, '<span style="color: green;">enabled</span>');

            $scope.log = result;

		});

    }
})();
