$(function () {

  function saveQuestion() {
    var btn = $(this);
    var form = $(this).closest("form");
    $.ajax({
      url: '/reviews/planning/save_question/',
      data: form.serialize(),
      type: 'post',
      cache: false,
      error: function (jqXHR, textStatus, errorThrown) {
        displayFormMessage(btn, "text-error", jqXHR.responseText);
      },
      success: function(data) {
        $("input[name='question-id']", form).val(data);
        displayFormMessage(btn, "text-success", "Your question has been saved successfully!");
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
          displayFormMessage(btn, "text-error", "Something went wrong! Please contact the administrator.");
        }
      });
    }
    else {
      $(form).closest("div.question").fadeOut();
    }
  }

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
      }
    });
  });

  $("div.questions-containers").on("click", ".btn-save-question", saveQuestion);
  $("div.questions-containers").on("click", ".btn-remove-question", removeQuestion);
});