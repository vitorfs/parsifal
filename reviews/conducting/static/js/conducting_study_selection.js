$(function () {

  $(".btn-import-bibtex").click(function () {
    var container = $(this).closest(".articles");
    $("input[type=file]", container).click();
  });

  $.fn.loadArticles = function () {
    var div = $(this);
    $.ajax({
      url: '/reviews/conducting/source_articles/',
      data: { 'review-id': $("#review-id").val(), 'source-id': $("input[name='source-id']", div).val() },
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(".source-articles", div).loading();
      },
      success: function (data) {
        $(".source-articles", div).html(data);
      },
      complete: function () {
        $(".source-articles", div).stopLoading();
      }
    });
  };

  if($("ul#source-tab li.active").length == 0) {
    $("ul#source-tab li:eq(0)").addClass("active");
    var div = $("div.source-tab-content div.articles:eq(0)");
    $(div).show();
    $(div).loadArticles();
  }

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

  $.fn.loadActiveArticle = function () {
    var article_id = $(".source-articles tbody tr.active").attr("oid");
    var review_id = $("#review-id").val();
    var container = $(this);
    $.ajax({
      url: '/reviews/conducting/article_details/',
      data: {'review-id': review_id, 'article-id': article_id},
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(container).loading();
      },
      success: function (data) {
        $(container).html(data);
      },
      complete: function () {
        $(container).stopLoading();
      }
    });
  };

  $(".source-articles").on("click", "tr", function () {
    $(".source-articles tbody tr").removeClass("active");
    $(this).addClass("active");
    $("#modal-article .modal-body").loadActiveArticle();
    $("#modal-article").open();
  });

  $("body").keydown(function (event) {
    var keyCode = event.which?event.which:event.keyCode;

    if (keyCode == ESCAPE_KEY) {
      if ($("body").hasClass("modal-open")) {
        $(".modal").close();  
      }
      else {
        $(".source-articles tbody tr").removeClass("active");    
      }
    }
    else if (!$("body").hasClass("modal-open")) {
      if (keyCode == UP_ARROW_KEY) {
        event.preventDefault();
        move(BACKWARD);
      }
      else if (keyCode == DOWN_ARROW_KEY) {
        event.preventDefault();
        move(FORWARD);
      }
      else if (keyCode == ENTER_KEY) {
       $(".source-articles tbody tr.active").click();
      }
    }
  });

  function move(step) {
    var active = $(".source-articles tbody tr.active").index();
    var size = $(".source-articles tbody tr").size();
    active = (active + step) % size;
    $(".source-articles tbody tr").removeClass("active");
    $(".source-articles tbody tr:eq("+active+")").addClass("active");
  }

  $("#btn-previous").click(function () {
    move(BACKWARD);
    $("#modal-article .modal-body").loadActiveArticle();
  });

  $("#btn-next").click(function () {
    move(FORWARD);
    $("#modal-article .modal-body").loadActiveArticle();
  });
  
  $("#btn-save-suggested-sources").click(function () {
    $.ajax({
      url: '/reviews/conducting/save_article_details/',
      cache: false,
      data: $("#article-details").serialize(),
      type: 'post',
      beforeSend: function () {

      },
      success: function (data) {

      },
      error: function () {

      }
    });
  });

  $("#modal-article").on("click", "ul.tab a", function () {
    var tab_id = $(this).attr("href");
    $("#modal-article div.tabs > div").hide();
    $("#modal-article ul.tab li").removeClass("active");
    $(this).closest("li").addClass("active");
    $(tab_id).show();
    return false;
  });
  
});