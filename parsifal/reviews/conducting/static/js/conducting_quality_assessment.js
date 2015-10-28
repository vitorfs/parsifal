$(function () {

  $("#quality-menu li a").click(function () {
    var a = $(this);
    $.ajax({
      url: $(a).attr("href"),
      data: { 'review-id': $('#review-id').val() },
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(".quality-container").loading();
      },
      success: function (data) {
        $(".quality-container").html(data);
      },
      complete: function () {
        $(".quality-container").stopLoading();
        $("#quality-menu li").removeClass("active");
        $(a).closest("li").addClass("active");
      }
    });
    return false;
  });

  $(".quality-container").on("click", "td.answer", function () {
    if (!$(this).hasClass("selected-answer")) {
      var answer_id = $(this).attr("answer-id");
      var question_id = $(this).closest("tr").attr("question-id");
      var article_id = $(this).closest("table").attr("article-id");
      var csrf_token = $(this).closest("table").attr("csrf-token");
      var review_id = $("#review-id").val();

      var tbl = $(this).closest(".panel");
      var td = $(this);

      var old_text = $(td).text();

      $.ajax({
        url: '/reviews/conducting/save_quality_assessment/',
        data: {'review-id': review_id, 
          'article-id': article_id, 
          'question-id': question_id, 
          'answer-id': answer_id,
          'csrfmiddlewaretoken': csrf_token
        },
        type: 'post',
        cache: false,
        beforeSend: function () {
          $(td).text("Processing...");
        },
        success: function (data) {
          $('.score', tbl).text(data);
          $(td).siblings().removeClass("selected-answer");
          $(td).addClass("selected-answer");
        },
        complete: function () {
          $(td).text(old_text);
        }
      });
    }
  });

  $(".quality-container").on("click", "#all-filter", function () {
    $(".quality-assessment .panel-quality-assessment").show();
  });

  $(".quality-container").on("click", "#done-filter", function () {
    var questions_count = parseInt($("#questions-count").val());
    $(".quality-assessment .panel-quality-assessment").each(function () {
      if ($("table td.selected-answer", this).length != questions_count) {
        $(this).hide();
      }
      else {
        $(this).show();
      }
    });
  });

  $(".quality-container").on("click", "#pending-filter", function () {
    var questions_count = parseInt($("#questions-count").val());
    $(".quality-assessment .panel-quality-assessment").each(function () {
      if ($("table td.selected-answer", this).length != questions_count) {
        $(this).show();
      }
      else {
        $(this).hide();
      }
    });
  });

  $(".quality-container").on("click", "#score-higher-filter", function () {
    var cutoff_score = parseFloat($("#cutoff-score").val());
    $(".quality-assessment .panel-quality-assessment").each(function () {
      var score = parseFloat($("span.score", this).text());
      if (score > cutoff_score) {
        $(this).show();
      }
      else {
        $(this).hide();
      }
    });
  });

  $(".quality-container").on("click", "#score-lower-filter", function () {
    var cutoff_score = parseFloat($("#cutoff-score").val());
    $(".quality-assessment .panel-quality-assessment").each(function () {
      var score = parseFloat($("span.score", this).text());
      if (score <= cutoff_score) {
        $(this).show();
      }
      else {
        $(this).hide();
      }
    });
  });

  $(".quality-container").on("change", "#quality-assessment-order", function () {
    $(this).closest("form").submit();
  });
      
});