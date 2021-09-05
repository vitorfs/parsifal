$(function () {
  $(".btn-save-picoc").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/reviews/planning/save_picoc/',
      data: $("#picoc-form").serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(btn).ajaxEnable();
      },
      error: function () {
        $(btn).ajaxEnableError();
        $.parsifal.alert("An error ocurred", "Something went wrong! Please contact the administrator.");
      }
    });
  });
});