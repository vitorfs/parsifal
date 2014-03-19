$(function () {

  $(".source-tab-content").on("click", ".btn-import-bibtex", function () {
    var container = $(this).closest(".articles");
    $("input[type=file]", container).click();
  });

  $(".source-tab-content").on("change", "input[name='bibtex']", function () {
    var form = $(this).closest("form");
    $(form).submit();
  });

  $("#source-tab a").click(function () {
    var source_id = $(this).attr("source-id");
    $("ul#source-tab li").removeClass("active");
    $(this).closest("li").addClass("active");

    $.ajax({
      url: '/reviews/conducting/source_articles/',
      data: { 'review-id': $("#review-id").val(), 'source-id': source_id },
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(".source-tab-content").loading();
      },
      success: function (data) {
        $(".source-tab-content").html(data);
      },
      complete: function () {
        $(".source-tab-content").stopLoading();
      }
    });

    return false;
  });

  $.fn.loadActiveArticle = function () {
    var article_id = $(".source-articles tbody tr.active").attr("oid");
    var review_id = $("#review-id").val();
    var container = $(this);

    var total_articles = $(".source-articles tbody tr:visible").length;
    var current_article = 0;
    $(".source-articles tbody tr:visible").each(function () {
      current_article++;
      if ($(this).attr("oid") == article_id) {
        return false;
      }
    });

    $("#modal-article span.current-article").text(current_article);
    $("#modal-article span.total-articles").text(total_articles);

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

  $(".source-tab-content").on("click", "tbody tr", function () {
    if (!$(this).hasClass("no-data")) {
      $(".source-articles tbody tr").removeClass("active");
      $(this).addClass("active");
      $("#modal-article .modal-body").loadActiveArticle();
      $("#modal-article").open();
    }
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
    var next;
    do {
      active = (active + step) % size;  
      next = $(".source-articles tbody tr:eq("+active+")");
    } while($(next).is(":hidden"));
    $(".source-articles tbody tr").removeClass("active");
    $(next).addClass("active");
  }

  $("#btn-previous").click(function () {
    move(BACKWARD);
    $("#modal-article .modal-body").loadActiveArticle();
  });

  $("#btn-next").click(function () {
    move(FORWARD);
    $("#modal-article .modal-body").loadActiveArticle();
  });

  function save_article() {
    var article_id = $("#modal-article #article-id").val();
    var row = $(".source-articles table tbody tr[oid=" + article_id + "]");
    $.ajax({
      url: '/reviews/conducting/save_article_details/',
      cache: false,
      data: $("#article-details").serialize(),
      type: 'post',
      beforeSend: function () {
        $("#btn-save-article").prop("disabled", true);
        $("#btn-save-article").text('Saving...');
      },
      success: function (data) {
        $(row).replaceWith(data);
        if ($("#save-and-move-next").is(":checked")) {
          move(FORWARD);
          $("#modal-article .modal-body").loadActiveArticle();
        }
      },
      error: function () {

      },
      complete: function () {
        $("#btn-save-article").prop("disabled", false);
        $("#btn-save-article").text('Save');
      }
    });
  }
  
  $("#btn-save-article").click(save_article);

  $("#modal-article").on("click", "ul.tab a", function () {
    var tab_id = $(this).attr("href");
    $("#modal-article div.tabs > div").hide();
    $("#modal-article ul.tab li").removeClass("active");
    $(this).closest("li").addClass("active");
    $(tab_id).show();
    return false;
  });

  $("#modal-article").on("change", "#status", function () {
    if ($("#save-and-move-next").is(":checked")) {
      save_article();
    }
  });

  function filter_articles(status) {
    if (status == "ALL") {
      $(".source-articles table tbody tr").show();
    }
    else {
      $(".source-articles table tbody tr").hide();
      $(".source-articles table tbody tr[article-status=" + status + "]").show();
    }
    $(".source-tab-content input[type=checkbox]").prop("checked", false);
    $(".source-articles tbody tr").removeClass("active");
  }

  $(".source-tab-content").on("click", "input[name=filter]", function () {
    filter_articles($(this).val());
  });

  $(".source-tab-content").on("click", "table tbody tr td input[type=checkbox]", function (event) {
    event.stopPropagation();
  });

  $(".source-tab-content").on("click", "#ck-all-articles", function () {
    $(".source-tab-content table tbody tr td input[type=checkbox]").prop("checked", false);
    if ($(this).is(":checked")) {
      $(".source-tab-content table tbody tr:visible td input[type=checkbox]").prop("checked", true);
    }
  });

  // On page load

  if ($("ul#source-tab li").length > 0) {
    if($("ul#source-tab li.active").length == 0) {
      $("ul#source-tab li:eq(0)").addClass("active");
    }
    $("#source-tab li.active a").click();
  }

});