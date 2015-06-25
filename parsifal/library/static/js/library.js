$(function () {

  $(".js-jump-page").popover({
    html: true,
    content: function () {
      var html = "<div><small><a href='?page=1'>First page</a></small></div>";
      html += "<div><small><a href='?page={{ documents.paginator.num_pages }}'>Last page</a></small></div>";
      return html;
    }
  });

  $(".js-document-checkbox").click(function () {
    var row = $(this).closest("tr");
    var checkbox = $("input[type='checkbox']", this);
    var icon = $(".glyphicon", this);
    var isChecked = $(checkbox).is(":checked");

    if (isChecked) {
      $(checkbox).prop("checked", false);
      $(icon).removeClass().addClass("glyphicon glyphicon-unchecked");
      $(row).removeClass("bg-warning");
    }
    else {
      $(checkbox).prop("checked", true);
      $(icon).removeClass().addClass("glyphicon glyphicon-check");
      $(row).addClass("bg-warning");
    }

  });

});
