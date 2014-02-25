$(function () {
  var is_editing = false;

  $.fn.addSettings = function () {
    $(this).blur(function () {
      var author = $(this).val();
      var parent = $(this).closest('li');
      var id = $('#review-id').val();
      if (author == "") {
        parent.remove();
        is_editing = false;
      }
      else {
        $.ajax({
            url: '/reviews/add_author/',
            data: { 'review-id': id, 'username': author },
            type: 'get',
            cache: false,
            success: function (data) {
              parent.remove();
              $('.authors').append(data);
            },
            error: function () {
              parent.remove();
            },
            complete: function () {
              is_editing = false;
            }
        });
      }
    });

    $(this).keyup(function (evt) {
      var keyCode = evt.which?evt.which:evt.keyCode;
      if (keyCode == ENTER_KEY) {
        $(this).blur();
      }
      else if (keyCode == ESCAPE_KEY) {
        $(this).closest('li').remove();
        is_editing = false;
      }
    });
  };

  var removeAuthor = function () {
    var review_id = $('#review-id').val();
    var parent = $(this).closest('li');
    var author_id = parent.attr("author-id");
    $.ajax({
      url: '/reviews/remove_author/',
      data: { 'review-id': review_id, 'author-id': author_id },
      type: 'get',
      cache: false,
      success: function (data) {
        parent.remove();
      }
    });
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

  $("#btn-save-description").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/reviews/save_description/',
      data: $("#form-description").serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-error").addClass("text-success");
        msg.text(data);
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-success").addClass("text-error");
        msg.text(jqXHR.responseText);
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      }
    });
  });

  $("ul.authors").on("click", ".remove-author", removeAuthor);

});