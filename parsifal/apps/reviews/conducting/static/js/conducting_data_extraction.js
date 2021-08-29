$(function () {

  function save_data_extraction_field(ref) {
    var row = $(ref).closest(".form-group");
    var review_id = $("#review-id").val();
    var article_id = $(ref).closest(".panel-body").attr("data-article-id");
    var field_id = $(row).attr("data-field-id");
    var value = $(ref).val();
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: '/reviews/conducting/save_data_extraction/',
      data: {
        'review-id': review_id,
        'article-id': article_id,
        'field-id': field_id,
        'value': value,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $("span.error", row).text('');
        $("span.error", row).hide();
        $(row).removeClass("has-error");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $("span.error", row).text(jqXHR.responseText);
        $("span.error", row).show();
        $(row).addClass("has-error");
      }
    });
  }

  $(".data-extraction-panel input[type='text'], .data-extraction-panel select, .data-extraction-panel textarea").change(function () {
    save_data_extraction_field($(this));
  });

  $(".data-extraction-panel input[type='checkbox']").click(function () {
    save_data_extraction_field($(this));
  });

  $(".data-extraction-panel").on("click", ".js-mark-as-finished", function () {
    var panel = $(this).closest(".panel");
    var article_id = $(".panel-body", panel).attr("data-article-id");
    $.ajax({
      url: '/reviews/conducting/save_data_extraction_status/',
      type: 'post',
      data: {
        'review-id': $("#review-id").val(),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        'article-id': article_id,
        'action': 'mark_as_done'
      },
      success: function () {
        var tab = $("#data-extraction-tab").val();
        if (tab === "all") {
          var action_button = $(".js-finished-button", panel);
          $(".glyphicon", action_button).removeClass().addClass("glyphicon glyphicon-check");
          $(".action-text", action_button).text("mark as undone");
          $(action_button).removeClass().addClass("js-finished-button js-mark-as-not-finished");
        } 
        else {
          $(panel).fadeOut(200);
        }
      }
    });
  });

  $(".data-extraction-panel").on("click", ".js-mark-as-not-finished", function () {
    var panel = $(this).closest(".panel");
    var article_id = $(".panel-body", panel).attr("data-article-id");
    $.ajax({
      url: '/reviews/conducting/save_data_extraction_status/',
      type: 'post',
      data: {
        'review-id': $("#review-id").val(),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        'article-id': article_id,
        'action': 'mark_as_undone'
      },
      success: function () {
        var tab = $("#data-extraction-tab").val();
        if (tab === "all") {
          var action_button = $(".js-finished-button", panel);
          $(".glyphicon", action_button).removeClass().addClass("glyphicon glyphicon-unchecked");
          $(".action-text", action_button).text("mark as done");
          $(action_button).removeClass().addClass("js-finished-button js-mark-as-finished");
        } 
        else {
          $(panel).fadeOut(200);
        }
      }
    });
  });

});