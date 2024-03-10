/*=========================================================================================
  File Name: form-validation.js
  Description: jquery bootstrap validation js
  ----------------------------------------------------------------------------------------
==========================================================================================*/

$(function () {
  'use strict';

  var pageResetForm = $('.auth-register-form');

  // jQuery Validation
  // --------------------------------------------------------------------
  if (pageResetForm.length) {
    pageResetForm.validate({
      
      // To enable validation onkeyup
      // onkeyup: function (element) {
      //   $(element).valid();
      // },
      /*
      * ? To enable validation on focusout
      onfocusout: function (element) {
        $(element).valid();
      }, */
      rules: {
        'full_name': {
          required: true,
          minlength: 3
        },
        'email': {
          required: true,
          email: true
        },
        'password': {
          required: true,
          minlength: 8
        },
        'confirm_password':{
          required: true,
          equalTo: '#register-password'
        },
        'privacy_policy':{
          required: true
        }
      }
    });
  }
});
