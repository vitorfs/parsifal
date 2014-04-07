$(function () {
  $(".btn-save-picoc").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/reviews/planning/save_picoc/',
      data: $("#picoc-form").serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).disable();
      },
      success: function (data) {
        displayFormMessage(btn, "text-success", "Your review have been saved successfully!");
      },
      error: function () {
        displayFormMessage(btn, "text-error", "Something went wrong! Please contact the administrator.");
      },
      complete: function () {
        $(btn).enable();
      }
    });
  });
});