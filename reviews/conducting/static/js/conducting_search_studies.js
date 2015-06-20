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
        cache: false,
        dataType: 'json',
        beforeSend: function () {
          $("button[type='submit']", form).ajaxDisable();
          $("table tbody", container).html("<tr><td colspan='5' class='loading-placeholder'></td></tr>");
          $(".loading-placeholder", container).spinner(false);
          $(".block-spinner", container).css("margin", "30px auto");
          $(form).attr("data-remote-status", "loading");
        },
        success: function (data) {
          if (data !== null) {
            $("table tbody", container).html("");
            data["search-results"].entry.forEach(function (entry) {
              $("table tbody", container).append("<tr><td>" +  entry["dc:title"] + "</td><td>" + entry["dc:creator"] + "</td><td>" + entry["prism:coverDisplayDate"] + "</td><td>" + entry["prism:publicationName"] + "</td><td>" + entry["citedby-count"] + "</td></tr>");
            });
            $(".document-results", container).text(data["search-results"]["opensearch:totalResults"]);
            $(form).attr("data-remote-status", "loaded");
          }
          else {
            $("table tbody", container).html("<tr><td colspan='5'>No data</td></tr>");
          }
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

  $(".js-save-elsevier-string").click(function () {
    var btn = $(this);
    var form = $(this).closest("form");
    var url = $(this).attr("data-remote");
    $.ajax({
      url: url,
      data: {
        'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
        'search_string': $("[name='query']", form).val(),
        'review-id': $("[name='review-id']", form).val(),
        'source-id': $("[name='source-id']", form).val(),
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
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
