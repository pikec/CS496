var app =angular.module('starter.controllers',[])
app.controller('ListCtrl', function($scope, $http){
	$scope.data=[];
	$http.get('http://projectapi-1371.appspot.com/projects/5066549580791808').success(function(results){
		$scope.data = results.project_id; 
		console.log(results);
	})
	.error(function(results){
		alert("ERROR");
	});
	
	$scope.deleteProj= function(id, $index){
		console.log(id);
		var urlApi = 'http://projectapi-1371.appspot.com/projects/';
		$scope.data.splice($index, 1);
		$http({
			method:"DELETE",
			url: urlApi+id	
		}).success(function(res){
			alert('Project'+ id +' deleted');
		});
	};
	
});

app.controller('AddCtrl', function($scope, $http){
	var urlApi = 'http://projectapi-1371.appspot.com/projects';
	var id = '5066549580791808';
	
	$scope.submits=function(){
		var title = $scope.data.title;
		console.log(title);
		var whom = $scope.data.whom;
		console.log(whom);
		var comm= $scope.data.commisioned;
		console.log(comm);
		var desc = $scope.data.descr;
		console.log(desc);
				
		$http({
				method: 'POST',
				url: urlApi,	
				data:({
						title: title,
						descr: desc,
						comm: comm,
						whom: whom,
						user: id}),
				headers: {'Content-Type': "application/x-www-form-urlencoded"}
		}).success(function(res){
			alert( "Project added");
			console.log(res);
			$scope.data={};
			$scope.addForm.$setPristine();
			$scope.addForm.$setUntouched();
		});
	};

});	

app.controller('ViewCtrl', function($scope, $http, $cordovaLocalNotification){
	var urlApi = 'http://projectapi-1371.appspot.com/projects/';
	var pid = $scope.id;
	console.log(pid);
	$scope.data={};
	
	$http.get(urlApi+pid).success(function(results){
		$scope.data.title = results.title;
		$scope.data.descr = results.description;
		$scope.data.whom = results.whom;
		$scope.data.comm = results.commisioned;	
		console.log(results);
	});
	
	//http://devdactic.com/local-notifications-ionic/
	//http://www.gajotres.net/how-to-use-local-notifications-with-ionic-framework
	$scope.$on("cordovaLocalNotification:added",function(id,state,json){
		alert("Added notification");
	});
	
	$scope.addNotify=function(){
		var msg = $scope.notify.msg;
		var alarmTime = new Date();
		alarmTime.setMinutes(alarmTime.getMinutes()+1);
		$cordovaLocalNotification.schedule({
			id: pid,
			title: "Craft Keeper",
			text: msg,
			at: alarmTime
		}).then(function(results){
			console.log("Notification set");
			$scope.notify.msg="";
			alert("Notificiation set.");
		});
	};
	
	
});

app.controller('EditCtrl', function($scope, $http){
	var urlApi = 'http://projectapi-1371.appspot.com/projects/';
	var pid=$scope.id;
	console.log(pid);

	//get edit initial values
	$http.get(urlApi+pid).success(function(results){
		$scope.edit = {
						title: results.title,
						descr: results.description,
						whom: results.whom,
						comm: results.commisioned};		
	});	

	//put edit
	$scope.edits=function(){
		var object ={
		title: $scope.edit.title,
		whom: $scope.edit.whom,
		comm:  $scope.edit.comm,
		desc: $scope.edit.descr};
		console.log(object);
		
		$http({
				method: 'PUT',
				url: urlApi+pid,
				data: JSON.stringify(object)
			}).success(function(data, status, header, config){
				alert( "Project edited");
				console.log(data);
				console.log(status);
		}). error(function(data, status, header, config){
			console.log(status);
		});		
	};	
	
});
	