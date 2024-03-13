/*=========================================================================================
	File Name: page-account-setting.js
	Description: Account setting.
	----------------------------------------------------------------------------------------
	
==========================================================================================*/

async function loadImage() {
  let accountUploadImg = document.getElementById("account-upload-img") , accountUploadBtn = document.getElementById("account-upload");
  
  if (accountUploadImg.src.includes("/media/uploads/user_placeholder.jpg")) 
  {
    console.log("image default")
    return
  }
  else if(!accountUploadImg.src.includes("/media/")){
    return 
  }
  
    // retirieve image blob by image path through server
  let images_paths = [accountUploadImg.src];
  let responses = await Promise.all(images_paths.map((e) => fetch(e)));
  console.log(images_paths);
  // console.log(responses)

  let files = new DataTransfer();
  await responses.forEach(function (response, index) {
    let blob_promise = response.blob();
    // console.log(blob_promise)
    blob_promise.then((blob) => {
      // console.log(blob)

      let path = images_paths[index];
      let filename = path.split("/")[path.split("/").length - 1];
      let extension = filename.split(".")[filename.split(".").length - 1];
      let name = filename.split(".")[0];

      let file = new File([blob], name + "." + extension, { type: blob.type });

      // console.log("Index "+ item_index + ":" + file.name)

      files.items.add(file);

      console.log(files)

      // console.log("Index "+ item_index + ":" + files.files.length)
    });
  });
  
  accountUploadBtn.files = files.files
}



$(function () {
  'use strict';

  loadImage()
  // variables
  var form = $('.validate-form'),
    flat_picker = $('.flatpickr'),
    accountUploadImg = $('#account-upload-img'),
    accountUploadBtn = $('#account-upload');
  

  // Update user photo on click of button
  if (accountUploadBtn) {
    accountUploadBtn.on('change', function (e) {
      if (e.target.files.length == 0){
        loadImage()
      }
      var reader = new FileReader(),
        files = e.target.files;
      reader.onload = function () {
        if (accountUploadImg) {
          accountUploadImg.attr('src', reader.result);
        }
      };
      reader.readAsDataURL(files[0]);
    });
  }

  // flatpickr init
  if (flat_picker.length) {
    flat_picker.flatpickr({
      onReady: function (selectedDates, dateStr, instance) {
        if (instance.isMobile) {
          $(instance.mobileInput).attr('step', null);
        }
      }
    });
  }

  // jQuery Validation
  // --------------------------------------------------------------------
  
  $("#bio_form").validate({
    rules: {
      full_name: {
        required: true,
        minlength: 3
      },
      email: {
        required: true,
        email: true
      },
      profile_image: {
        required: false,
      }
    }
  });
  // $("#bio_form").on('submit', function (e) {
  //   console.log($("#pass_form"))
  //   e.preventDefault();
  // })
  $("#pass_form").validate({
    rules: {
      'old_password': {
        required: true,
        minlength: 8
      },
      'new_password1': {
        required: true,
        minlength: 8
      },
      'password': {
        required: true,
        minlength: 8
      },
      'new_password2': {
        required: true,
        minlength: 8,
        equalTo: '#account-new-password'
      },
    },
    // messages: {},
    // errorElement : 'span',
  });
  // $("#pass_form").on('submit', function (e) {
  //   console.log($("#pass_form").errors)
  //   e.preventDefault();
  // })
});
