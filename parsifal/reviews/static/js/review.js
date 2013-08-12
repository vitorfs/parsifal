$(function () {
  var RETURN = 13;
  var ESC = 27;
  var is_editing = false;

  $.fn.addSettings = function () {
    $(this).blur(function () {
      var author = $(this).val();
      var parent = $(this).closest('li');
      var id = $('#review-id').val();
      $(this).remove();
      if (author == "") {
        parent.remove();
      }
      else {
        $.ajax({
            url: '/reviews/addauthor/',
            data: { id: id, username: author },
            type: 'get',
            cache: false,
            success: function (data) {
              parent.html(data + ' <button type="button" class="remove-author">(remove)</button>');
              $('.remove-author').unbind('click').bind('click', $.fn.bindRemoveButton);
            },
            complete: function () {
              is_editing = false;
            }
        });
      }
    });

    $(this).keyup(function (evt) {
      var keyCode = evt.which?evt.which:evt.keyCode; 
      if (keyCode == RETURN) {
        $(this).blur();
      }
      else if (keyCode == ESC) {
        $(this).closest('li').remove();
        is_editing = false;
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
      $('.authors').append('<li class="add-author-input"><input type="text" class="input-author"> <span>(please inform the author\'s username or email and then press <strong>Enter</strong> to confirm or <strong>Esc</strong> to cancel)</span></li>');
      $('.input-author').focus();
      $('.input-author').addSettings();
    }
  });

  $('.remove-author').click(function () {
    $(this).closest('li').remove();
  });
});