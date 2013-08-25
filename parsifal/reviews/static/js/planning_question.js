$(function () {
  function saveQuestion() {
    var btn = $(this);
    var form = $(this).closest("form");
    $.ajax({
      url: '/reviews/planning/save_question/',
      data: form.serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
      },
      error: function () {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-success").addClass("text-error");
        msg.text('Something went wrong! Please contact the administrator.');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      },
      success: function(data) {
        $("input[name='question-id']", form).val(data);
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-error").addClass("text-success");
        msg.text('Your question have been saved successfully!');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      },
      complete: function () {
      }
    });
  }

  function removeQuestion() {
    var btn = $(this);
    var form = $(this).closest("form");
    var question_id = $("input[name='question-id']", form).val();
    if (question_id != 'None') {
      $.ajax({
        url: '/reviews/planning/remove_question/',
        data: form.serialize(),
        type: 'post',
        cache: false,
        success: function (data) {
          $(form).closest("div.question").fadeOut();
        },
        error: function () {
        var msg = btn.siblings('.form-status-message');
          msg.removeClass("text-success").addClass("text-error");
          msg.text('Something went wrong! Please contact the administrator.');
          msg.fadeIn();
          window.setTimeout(function () {
            msg.fadeOut();
          }, 2000);
        }
      });
    }
    else {
      $(form).closest("div.question").fadeOut();
    }
  }

  $(".btn-save-question").click(saveQuestion);
  $(".btn-remove-question").click(removeQuestion);

  $("#btn-add-sec-question").click(function () {
    $.ajax({
      url: '/reviews/planning/add_question/',
      data: { 'review-id': $('#review-id').val() },
      type: 'get',
      cache: false,
      success: function (data) {
        $('.questions-containers').append(data);
        $('html, body').animate({
            scrollTop: ($(".questions-containers .question:last-child").offset().top - 20)
        }, 1000);
        $('.btn-save-question').unbind('click').bind('click', saveQuestion);
        $('.btn-remove-question').unbind('click').bind('click', removeQuestion);
      }
    });
  });
});