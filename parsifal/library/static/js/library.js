$(function () {

  'use strict';

  $(".js-jump-page").popover({
    html: true,
    content: function () {
      var last_page = $("#library-documents").attr("data-num-pages");
      var html = "<div><small><a href='?page=1'>First page</a></small></div>";
      html += "<div><small><a href='?page=" + last_page + "'>Last page</a></small></div>";
      return html;
    }
  });

  $(".js-toggle-select-documents").click(function () {
    var isChecked = $(".glyphicon", this).hasClass("glyphicon-check");
    var btnSelectAll = $(this);
    if (isChecked) {
      $("#library-documents .js-document-checkbox").each(function () {
        $(this).unselectDocument();
      });
      $(".glyphicon", btnSelectAll).removeClass().addClass("glyphicon glyphicon-unchecked");
    }
    else {
      $("#library-documents .js-document-checkbox").each(function () {
        $(this).selectDocument();
      });
      $(".glyphicon", btnSelectAll).removeClass().addClass("glyphicon glyphicon-check");
    }
  });

  $.fn.selectDocument = function () {
    var row = $(this).closest("tr");
    var checkbox = $("input[type='checkbox']", this);
    var icon = $(".glyphicon", this);

    $(checkbox).prop("checked", true);
    $(icon).removeClass().addClass("glyphicon glyphicon-check");
    $(row).addClass("bg-warning");
  };

  $.fn.unselectDocument = function () {
    var row = $(this).closest("tr");
    var checkbox = $("input[type='checkbox']", this);
    var icon = $(".glyphicon", this);

    $(checkbox).prop("checked", false);
    $(icon).removeClass().addClass("glyphicon glyphicon-unchecked");
    $(row).removeClass("bg-warning");
  };

  $(".js-document-checkbox").click(function () {
    var row = $(this).closest("tr");
    var checkbox = $("input[type='checkbox']", this);
    var icon = $(".glyphicon", this);
    var isChecked = $(checkbox).is(":checked");

    if (isChecked) {
      $(this).unselectDocument();
    }
    else {
      $(this).selectDocument();
    }

  });

});
