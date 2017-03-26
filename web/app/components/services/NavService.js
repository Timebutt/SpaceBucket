(function(){
  'use strict';

  angular.module('app')
          .service('navService', [
          '$q',
          navService
  ]);

  function navService($q){
    var menuItems = [
      {
        name: 'Dashboard',
        icon: 'dashboard',
        sref: '.dashboard'
      },
      {
        name: 'Lighting',
        icon: 'brightness_5',
        sref: '.profile'
      },
      {
          name: 'Log',
          icon: 'event_note',
          sref: '.log'
      },
      {
        name: 'Settings',
        icon: 'settings',
        sref: '.configuration'
      }
    ];

    return {
      loadAllItems : function() {
        return $q.when(menuItems);
      }
    };
  }

})();
