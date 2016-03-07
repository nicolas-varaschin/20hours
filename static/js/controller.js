'use strict';

var controllerApp = angular.module('controllerApp', []);
controllerApp.controller('ControllerCtrl', function($scope) {
	$scope.list = []
	$scope.add = function() {
		$scope.list.push($scope.input);
	}
	
	$scope.remove = function(index) {
		$scope.list.splice(index, 1);
	}
});
