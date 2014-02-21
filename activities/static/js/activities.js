$(function () {

  $(".user-actions button").click(function() {
    var btn = $(this);
    var user_actions = $(this).closest(".user-actions");
    var user_id = $(user_actions).attr("data-user-id");
    if ($(user_actions).hasClass("following")) {
      $.ajax({
        url: '/activity/unfollow/',
        data: {'user-id': user_id},
        type: 'get',
        cache: false,
        success: function (data) {
          $(user_actions).removeClass("following");
          $(user_actions).addClass("not-following");
          $(btn).removeClass("btn-warning");
          $(btn).addClass("btn-success");
          $(btn).text("Follow");
        },
        error: function (jqXHR, textStatus, errorThrown) {
          
        }
      });
    }
    else {
      $.ajax({
        url: '/activity/follow/',
        data: {'user-id': user_id},
        type: 'get',
        cache: false,
        success: function (data) {
          $(user_actions).removeClass("not-following");
          $(user_actions).addClass("following");
          $(btn).removeClass("btn-success");
          $(btn).addClass("btn-warning")
          $(btn).text("Unfollow");
        },
        error: function (jqXHR, textStatus, errorThrown) {
          
        }
      });
    }
  });

});