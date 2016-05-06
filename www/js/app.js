// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var fpaApp = angular.module('fpa', ['ionic']);

fpaApp.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
});

/**
 * The base controller for the app. Will contain any shared data or methods that can be used by the
 * child controllers.
 */
fpaApp.controller('FpaCtrl', ['$scope', function($scope) {
  $scope.state = 'PA';
  $scope.city = 'Pittsburgh';
  $scope.route = 1;
  $scope.results = null;

  $scope.setRoute = function(route) {
    $scope.route = route;
  };

  $scope.setResults = function(results) {
    $scope.results = results;
  };
}]);

/**
 * Search controller that is responsible for collecting user input, fetching the results set,
 * and navigating to a results view (either listing or map).
 */
fpaApp.controller('FpaSearchCtrl', ['$scope', '$ionicLoading', '$ionicTabsDelegate', '$http',
                              function($scope, $ionicLoading, $ionicTabsDelegate, $http) {

      $scope.lov_state = [
        {'lookupCode': 'AL', 'description': 'Alabama'},
        {'lookupCode': 'FL', 'description': 'Florida'},
        {'lookupCode': 'CA', 'description': 'California'},
        {'lookupCode': 'PA', 'description': 'Pennsylvania'}
      ];

      $http({
        method: 'GET',
        url: 'http://10.51.236.201:5000/routes/'
      }).then(function successCallback(response) {
        $scope.routes = response.data.data.routes;
      }, function errorCallback(response) {
      });

      $scope.routes = [];

      $scope.searchRoutes = function(state, city, route) {
        $scope.setRoute(route);
        $http.get('http://10.51.236.201:5000/routes/' + $scope.route + '/').then(function(resp) {
          $scope.setResults(resp.data);
          $ionicTabsDelegate.select(1);
        });
      } 
}]);

/**
 * Listing controller will display addresses and FPA status indicators.
 */
fpaApp.controller('FpaListingCtrl', ['$scope', '$ionicLoading', '$ionicTabsDelegate', '$ionicModal',
                               function($scope, $ionicLoading, $ionicTabsDelegate, $ionicModal) {
  $scope.viewCustomer = function(customer) {
    $scope.selectedCustomer = customer;
    $scope.openModal();
  };

  $scope.viewCustomerOnMap = function(customer) {
    $ionicTabsDelegate.select(2);
  };

  $scope.escalationOnly = function(value, index, array) {
    return value.escalation != null;
  };

  $ionicModal.fromTemplateUrl('my-modal.html', {
    scope: $scope,
    animation: 'slide-in-up'
  }).then(function(modal) {
    $scope.modal = modal;
  });

  $scope.openModal = function() {
    $scope.modal.show();
  };
}]);

/**
 * Map controller will display the current result set in a map view.
 */
fpaApp.controller('FpaMapCtrl', ['$scope', '$ionicLoading', '$ionicTabsDelegate', '$timeout',
                           function($scope, $ionicLoading, $ionicTabsDelegate, $timeout) {
  $scope.initGoogleMaps = function() {
    var myLatlng = new google.maps.LatLng(40.45640550,-79.93191060);
    var mapOptions = {
      center: myLatlng,
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    $timeout(function() {
      $scope.map = new google.maps.Map(document.getElementById("map"), mapOptions);
    }, 0);
  };

  $scope.showMap = function(tabIndex) {
    if (!$scope.map) {
      google.maps.event.addDomListener(window, "load", $scope.initGoogleMaps());
    }
  };

  $scope.centerOnMe = function() {
    if(!$scope.map) {
      return;
    }

    $scope.loading = $ionicLoading.show({
      content: 'Getting current location...',
      showBackdrop: false
    });

    navigator.geolocation.getCurrentPosition(function(pos) {
      $scope.map.setCenter(new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude));
      $scope.loading.hide();
    }, function(error) {
      alert('Unable to get location: ' + error.message);
    });
  };
}]);
