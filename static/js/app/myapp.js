// appli Angular
var app = angular.module('DashboardAPI', ['ngMaterial', 'ngAnimate', 'ngMessages', 'toolbar']);

// controlleur principal
app.controller('mainControl', function($scope, $window) {
    //
    var ua =  $window.navigator.userAgent; // récupérer l'user agent du navigateur
    if (ua.indexOf('MSIE ') > -1 || ua.indexOf('Trident/') > -1) // si windows explorer
        $scope.internet_explorer = true; // afficher l'avertissement
});
