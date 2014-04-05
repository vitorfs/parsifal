$(function () {

  $(".btn-suggested-search-string").click(function () {
    var form = $(this).closest("form");
    $.ajax({
      url: '/reviews/planning/generate_search_string/',
      data: { 'review-id': $("#review-id").val() },
      cache: false,
      type: 'get',
      success: function (data) {
        $(".search-string", form).val(data);
      }
    });
  });

  $(".btn-save-generic-search-string").click(function () {
    var btn = $(this);
    var form = $(this).closest("form");
    var search_string = $(".search-string", form).val();
    $.ajax({
      url: '/reviews/planning/save_generic_search_string/',
      data: $(form).serialize(),
      cache: false,
      type: 'post',
      success: function (data) {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-error").addClass("text-success");
        msg.text('Your search string have been saved successfully!');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
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
  });

});