'use strict';

var controllerApp = angular.module('controllerApp', []);
controllerApp.controller('ControllerCtrl', function($scope, $interval, $http) {
	$scope.list = {}
	$scope.intervals = {}
	$scope.user = ''
    $scope.edit_enable = {};

	$scope.init = function(user) {
		$scope.user = user
		$http({
        method: 'GET',
        url: 'user/' + user,

     }).success(function(data){
     	 for(var i = 0; i < data['tasks'].length; i++){
	     		$scope.list[data['tasks'][i]['name']] = data['tasks'][i]['time'];
     	 }
    }).error(function(){
        console.log("error");
    });
	}

	$scope.add = function() {
		$scope.list[$scope.input] = new Date(23*60*60*1000);
		$http({
        method: 'POST',
        url: 'task/' + $scope.user + '/' + $scope.input,
     }).success(function(data){
        console.log("added");
    }).error(function(){
        console.log("error");
    });
	}

	$scope.remove = function(item) {
		delete $scope.list[item];
		$http({
        method: 'DELETE',
        url: 'task/' + $scope.user + '/' + item,
     }).success(function(data){
        console.log("deleted");
    }).error(function(){
        console.log("error");
    });
	}

    $scope.edit = function(item, new_item) {
        if(!$scope.edit_enable[item]){
           $scope.edit_enable[item] = true;
           $scope.item_edit = item
        } else {
            $scope.list[new_item] = $scope.list[item]
            delete $scope.list[item];
            $http({
                method: 'PUT',
                url: 'task_edit/' + $scope.user + '/' + item + '/' + new_item,
             }).success(function(data){
                console.log("edited");
            }).error(function(){
                console.log("error");
            });

        }
    }

	$scope.start = function(item) {
		$scope.intervals[item] = $interval(function(){
			$scope.list[item] -= 1000;
		}, 1000);
	}

	$scope.stop = function(item) {
		$interval.cancel($scope.intervals[item]);
		$http({
        method: 'PUT',
        url: 'task/' + $scope.user + '/' + item + '/' + $scope.list[item],
     }).success(function(data){
        console.log("updated");
    }).error(function(){
        console.log("error");
    });
	}


});
