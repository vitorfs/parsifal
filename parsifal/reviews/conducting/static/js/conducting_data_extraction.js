$(function () {

  function save_data_extraction_field(ref) {
    var row = $(ref).closest(".form-group");
    var review_id = $("#review-id").val();
    var article_id = $(ref).closest(".panel-body").attr("data-article-id");
    var field_id = $(row).attr("data-field-id");
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
        $("span.error", row).text('');
        $("span.error", row).hide();
        $(row).removeClass("has-error");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $("span.error", row).text(jqXHR.responseText);
        $("span.error", row).show();
        $(row).addClass("has-error");
      }
    });
  }

  $(".data-extraction-panel input[type=text]").change(function () {
    save_data_extraction_field($(this));
  });

  $(".data-extraction-panel select").change(function () {
    save_data_extraction_field($(this));
  });

  $(".data-extraction-panel input[type=checkbox]").click(function () {
    save_data_extraction_field($(this));
  });

});