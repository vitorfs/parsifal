$(function () {

  function save_data_extraction_field(ref) {
    var review_id = $("#review-id").val();
    var article_id = $(ref).closest(".tbl-data-extraction").attr("article-id");
    var field_id = $(ref).closest("tr").attr("field-id");
    var value = $(ref).val();
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: '/reviews/conducting/save_data_extraction/',
      data: {
        'review-id': review_id,
        'article-id': article_id,
        'field-id': field_id,
        'value': value,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      success: function (data) {

      }
    });
  }

  $(".tbl-data-extraction input[type=text]").blur(function () {
    save_data_extraction_field($(this));
  });

  $(".tbl-data-extraction select").change(function () {
    save_data_extraction_field($(this));
  });

  $(".tbl-data-extraction input[type=checkbox]").click(function () {
    save_data_extraction_field($(this));
  });

});