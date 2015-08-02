$(function () {

  $("#import-pico-keywords").click(function () {
    $.ajax({
      url: '/reviews/planning/import_pico_keywords/',
      data: { 'review-id': $('#review-id').val() },
      cache: false,
      type: 'get',
      success: function (data) {
        $("#table-keywords tbody").append(data);
      }
    });
  });


  /* Delete functions */

  $("#table-keywords tbody").on("click", ".js-start-keyword-deletion", function () {
    var keyword_id = $(this).closest("tr").attr("data-keyword-id");
    var keyword_description = $(this).closest("tr").attr("data-keyword-description");

    $("#confirm-keyword-deletion").attr("data-keyword-id", keyword_id);
    $("#delete-keyword-name").text(keyword_description);

    $("#modal-confirm-keyword-deletion").modal("show");
  });

  $("#confirm-keyword-deletion").click(function () {
    var keyword_id = $(this).attr("data-keyword-id");
    var row = $("#table-keywords tbody tr[data-keyword-id='" + keyword_id + "']");
    $.ajax({
      url: '/reviews/planning/remove_keyword/',
      data: {
        'review-id': $('#review-id').val(), 
        'keyword-id': keyword_id 
      },
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).remove();
        $("#modal-confirm-keyword-deletion").modal("hide");
      }
    });
  });


  /* Edit functions */

  $("#table-keywords tbody").on("click", ".js-start-keyword-edit", function () {
    var review_id = $("#review-id").val();
    var keyword_id = $(this).closest("tr").attr("data-keyword-id");

    $.ajax({
      url: '/reviews/planning/edit_keyword/',
      data: {
        'review-id': review_id,
        'keyword-id': keyword_id
      },
      type: 'get',
      cache: false,
      beforeSend: function () {
        $("#modal-keyword").modal("show");
      },
      success: function (data) {
        $("#modal-keyword .modal-dialog").html(data.html);
      }
    });
  });


  /* Add functions */

  $("#add-keyword").click(function () {
    $.ajax({
      url: '/reviews/planning/add_keyword/',
      data: {
        'review-id': $("#review-id").val()
      },
      type: 'get',
      cache: false,
      beforeSend: function () {
        $("#modal-keyword").modal("show");
      },
      success: function (data) {
        $("#modal-keyword .modal-dialog").html(data.html);
      }
    });
  });

  $("#keywords-section").on("click", ".js-remove-synonym", function () {
    var container = $(this).closest("form");
    $(this).closest("tr").remove();
    $(container).updateFormsetIndex();
  });

  $("#keywords-section").on("click", ".js-add-synonym", function () {
      var container = $(this).closest("form");

      var totalForms = $("[id$='TOTAL_FORMS']", container).val();
      totalForms = parseInt(totalForms) + 1;
      $("[id$='TOTAL_FORMS']", container).val(totalForms);

      var formsetIndex = totalForms - 1;
      var template = $('#synonym-tr').html();
      var rendered = Mustache.render(template, { 'i': formsetIndex });
      $("table tbody", container).append(rendered);

      $("table tbody tr:last-child td:eq(0) input", container).focus();
  });

  $("#keywords-section").on("keydown", "#table-synonyms input", function (event) {
    var keyCode = event.which?event.which:event.keyCode;
    if (keyCode == TAB_KEY) {
      event.preventDefault();
      $("#keywords-section .js-add-synonym").click();
    }
  });

  $("#keywords-section").on("submit", "#new-keyword-form", function () {
    var form = $(this);
    $.ajax({
      url: $(form).attr("action"),
      data: $(form).serialize(),
      type: $(form).attr("method"),
      cache: false,
      beforeSend: function () {

      },
      success: function (data) {
        if (data.status == "ok") {
          $("#modal-keyword").modal("hide");
          $("#table-keywords tbody").append(data.html);
        }
        else if (data.status == "validation_error") {
          $("#modal-keyword .modal-dialog").html(data.html);
        }
      },
      error: function () {

      },
      complete: function () {

      }
    });
    return false;
  });

});