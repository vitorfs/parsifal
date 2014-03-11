function update_max_score() {
  var questions_count = $("#tbl-quality-questions tbody tr").length;
}

$(function () {

  //===========================================================================
  // QUALITY ASSESSMENT QUESTIONS 
  //===========================================================================

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
          $("#quality-question-description").focus();
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
    var quality_question_id = $(this).closest("tr").attr("oid");
    var review_id = $("#review-id").val();
    var row = $(this).closest("tr");
    
    $.ajax({
      url: '/reviews/planning/remove_quality_assessment_question/',
      data: {'review-id': review_id, 'quality-question-id': quality_question_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).remove();
      },
      error: function (jqXHR, textStatus, errorThrown) {

      }
    });

  });


  //===========================================================================
  // QUALITY ASSESSMENT ANSWERS
  //===========================================================================

  IS_ADDING_OR_EDITING_QUALITY_ANSWER = false;

  $("#btn-add-quality-answer").click(function () {
    if (!IS_ADDING_OR_EDITING_QUALITY_ANSWER) {
      
      IS_ADDING_OR_EDITING_QUALITY_ANSWER = true;

      var review_id = $("#review-id").val();

      $.ajax({
        url: '/reviews/planning/add_quality_assessment_answer/',
        data: {'review-id': review_id},
        type: 'get',
        cache: false,
        success: function (data) {
          $("#tbl-quality-answers tbody").prepend(data);
          $("#quality-answer-description").focus();
        }
      });

    }
  });

  $("table#tbl-quality-answers").on("click", "#btn-save-quality-answer", function () {
    var row = $(this).closest("tr");
    var review_id = $("#review-id").val();
    var description = $("#quality-answer-description").val();
    var weight = $("#quality-answer-weight").val();
    var quality_answer_id = $(row).attr("oid");
    var csrf_token = $(row).attr("csrf-token");

    $.ajax({
      url: '/reviews/planning/save_quality_assessment_answer/',
      data: {'review-id': review_id,
        'description': description,
        'weight': weight,
        'quality-answer-id': quality_answer_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      success: function (data) {
        if (quality_answer_id == 'None') {
          $(row).remove();
          $("#tbl-quality-answers tbody").prepend(data);
        }
        else {
          $("tr.quality-answer-hidden-for-edition").after(data);
          $("tr.quality-answer-hidden-for-edition").remove();
          $(row).remove();
        }
        IS_ADDING_OR_EDITING_QUALITY_ANSWER = false;
      }
    });
  });

  $("table#tbl-quality-answers").on("click", "#btn-cancel-quality-answer", function () {
    IS_ADDING_OR_EDITING_QUALITY_ANSWER = false;
    $(this).closest("tr").fadeOut(400, function () {
      $(this).remove();
      $("tr.quality-answer-hidden-for-edition").show();
      $("tr.quality-answer-hidden-for-edition").removeClass("quality-answer-hidden-for-edition");
    });
  });

  $("table#tbl-quality-answers").on("click", ".btn-edit-quality-answer", function () {
    if (!IS_ADDING_OR_EDITING_QUALITY_ANSWER) {

      IS_ADDING_OR_EDITING_QUALITY_ANSWER = true;

      var quality_answer_id = $(this).closest("tr").attr("oid");
      var review_id = $("#review-id").val();
      var row = $(this).closest("tr");

      $.ajax({
        url: '/reviews/planning/edit_quality_assessment_answer/',
        data: {'review-id': review_id, 'quality-answer-id': quality_answer_id},
        type: 'get',
        cache: false,
        success: function (data) {
          $(row).hide();
          $(row).after(data);
          $(row).addClass("quality-answer-hidden-for-edition");
        }
      });

    }    
  });

  $("table#tbl-quality-answers").on("click", ".btn-remove-quality-answer", function () {
    var quality_answer_id = $(this).closest("tr").attr("oid");
    var review_id = $("#review-id").val();
    var row = $(this).closest("tr");
    
    $.ajax({
      url: '/reviews/planning/remove_quality_assessment_answer/',
      data: {'review-id': review_id, 'quality-answer-id': quality_answer_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).remove();
      },
      error: function (jqXHR, textStatus, errorThrown) {

      }
    });
  });

  $("#add-suggested-answers").click(function () {
    alert('');
  });
  
});