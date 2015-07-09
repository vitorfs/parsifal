$(function () {
  $(".btn-save-objective").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/reviews/planning/save_objective/',
      data: $('#form-objective').serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(btn).ajaxEnable();
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $(btn).ajaxEnableError();
        $.parsifal.alert("An error ocurred", jqXHR.responseText);
      }
    });
  });
});