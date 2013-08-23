$(function () {
  $("ul#source-tab li:eq(0)").addClass("active");

  $("div.source-tab-content div.articles:eq(0)").show();


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

  $("#source-tab a").click(function () {
    var tab_id = $(this).attr("href");
    $("div.source-tab-content div.articles").hide();
    $("ul#source-tab li").removeClass("active");
    $(this).closest("li").addClass("active");
    $(tab_id).show();
    return false;
  });

});