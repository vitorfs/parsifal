function update_max_score() {
  $.ajax({
    url: '/reviews/planning/calculate_max_score/',
    data: {'review-id': $('#review-id').val()},
    type: 'get',
    cache: false,
    success: function (data) {
      $("#max-score").val(data);
    },
    error: function () {
      $("#max-score").val("0.0");
    }
  });
}

$(function () {

  //===========================================================================
  // QUALITY ASSESSMENT QUESTIONS 
  //===========================================================================
  
  var cancel_question_edition_row = new Array();

  $("#btn-add-quality-question").click(function () {
    var review_id = $("#review-id").val();
    $.ajax({
      url: '/reviews/planning/add_quality_assessment_question/',
      data: {'review-id': review_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $("#tbl-quality-questions tbody").prepend(data);
        $("#tbl-quality-questions tbody tr:first-child .quality-question-description").focus();
      }
    });
  });

  $("table#tbl-quality-questions").on("click", ".btn-cancel-quality_question", function () { 
    var row = $(this).closest("tr");
    var quality_question_id = $(row).attr("oid");
    if (quality_question_id == 'None') {
      $(row).fadeOut(400, function () {
        $(this).remove();
      });
    }
    else {
      $(row).replaceWith(cancel_question_edition_row[quality_question_id]);
    }
  });

  $("table#tbl-quality-questions").on("click", ".btn-save-quality_question", function () { 
    var row = $(this).closest("tr");
    var review_id = $("#review-id").val();
    var description = $(".quality-question-description", row).val();
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
        $(row).replaceWith(data);
        update_max_score();
      }
    });
  });

  $("table#tbl-quality-questions").on("click", ".btn-edit-quality-question", function () { 
    var row = $(this).closest("tr");
    var quality_question_id = $(row).attr("oid");
    var review_id = $("#review-id").val();

    cancel_question_edition_row[quality_question_id] = row;

    $.ajax({
      url: '/reviews/planning/edit_quality_assessment_question/',
      data: {'review-id': review_id, 'quality-question-id': quality_question_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).replaceWith(data);
      }
    });
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
        update_max_score();
      },
      error: function (jqXHR, textStatus, errorThrown) {

      }
    });

  });


  //===========================================================================
  // QUALITY ASSESSMENT ANSWERS
  //===========================================================================

  var cancel_answer_edition_row = new Array();

  $("#btn-add-quality-answer").click(function () {
    var review_id = $("#review-id").val();
    $.ajax({
      url: '/reviews/planning/add_quality_assessment_answer/',
      data: {'review-id': review_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $("#tbl-quality-answers tbody").prepend(data);
        $("#tbl-quality-answers tbody tr:first-child .quality-answer-description").focus();
      }
    });
  });

  $("table#tbl-quality-answers").on("click", ".btn-save-quality-answer", function () {
    var row = $(this).closest("tr");
    var review_id = $("#review-id").val();
    var description = $(".quality-answer-description", row).val();
    var weight = $(".quality-answer-weight", row).val();
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
        $(row).replaceWith(data);
        update_max_score();
      }
    });
  });

  $("table#tbl-quality-answers").on("click", ".btn-cancel-quality-answer", function () {
    var row = $(this).closest("tr");
    var quality_answer_id = $(row).attr("oid");
    if (quality_answer_id == 'None') {
      $(row).fadeOut(400, function () {
        $(this).remove();
      });
    }
    else {
      $(row).replaceWith(cancel_answer_edition_row[quality_answer_id]);
    }
  });

  $("table#tbl-quality-answers").on("click", ".btn-edit-quality-answer", function () {
    var row = $(this).closest("tr");
    var quality_answer_id = $(row).attr("oid");
    var review_id = $("#review-id").val();
    cancel_answer_edition_row[quality_answer_id] = row;

    $.ajax({
      url: '/reviews/planning/edit_quality_assessment_answer/',
      data: {'review-id': review_id, 'quality-answer-id': quality_answer_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).replaceWith(data);
      }
    });
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
        update_max_score();
      },
      error: function (jqXHR, textStatus, errorThrown) {

      }
    });
  });

  $("#add-suggested-answers").click(function () {
    $.ajax({
      url: '/reviews/planning/add_suggested_answer/',
      data: {'review-id': $("#review-id").val()},
      type: 'get',
      cache: false,
      success: function (data) {
        $("#tbl-quality-answers tbody").replaceWith("<tbody>" + data + "</tbody>");
        $(".no-answers").fadeOut();
      }
    });
  });

  $("#save-cutoff-score").click(function () {
    var btn = $(this);
    var review_id = $("#review-id").val();
    var cutoff_score = $("#cutoff-score").val();

    $.ajax({
      url: '/reviews/planning/save_cutoff_score/',
      data: {'review-id': review_id, 'cutoff-score': cutoff_score},
      type: 'get',
      cache: false,
      success: function (data) {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-error").addClass("text-success");
        msg.text(data);
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-success").addClass("text-error");
        msg.text(jqXHR.responseText);
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      }
    });

  });
  
});