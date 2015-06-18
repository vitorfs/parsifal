(function($) {

  'use strict';

  /* Parsifal base scripts */

  $.parsifal = {

    /* General application initialization */

    init: function () {
      $("[data-toggle='tooltip']").tooltip();

      $.fn.disable = function () {
        $(this).prop("disabled", true);
        $(this).attr("data-original", $(this).text());
        $(this).text($(this).attr("data-loading"));
      };

      $.fn.enable = function () {
        $(this).prop("disabled", false);
        $(this).text($(this).attr("data-original"));
      };

      $.fn.spinner = function (alignCenter) {
        alignCenter = typeof alignCenter !== 'undefined' ? alignCenter : true;
        if ($(this).hasClass("loading")) {
          $(this).find(".block-spinner").remove();
          $(this).removeClass("loading");
        }
        else {
          if (alignCenter) {
            var center = (parseInt($(this).css("height")) / 2) - 40;
          }
          else {
            var center = 0;
          }
          $(this).addClass("loading");
          $(this).html("<div class='block-spinner' style='margin-top: " + center + "px;'></div>");
        }
      };
      
    },

    /* Apps */

    activities: function () {

    },

    /* Helper functions */

    pageLoading: function () {
      if ($("body").hasClass("no-scroll")) {
        $("body").removeClass("no-scroll");
      }
      else {
        $("body").addClass("no-scroll");
      }
      $(".page-loading").toggle();
    }
  };

})(jQuery);

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

var FORWARD = 1;
var BACKWARD = -1;
var UP_ARROW_KEY = 38;
var DOWN_ARROW_KEY = 40;
var ENTER_KEY = 13;
var ESCAPE_KEY = 27;
var LOADING = "<table class='loading'><tr><td><img src='/static/img/loading.gif'></td></tr></table>";

// Loading functions

$.fn.loading = function () {
  $(this).addClass("loading-state");
  $(this).html(LOADING);
};

$.fn.stopLoading = function () {
  $(this).removeClass("loading-state");
};