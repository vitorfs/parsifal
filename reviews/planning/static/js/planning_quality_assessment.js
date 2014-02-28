$(function () {

  IS_ADDING_OR_EDITING_QUALITY_QUESTION = false;

  $("#btn-add-quality-question").click(function () {
    if (!IS_ADDING_OR_EDITING_QUALITY_QUESTION) {
      var review_id = $("#review-id").val();
      IS_ADDING_OR_EDITING_QUALITY_QUESTION = true;
      $.ajax({
        url: '/reviews/planning/add_quality_assessment_question/',
        data: {'review-id': review_id},
        type: 'get',
        cache: false,
        success: function (data) {
          $("#tbl-quality-questions tbody").append(data);
        }
      });
    }
  });

  $("table#tbl-quality-questions").on("click", "#btn-cancel-quality_question", function () { 
    IS_ADDING_OR_EDITING_QUALITY_QUESTION = false;
    $(this).closest("tr").fadeOut(400, function () {
      $(this).remove();
      $("tr.quality-question-hidden-for-edition").show();
      $("tr.quality-question-hidden-for-edition").removeClass("quality-question-hidden-for-edition");
    });
  });

  $("table#tbl-quality-questions").on("click", "#btn-save-quality_question", function () { 
    var row = $(this).closest("tr");
    var review_id = $("#review-id").val();
    var description = $("#quality-question-description").val();
    var quality_question_id = $(row).attr("oid");
    var csrf_token = $(row).attr("csrf-token");

    $.ajax({
      url: '/reviews/planning/save_quality_assessment_question/',
      data: {'review-id': review_id,
        'description': description,
        'quality-question-id': quality_question_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $(row).fadeOut(400, function () {
          $(this).remove();
          $("#tbl-quality-questions tbody").prepend(data);
          IS_ADDING_OR_EDITING_QUALITY_QUESTION = false;
        });
      }
    });
  });

});