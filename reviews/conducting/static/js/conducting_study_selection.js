function isScrolledIntoView(elem) {
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

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
    var row = $(".source-articles tbody tr.active");

    var active = $(".source-articles tbody tr.active").index();
    var old_active = active;
    var size = $(".source-articles tbody tr").size();
    var next;
    do {
      active = (active + step) % size;  
      next = $(".source-articles tbody tr:eq("+active+")");
    } while($(next).is(":hidden"));
    $(".source-articles tbody tr").removeClass("active");
    $(next).addClass("active");

    if (!isScrolledIntoView(row)) {
      if (active > old_active)
        $('html, body').animate({scrollTop: $(row).offset().top}, 2000);
      else
        $('html, body').animate({scrollTop: $(row).offset().top - $(window).height()}, 2000);
    }
  }

  $("#btn-previous").click(function () {
    move(BACKWARD);
    $("#modal-article .modal-body").loadActiveArticle();
  });

  $("#btn-next").click(function () {
    move(FORWARD);
    $("#modal-article .modal-body").loadActiveArticle();
  });

  function save_article(move_next) {
    var article_id = $("#modal-article #article-id").val();
    $.ajax({
      url: '/reviews/conducting/save_article_details/',
      cache: false,
      data: $("#article-details").serialize(),
      type: 'post',
      beforeSend: function () {
        $("#btn-save-article").prop("disabled", true);
      },
      success: function (data) {
        $(".source-articles table tbody tr[oid=" + article_id + "]").replaceWith(data);
        $(".source-articles table tbody tr[oid=" + article_id + "]").addClass("active");
        if (move_next) {
          move(FORWARD);
          $("#modal-article .modal-body").loadActiveArticle();
        }
        else {
          $("#modal-article .alert span").text("Article successfully saved!");
          $("#modal-article .alert").removeClass("article-error").addClass("alert-success");
          $("#modal-article .alert").show();
        }
      },
      error: function () {
          $("#modal-article .alert span").text("Something went wrong! That's all we know :(");
          $("#modal-article .alert").removeClass("article-success").addClass("alert-error");
          $("#modal-article .alert").show();
      },
      complete: function () {
        $("#btn-save-article").prop("disabled", false);
      }
    });
  }
  
  $("#btn-save-article").click(function () {
    save_article(false);
  });

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
      save_article(true);
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

  function multiple_articles_actions(article_ids, action) {
    var review_id = $("#review-id").val();
    var csrf_token = $(".source-tab-content table").attr("csrf-token");

    $.ajax({
      url: '/reviews/conducting/multiple_articles_action/' + action + '/',
      data: {
        'review-id': review_id,
        'article_ids': article_ids,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(".go-button").prop("disabled", true);
        $(".go-button").text("Processing...");
      },
      success: function (data) {
        switch (action) {
          case "remove":
            $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
              $(this).closest("tr").remove();
            });
            break;
          case "accept":
            $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
              var row = $(this).closest("tr");
              $(row).attr("article-status", "A");
              $("span", row).replaceWith("<span class='label label-success'>Accepted</span>");
            });
            break;
          case "reject":
            $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
              var row = $(this).closest("tr");
              $(row).attr("article-status", "R");
              $("span", row).replaceWith("<span class='label label-warning'>Rejected</span>");
            });
            break;
        }
      },
      error: function () {

      },
      complete: function () {
        $(".go-button").prop("disabled", false);
        $(".go-button").text("Go");
      }
    });
  }

  $(".source-tab-content").on("click", ".go-button", function () {
    var article_ids = '';
    var action = $(".source-tab-content .select-action").val();
    if (action) {
      $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
        article_ids += $(this).val() + "|";
      });
      if (article_ids) {
        article_ids = article_ids.substring(0, article_ids.length - 1);
        switch (action) {
          case "remove":
            multiple_articles_actions(article_ids, action);
            break;
          case "accept":
            multiple_articles_actions(article_ids, action);
            break;
          case "reject":
            multiple_articles_actions(article_ids, action);
            break;
        }
      }
    }
  });

  $(".source-tab-content").on("click", ".source-articles table thead tr th a", function () {
    var a = $(this);
    var column = $(a).attr("col");
    $.ajax({
      url: '/reviews/conducting/articles/order_by/',
      data: {
        'review-id': $("#review-id").val(),
        'source-id': $(".source-tab-content form input[name=source-id]").val(),
        'column': column
      },
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(".source-articles table tbody").replaceWith("<tbody><tr><td colspan='7'></td></tr></tbody>");
        $(".source-articles table tbody tr td").loading();
      },
      success: function (data) {
        $(".source-articles table tbody").replaceWith(data);
      },
      complete: function () {
        if ($(a).attr("col").indexOf("-") == 0) {
          $(a).attr("col", $(a).attr("col").replace("-", ""));
        }
        else {
          $(a).attr("col", "-" + $(a).attr("col"));
        }
      }
    });
    return false;
  });

  // On page load

  if ($("ul#source-tab li").length > 0) {
    if($("ul#source-tab li.active").length == 0) {
      $("ul#source-tab li:eq(0)").addClass("active");
    }
    $("#source-tab li.active a").click();
  }

});