$(function () {
  $(".js-save-source-string").click(function () {
    var btn = $(this);
    var form = $(this).closest("form");
    var url = $(this).attr("data-remote");
    $.ajax({
      url: url,
      data: $(form).serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function () {
        var source_id = $("[name='source-id']", form).val();
        var search_string = $("[name='search_string']", form).val();
        $("[data-source-id='" + source_id + "'] textarea[name='query']").val(search_string);
      },
      complete: function () {
        $(btn).ajaxEnable();
      }
    });
  });

  $(".js-import-base-string").click(function () {
    var btn = $(this);
    var form = $(this).closest("form");
    var url = $(this).attr("data-remote");
    $.ajax({
      url: url,
      data: $(form).serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $("textarea[name='search_string']", form).val(data);
        var source_id = $("[name='source-id']", form).val();
        $("[data-source-id='" + source_id + "'] textarea[name='query']").val(data);
      },
      complete: function () {
        $(btn).ajaxEnable();
      }
    });
  });

  $(".source-search textarea:visible").expanding();

  $("#remote-search-panels .panel-collapse").on("show.bs.collapse", function () {
    var panel = $(this).closest(".panel");
    $("[data-toggle='collapse'] .glyphicon", panel).removeClass().addClass("glyphicon glyphicon-minus pull-right");
  });

  $("#remote-search-panels .panel-collapse").on("hide.bs.collapse", function () {
    var panel = $(this).closest(".panel");
    $("[data-toggle='collapse'] .glyphicon", panel).removeClass().addClass("glyphicon glyphicon-plus pull-right");
  });

  $("#remote-search-panels .panel-collapse").on("shown.bs.collapse", function () {
    $("textarea", this).each(function () {
      if (!$(this).hasClass("expanding")) {
        $(this).expanding();
      }
    });
  });

  $.fn.displaySearchResults = function (data) {
    var container = $(this);
    if (data !== null) {
      $("table tbody", container).html("");

      data["search-results"].entry.forEach(function (entry) {
        var citations = entry["citedby-count"];
        if (citations === undefined) {
          citations = "";
        }
        $("table tbody", container).append("<tr><td>" +  entry["dc:title"] + "</td><td>" + entry["dc:creator"] + "</td><td>" + entry["prism:coverDisplayDate"] + "</td><td>" + entry["prism:publicationName"] + "</td><td>" + citations + "</td></tr>");
      });

      data["search-results"].link.forEach(function (link) {
        var pager = $(".pager a[ref='" + link["@ref"] + "']");
        $(pager).attr("href", link["@href"]);
        $(pager).closest("li").removeClass("disabled");
      });

      $(".document-results", container).text(data["search-results"]["opensearch:totalResults"]);
      $("form", container).attr("data-remote-status", "loaded");
    }
    else {
      $("table tbody", container).html("<tr><td colspan='5'>No data</td></tr>");
    }
  };

  $(".source-search").submit(function () {
    var container = $(this).closest(".panel-body");
    var form = $(this);
    var url = $(this).attr("action");
    var data = $(this).serialize();
    var status = $(form).attr("data-remote-status");

    if (status !== "loading") {
      $.ajax({
        url: url,
        data: data,
        cache: true,
        dataType: 'json',
        beforeSend: function () {
          $("[name='page-query']", form).val($("[name='query']", form).val());
          $("button[type='submit']", form).ajaxDisable();
          $("table tbody", container).html("<tr><td colspan='5' class='loading-placeholder'></td></tr>");
          $(".loading-placeholder", container).spinner(false);
          $(".block-spinner", container).css("margin", "30px auto");
          $(form).attr("data-remote-status", "loading");
        },
        success: function (data) {
          $(container).displaySearchResults(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
          $(form).attr("data-remote-status", "error");
          $("table tbody", container).html("<tr><td colspan='5'>" + jqXHR.responseText + "</td></tr>");
        },
        complete: function () { 
          $("button[type='submit']", form).ajaxEnable();
        }
      });
    }
    return false;
  });

  $(".source-search [name='count']").change(function () {
    $(this).closest("form").submit();
  });

  $(".source-search .pager a").click(function (e) {
    e.preventDefault();
    var isDisabled = $(this).closest("li").hasClass("disabled");
    if (!isDisabled) {
      
      var container = $(this).closest(".panel-body");
      var form = $(this).closest("form");
      var url = $(form).attr("action");
      var status = $(form).attr("data-remote-status");

      var href = $(this).attr("href");
      var start = href.split('start=')[1].split('&')[0];
      var query = $("[name='page-query']", form).val();
      var count = href.split('count=')[1].split('&')[0];

      var review_id = $("[name='review-id']", form).val();

      if (status !== "loading") { 
        $.ajax({
          url: url,
          data: {
            'review-id': review_id,
            'query': query,
            'start': start,
            'count': count
          },
          cache: true,
          dataType: 'json',
          beforeSend: function () {
            $("table tbody", container).html("<tr><td colspan='5' class='loading-placeholder'></td></tr>");
            $(".loading-placeholder", container).spinner(false);
            $(".block-spinner", container).css("margin", "30px auto");
            $(form).attr("data-remote-status", "loading");
            $(".pager li", container).addClass("disabled");
          },
          success: function (data) {
            $(container).displaySearchResults(data);
          },
          error: function (jqXHR, textStatus, errorThrown) {
            $(form).attr("data-remote-status", "error");
            $("table tbody", container).html("<tr><td colspan='5'>" + jqXHR.responseText + "</td></tr>");
          }
        });
      }
    }
    return false;
  });

  $(".js-save-elsevier-string").click(function () {
    var btn = $(this);
    var form = $(this).closest("form");
    var url = $(this).attr("data-remote");
    var search_string = $("[name='query']", form).val();
    var review_id = $("[name='review-id']", form).val();
    var source_id = $("[name='source-id']", form).val();
    $.ajax({
      url: url,
      data: {
        'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
        'search_string': search_string,
        'review-id': review_id,
        'source-id': source_id,
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function () {
        $("#source_" + source_id + " textarea[name='search_string']").val(search_string);
      },
      complete: function () {
        $(btn).ajaxEnable();
      }
    });
  });

  $(".js-remove-source-string").click(function () {
    $(this).ajaxDisable();
    var form = $(this).closest("form");
    var url = $(this).attr("data-remote");
    $(form).attr("action", url);
    $(form).submit();
  });

});
