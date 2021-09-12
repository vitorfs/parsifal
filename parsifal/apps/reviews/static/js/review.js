$(function () {

  $(".js-leave").click(function () {
    $(this).closest("form").submit();
  });

  $(".js-remove-author").click(function () {

    var user_container = $(this).closest("li");

    var csrf_token = $("[name='csrfmiddlewaretoken']").val();
    var user_id = $(this).closest("li").attr("data-user-id");
    var review_id = $("#review-id").val();
    var url = $(this).closest("ul").attr("data-remove-url");

    $.post(url, {
      'csrfmiddlewaretoken': csrf_token,
      'user-id': user_id,
      'review-id': review_id
    }, function () {
      $(user_container).fadeOut(400, function () {
        $(this).remove();
      });
    });

  });

});
