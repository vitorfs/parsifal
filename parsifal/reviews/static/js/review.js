$(function () {
  var RETURN = 13;
  var ESC = 27;
  var is_editing = false;

  $.fn.addSettings = function () {
    $(this).blur(function () {
      var author = $(this).val();
      var parent = $(this).closest('li');
      $(this).remove();
      if (author == "") {
        parent.remove();
      }
      else {
        parent.html(author + ' <button type="button" class="remove-author">× remove</button>');
        $('.remove-author').unbind('click').bind('click', $.fn.bindRemoveButton);
      }
      is_editing = false;
    });

    $(this).keyup(function (evt) {
      var keyCode = evt.which?evt.which:evt.keyCode; 
      if (keyCode == RETURN || keyCode == ESC) {
        $(this).blur();
      }
    });
  };

  $.fn.bindRemoveButton = function () {
    $(this).closest('li').remove();
  };

  $('.add-author').click(function () {
    if (is_editing) {
      return false;
    }
    else {
      is_editing = true;
      $('.authors').append('<li><input type="text" class="input-author"></li>');
      $('.input-author').focus();
      $('.input-author').addSettings();
    }
  });

  $('.remove-author').click(function () {
    $(this).closest('li').remove();
  });
});