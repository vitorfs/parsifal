$(function () {
  $("td.answer").click(function () {
    if ($(this).hasClass("selected-answer")) {
      $(this).removeClass("selected-answer");
    }
    else {
      $(this).siblings().removeClass("selected-answer");
      $(this).addClass("selected-answer");

      var answer_id = $(this).attr("answer-id");
      var question_id = $(this).closest("tr").attr("question-id");
      var article_id = $(this).closest("table").attr("article-id");
      var review_id = $("#review-id").val();

      var tbl = $(this).closest("table");

      $.ajax({
        url: '/reviews/conducting/save_quality_assessment/',
        data: {'review-id': review_id, 'article-id': article_id, 'question-id': question_id, 'answer-id': answer_id},
        type: 'get',
        cache: false,
        success: function (data) {
          $('.score', tbl).text(data);
        }
      });
    }
  });
});