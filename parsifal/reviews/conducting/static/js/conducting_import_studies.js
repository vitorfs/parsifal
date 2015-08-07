$(function () {
  $(".btn-import-bibtex").click(function () {
    var container = $(this).closest("td");
    $("input[type=file]", container).click();
  });


  $("input[name='bibtex']").change(function () {
    var form = $(this).closest("form");
    $(form).submit();
  });
});