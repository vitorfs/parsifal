$(function () {
  $("td.answer").click(function () {
    if ($(this).hasClass("selected-answer")) {
      $(this).removeClass("selected-answer");
    }
    else {
      var answer_id = $(this).attr("answer-id");
      var question_id = $(this).closest("tr").attr("question-id");
      var article_id = $(this).closest("table").attr("article-id");
      var csrf_token = $(this).closest("table").attr("csrf-token");
      var review_id = $("#review-id").val();

      var tbl = $(this).closest("table");
      var td = $(this);

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
        success: function (data) {
          $('.score', tbl).text(data);
          $(td).siblings().removeClass("selected-answer");
          $(td).addClass("selected-answer");
        }
      });
    }
  });

  $("#all-filter").click(function () {
    $(".quality-assessment table").show();
  });


  $("#done-filter").click(function () {
    var questions_count = parseInt($("#questions-count").val());
    $(".quality-assessment table").each(function () {
      if ($("td.selected-answer", this).length != questions_count) {
        $(this).hide();
      }
      else {
        $(this).show();
      }
    });
  });


  $("#pending-filter").click(function () {
    var questions_count = parseInt($("#questions-count").val());
    $(".quality-assessment table").each(function () {
      if ($("td.selected-answer", this).length != questions_count) {
        $(this).show();
      }
      else {
        $(this).hide();
      }
    });
  });


  $("#score-higher-filter").click(function () {
    var cutoff_score = parseFloat($("#cutoff-score").val());
    $(".quality-assessment table").each(function () {
      var score = parseFloat($("span.score", this).text());
      if (score > cutoff_score) {
        $(this).show();
      }
      else {
        $(this).hide();
      }
    });
  });

  $("#score-lower-filter").click(function () {
    var cutoff_score = parseFloat($("#cutoff-score").val());
    $(".quality-assessment table").each(function () {
      var score = parseFloat($("span.score", this).text());
      if (score <= cutoff_score) {
        $(this).show();
      }
      else {
        $(this).hide();
      }
    });
  });
      
});