$(function () {
  $(".btn-import-bibtex").click(function () {
    var container = $(this).closest("td");
    $("input[type=file]", container).click();
  });


  $("input[name='bibtex']").change(function () {
    var form = $(this).closest("form");
    $(form).submit();
  });

  $(".js-import-bibtex-raw-content").click(function () {
    var source_id = $(this).attr("data-source-id");
    $("#bibtex-raw-content-source-id").val(source_id);
  });

  $("#parse-bibtex").on("shown.bs.modal", function () {
    $("#bibtex_raw_content").focus();
  });
});