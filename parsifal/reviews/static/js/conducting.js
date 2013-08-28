$(function () {

  $.fn.loadArticles = function () {
    var div = $(this);
    $.ajax({
      url: '/reviews/conducting/source_articles/',
      data: { 'review-id': $("#review-id").val(), 'source-id': $("input[name='source-id']", div).val() },
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(".source-articles", div).html("<p>Loading data...</p>");
      },
      success: function (data) {
        $(".source-articles", div).html(data);
      }
    });
  };
  
  $("ul#source-tab li:eq(0)").addClass("active");

  var div = $("div.source-tab-content div.articles:eq(0)");
  $(div).show();
  $(div).loadArticles();

  $(".btn-suggested-search-string").click(function () {
    var form = $(this).closest("form");
    $.ajax({
      url: '/reviews/conducting/generate_search_string/',
      data: { 'review-id': $("#review-id").val() },
      cache: false,
      type: 'get',
      success: function (data) {
        $(".search-string", form).val(data);
      }
    });
  });

  $(".btn-save-generic-search-string").click(function () {
    var btn = $(this);
    var form = $(this).closest("form");
    var search_string = $(".search-string", form).val();
    $.ajax({
      url: '/reviews/conducting/save_generic_search_string/',
      data: $(form).serialize(),
      cache: false,
      type: 'post',
      success: function (data) {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-error").addClass("text-success");
        msg.text('Your search string have been saved successfully!');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      },
      error: function () {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-success").addClass("text-error");
        msg.text('Something went wrong! Please contact the administrator.');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      }
    });
  });

  $("#source-tab a").click(function () {
    var tab_id = $(this).attr("href");
    $("div.source-tab-content div.articles").hide();
    $("ul#source-tab li").removeClass("active");
    $(this).closest("li").addClass("active");
    $(tab_id).show();
    $(tab_id).loadArticles();
    return false;
  });

  $("input[name='bibtex']").change(function () {
    var form = $(this).closest("form");
    $(form).submit();
  });

});