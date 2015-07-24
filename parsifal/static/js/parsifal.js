(function($) {

  'use strict';

  /* Parsifal base scripts */

  $.parsifal = {

    /* General application initialization */

    init: function () {

      $("[data-toggle='tooltip']").tooltip();

      $("table.table-check-all thead tr th input[type='checkbox']").click(function () {
        var is_checked = $(this).is(":checked");
        var table = $(this).closest("table");
        if (is_checked) {
          $("tbody tr td input[type='checkbox']", table).prop("checked", true);
        }
        else {
          $("tbody tr td input[type='checkbox']", table).prop("checked", false);
        }
      });

      $("table.table-check-all").on("click", "input[type='checkbox']", function () {
        var table = $(this).closest("table");
        var all_checked_flag = true;
        var checked_count = 0;
        $("tbody tr td input[type='checkbox']", table).each(function () {
          if ($(this).is(":checked")) {
            checked_count = checked_count + 1;
          }
          else {
            all_checked_flag = false;
          }
        });
        $("thead tr th input[type='checkbox']", table).prop("checked", all_checked_flag);
      });

      $.fn.disable = function () {
        $(this).prop("disabled", true);
        $(this).attr("data-original", $(this).text());
        $(this).text($(this).attr("data-loading"));
      };

      $.fn.enable = function () {
        $(this).prop("disabled", false);
        $(this).text($(this).attr("data-original"));
      };

      $.fn.ajaxDisable = function () {
        $(this).prop("disabled", true);
        $("span[class^='btn-ajax-']", this).hide();
        $("span.btn-ajax-loading", this).show();
      };

      $.fn.ajaxEnable = function (callback) {
        callback = callback || function () {};
        
        var btn = $(this);
        $(this).prop("disabled", false);
        $("span[class^='btn-ajax-']", this).hide();

        var hasCompleteState = $("span.btn-ajax-complete", this).length > 0;

        if (hasCompleteState) {
          $("span.btn-ajax-complete", this).show();
          setTimeout(function () {
            $("span[class^='btn-ajax-']", btn).hide();
            $("span.btn-ajax-normal", btn).show();
            callback();
          }, 1500);
        }
        else {
          $("span.btn-ajax-normal", btn).show();
          callback();
        }

      };

      $.fn.ajaxEnableError = function (callback) {
        callback = callback || function () {};
        
        var btn = $(this);
        $(this).prop("disabled", false);
        $("span[class^='btn-ajax-']", this).hide();

        var hasErrorState = $("span.btn-ajax-error", this).length > 0;

        if (hasErrorState) {
          $("span.btn-ajax-error", this).show();
          setTimeout(function () {
            $("span[class^='btn-ajax-']", btn).hide();
            $("span.btn-ajax-normal", btn).show();
            callback();
          }, 1500);
        }
        else {
          $("span.btn-ajax-normal", btn).show();
          callback();
        }

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

      $.fn.updateFormsetIndex = function () {
        var tableRows = $("table tbody tr", this);
        var totalForms = $(tableRows).length;
        $("[id$='TOTAL_FORMS']", this).val(totalForms);

        $(tableRows).each(function () {
          var rowIndex = $(this).index();
          $("td input", this).each(function () {
            var name = $(this).attr("name");
            $(this).attr("name", name.replace(/-(.*?)-/, "-" + rowIndex + "-"));
            var id = $(this).attr("id");
            $(this).attr("id", id.replace(/-(.*?)-/, "-" + rowIndex + "-"));
          });
        });

      };
      
    },

    uuid: function () {
      var _uuid ='xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
          var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
          return v.toString(16);
      });
      return _uuid;
    },

    alert: function (title, message) {
      $("#modal-alert .modal-title").text(title);
      $("#modal-alert .modal-body").text(message);
      $("#modal-alert").modal("show");
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
var TAB_KEY = 9;
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