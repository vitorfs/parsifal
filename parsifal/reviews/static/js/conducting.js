$(function () {
  $("ul#source-tab li:first-child").addClass("active");

  $(".btn-suggested-search-string").click(function () {
    $.ajax({
      url: '/reviews/conducting/generate_search_string/',
      data: { 'review_id': $("#review-id").val() },
      cache: false,
      type: 'get',
      success: function (data) {
        $(".search-string").val(data);
      }
    });
  });
});