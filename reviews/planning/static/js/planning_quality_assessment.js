$(function () {

  IS_ADDING_OR_EDITING_QUALITY_QUESTION = false;

  $("#btn-add-quality-question").click(function () {
    if (!IS_ADDING_OR_EDITING_QUALITY_QUESTION) {
      
      IS_ADDING_OR_EDITING_QUALITY_QUESTION = true;

      var review_id = $("#review-id").val();

      $.ajax({
        url: '/reviews/planning/add_quality_assessment_question/',
        data: {'review-id': review_id},
        type: 'get',
        cache: false,
        success: function (data) {
          $("#tbl-quality-questions tbody").prepend(data);
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
        // It's a new question so it will be prepended on the table
        if (quality_question_id == 'None') {
          $(row).remove();
          $("#tbl-quality-questions tbody").prepend(data);
        }
        // Saving an existing question, so it will have to appear on the same position as before
        else {
          $("tr.quality-question-hidden-for-edition").after(data);
          $("tr.quality-question-hidden-for-edition").remove();
          $(row).remove();
        }
        IS_ADDING_OR_EDITING_QUALITY_QUESTION = false;
      }
    });
  });

  $("table#tbl-quality-questions").on("click", ".btn-edit-quality-question", function () { 
    if (!IS_ADDING_OR_EDITING_QUALITY_QUESTION) {

      IS_ADDING_OR_EDITING_QUALITY_QUESTION = true;

      var quality_question_id = $(this).closest("tr").attr("oid");
      var review_id = $("#review-id").val();
      var row = $(this).closest("tr");

      $.ajax({
        url: '/reviews/planning/edit_quality_assessment_question/',
        data: {'review-id': review_id, 'quality-question-id': quality_question_id},
        type: 'get',
        cache: false,
        success: function (data) {
          $(row).hide();
          $(row).after(data);
          $(row).addClass("quality-question-hidden-for-edition");
        }
      });

    }

  });

  $("table#tbl-quality-questions").on("click", ".btn-remove-quality-question", function () { 
    
  });

});