var FORWARD = 1;
var BACKWARD = -1;
var UP_ARROW_KEY = 38;
var DOWN_ARROW_KEY = 40;
var ENTER_KEY = 13;
var ESCAPE_KEY = 27;
var LOADING = "<table class='loading'><tr><td><img src='/static/img/loading.gif'></td></tr></table>";

// Form functions

function displayFormMessage(ref, type, message) {
  var msg = ref.siblings('.form-status-message');
  if (type == "text-success") {
    msg.removeClass("text-error").addClass("text-success");
  }
  else {
    msg.removeClass("text-success").addClass("text-error");
  }
  msg.text(message);
  msg.fadeIn();
  window.setTimeout(function () {
    msg.fadeOut();
  }, 2000);
}

// Modal functions 

$.fn.open = function () {
  $(this).before("<div class='shade'></div>");
  $(this).slideDown(400, function () {
    $("body").addClass("modal-open");
  });
};

$.fn.close = function () {
  $(this).slideUp(400, function () {
    $(".shade").remove();
    $("body").removeClass("modal-open");
  });
};

// Loading functions

$.fn.loading = function () {
  $(this).addClass("loading-state");
  $(this).html(LOADING);
};

$.fn.stopLoading = function () {
  $(this).removeClass("loading-state");
};

// Button functions

$.fn.disable = function () {
  $(this).prop("disabled", true);
  $(this).attr("data-original", $(this).text());
  $(this).text($(this).attr("data-loading"));
};

$.fn.enable = function () {
  $(this).prop("disabled", false);
  $(this).text($(this).attr("data-original"));
};

// On page load

$(function () {
  $(".modal").on("click", ".close-modal", function () {
    var modal = $(this).closest(".modal");
    $(modal).close();
    return false;
  });
});