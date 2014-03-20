$(function () {

  function save_data_extraction_field() {

  }

  $(".tbl-data-extraction input[type=text]").blur(function () {
    var article_id = $(this).closest(".tbl-data-extraction").attr("article-id");
    var field_id = $(this).closest("tr").attr("field-id");
    var value = $(this).val();
    console.log(article_id + ' ' + field_id + ' ' + value);
  });

  $(".tbl-data-extraction select").change(function () {
    var article_id = $(this).closest(".tbl-data-extraction").attr("article-id");
    var field_id = $(this).closest("tr").attr("field-id");
    var value = $(this).val();
    console.log(article_id + ' ' + field_id + ' ' + value);
  });

  $(".tbl-data-extraction input[type=checkbox]").click(function () {
    var article_id = $(this).closest(".tbl-data-extraction").attr("article-id");
    var field_id = $(this).closest("tr").attr("field-id");
    var value = $(this).val();
    console.log(article_id + ' ' + field_id + ' ' + value);
  });

});