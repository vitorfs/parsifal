$(function () {
  $(".btn-save-objective").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/reviews/planning/save_objective/',
      data: $('#form-objective').serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-error").addClass("text-success");
        msg.text('Your review have been saved successfully!');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      }
    });
  });
});