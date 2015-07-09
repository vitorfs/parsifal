$(function () {

  var cancel_research_question_edition_row = new Array();

  $("#btn-add-question").click(function () {
    var review_id = $("#review-id").val();
    var csrf_token = $("#question-form input[name='csrfmiddlewaretoken']").val();
    $.ajax({
      url: '/reviews/planning/add_or_edit_question/',
      data: {
        'review-id': review_id,
        'question-id': 'None',
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $("#question-form table tbody").append(data);
        $("#question-form table tbody input[type='text']").last().focus();
      }
    });
  });

  $("#question-form").on("click", ".btn-cancel-question", function () {
    var tr = $(this).closest("tr");
    var question_id = $(tr).attr("data-question-id");
    if (question_id == 'None') {
      $(tr).remove();
    }
    else {
      $(tr).replaceWith(cancel_research_question_edition_row[question_id]);
    }
  });

  $("#question-form").on("click", ".btn-edit-question", function () {
    var tr = $(this).closest("tr");
    var btn = $(this);
    var review_id = $("#review-id").val();
    var question_id = $(tr).attr("data-question-id");
    var csrf_token = $("#question-form input[name='csrfmiddlewaretoken']").val();

    cancel_research_question_edition_row[question_id] = tr;

    $.ajax({
      url: '/reviews/planning/add_or_edit_question/',
      data: {
        'review-id': review_id,
        'question-id': question_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function(data) {
        var newRow = $(tr).replaceWith(data);
        var input = $("tr[data-question-id='" + question_id + "'] input[type='text']");
        $(input).focus();
        /* This trick is done to put the cursor in the end of the input value */
        var tmpVal = $(input).val();
        $(input).val("");
        $(input).val(tmpVal);
      },
      complete: function () {
        $(btn).ajaxEnable();
      }
    });
  });

  $("#question-form").on("click", ".btn-save-question", function () {
    var tr = $(this).closest("tr");
    var btn = $(this);
    var review_id = $("#review-id").val();
    var question_id = $(tr).attr("data-question-id");
    var description = $("input[name='question-description']", tr).val();
    var csrf_token = $("#question-form input[name='csrfmiddlewaretoken']").val();
    $.ajax({
      url: '/reviews/planning/save_question/',
      data: {
        'review-id': review_id,
        'question-id': question_id,
        'description': description,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function(data) {
        $(tr).replaceWith(data);
        manageQuestionsOrder();
      },
      error: function (jqXHR, textStatus, errorThrown) {
        
      },
      complete: function () {
        $(btn).ajaxEnable();
      }
    });
  });

  $("#question-form").on("click", ".btn-remove-question", function () {
    var tr = $(this).closest("tr");
    var btn = $(this);
    var review_id = $("#review-id").val();
    var question_id = $(tr).attr("data-question-id");
    var csrf_token = $("#question-form input[name='csrfmiddlewaretoken']").val();
    $.ajax({
      url: '/reviews/planning/remove_question/',
      data: {
        'review-id': review_id,
        'question-id': question_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(tr).remove();
      },
      error: function () {
        
      },
      complete: function () {
        $(btn).ajaxEnable();
      }
    });
  });

  $("#question-form").on("keydown", "input[name='question-description']", function (event) {
    if (event.keyCode == 13) { // Enter, Return
      var tr = $(this).closest("tr");
      $(".btn-save-question", tr).click();
      return false;
    } else if (event.keyCode == 27) { // ESC
      var tr = $(this).closest("tr");
      $(".btn-cancel-question", tr).click();
      return false;
    }
  });

  var manageQuestionsOrder = function () {
    var orders = "";
    $("#question-form table tbody tr").each(function () {
      var questionId = $(this).attr("data-question-id");
      var rowOrder = $(this).index();
      orders += questionId + ":" + rowOrder + ",";
      $("[name='question-order']", this).val(rowOrder);
    });

    var review_id = $("#review-id").val();
    var csrf_token = $("#question-form input[name='csrfmiddlewaretoken']").val();

    $.ajax({
      url: '/reviews/planning/save_question_order/',
      type: 'post',
      cache: false,
      data: {
        'csrfmiddlewaretoken': csrf_token,
        'review-id': review_id,
        'orders': orders
      }
    });
  };

  $("#question-form").on("click", ".js-order-research-question-up", function () {
    var i = $(this).closest("tr").index();
    if (i > 0) {
      var sibling = $("#question-form table tbody tr:eq(" + (i - 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).before(row);
      manageQuestionsOrder();
    }
    return false;
  });

  $("#question-form").on("click", ".js-order-research-question-down", function () {
    var container = $(this).closest("tbody");
    var rows = $("tr", container).length - 1;
    var i = $(this).closest("tr").index();
    if (i < rows) {
      var sibling = $("#question-form table tbody tr:eq(" + (i + 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).after(row);
      manageQuestionsOrder();
    }
    return false;
  });

});