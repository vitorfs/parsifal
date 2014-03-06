$(function () {

  $("#conducting-tab a").click(function () {
    var tab_url = $(this).attr("href");

    $("#conducting-tab li").removeClass("active");
    $(this).closest("li").addClass("active");

    $.ajax({
      url: tab_url,
      data: {'review-id': $("#review-id").val()},
      cache: false,
      type: 'get',
      beforeSend: function () {
        $("#tab-contents").loading();
      },
      success: function (data) {
        $("#tab-contents").html(data);
      },
      complete: function() {
        $("#tab-contents").stopLoading();
      }
    });

    return false;
  });

});