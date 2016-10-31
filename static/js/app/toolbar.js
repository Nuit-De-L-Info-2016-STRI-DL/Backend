angular.module('toolbar', []);

angular.module('toolbar').component('toolbar',
{
    templateUrl: '/static/html/toolbar.tmpl.html',
    controller: ['$http', '$cacheFactory', '$templateCache', '$window', '$mdDialog',
        function controller($http, $cacheFactory, $templateCache, $window, $mdDialog) {
            var self = this;
            //----------------------------------------------------------------------
            //
            self.show_settings = function() {
                // open dialog
                $mdDialog.show({
                    templateUrl: '/static/html/settingsDialog.tmpl.html',
                    locals: {parent: self},
                    bindToController: true,
                    fullscreen: true,
                    clickOutsideToClose: true,
                    escapeToClose: true,
                    parent: angular.element(document.body),
                    controller: ['$scope', '$mdDialog', '$http',
                        function controller ($scope, $mdDialog, $http) {
                            $scope.closeDialog = function() {
                                $mdDialog.hide();
                            };
                            //
                            $scope.list_apis = [];
                            $scope.selected_ignored_api = [];
                            $scope.new_ignored_api = undefined;
                            //
                            $scope.refresh_daemons_status = function() {
                                $scope.daemons = undefined;
                                $scope.err = undefined;
                                $http.get('/api/status').then(function (response) { // on success
                                    $scope.daemons = response.data;
                                }, function (response) { // on error
                                    $scope.err = "Erreur lors de la récupération des status des Daemons";
                                    console.log(response);
                                });
                            };
                            $scope.do_daemon_change = function(daemon_name, change_name) {
                                $scope.daemons = undefined;
                                $scope.err = undefined;
                                $http({
                                    method: 'POST',
                                    url: '/api/daemon-control',
                                    params: {
                                        'name': daemon_name,
                                        'action': change_name
                                    }
                                }).then(function (response) { // on success
                                    $scope.refresh_daemons_status();
                                }, function (response) { // on error
                                    $scope.err = "Erreur lors d'une action sur un Daemon";
                                    console.log(response);
                                    $scope.refresh_daemons_status();
                                });
                            };
                            //
                            $scope.uploadedFile = function(input) {  // TODO
                                $scope.$apply(function($scope) {
                                    var file2upload = input.files[0];
                                    var fd = new FormData();
                                    fd.append("file", file2upload);
                                    $http.post('/data/import.zip', fd, {
                                        withCredentials: false,
                                        headers: {'Content-Type': undefined }, // reset it
                                        transformRequest: angular.identity // it'll be automatically set to the good one here
                                    }).then(function() { // on success
                                        console.log("POST /data/import.zip", response.data);
                                    }, function(data, status, header, config) { // on error
                                        $scope.showErrToast("Erreur lors de l'import d'un zip");
                                        console.log(data);
                                    });
                                });
                            };
                            //
                            $scope.refresh_daemons_status();
                        }
                    ]
                });
            };
            //----------------------------------------------------------------------
            // open popup
            $mdDialog.show({
                templateUrl: '/static/html/avert.tmpl.html',
                fullscreen: true,
                clickOutsideToClose: true,
                escapeToClose: true,
                locals: {parent: self},
                bindToController: true,
                parent: angular.element(document.body),
                controller: ['$scope', '$mdDialog',
                    function controller ($scope, $mdDialog) {
                        $scope.closeDialog = function() {
                            $mdDialog.hide();
                        };
                    }
                ]
            });

            self.refresh_page = function() {
                $cacheFactory.get('$http').removeAll(); // vider le cache
                $templateCache.removeAll(); // vider le cache du navigateur
                $window.location.reload(); // reload page
            };
        }
    ]
});
