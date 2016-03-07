'use strict';

var controllerApp = angular.module('controllerApp', []);
controllerApp.controller('ControllerCtrl', function($scope, $interval) {
	$scope.list = {}
	$scope.intervals = {}
	$scope.add = function() {
		$scope.list[$scope.input] = new Date(23*60*60*1000);
	}
	
	$scope.remove = function(item) {
		delete $scope.list[item];
	}

	$scope.start = function(item) {
		$scope.intervals[item] = $interval(function(){ 
			$scope.list[item] -= 1000; 
		}, 1000);
	}

	$scope.stop = function(item) {
		$interval.cancel($scope.intervals[item]);
	}


});
