(function () {
    angular
        .module('app')
        .controller('FeedController', [
			'$http', '$scope',
            FeedController
        ]);

    function FeedController($http, $scope) {
        var vm = this;

    }
})();
