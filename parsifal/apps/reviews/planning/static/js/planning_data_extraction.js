$(function () {
  IS_ADDING_OR_EDITING_FIELD = false;

  $("#btn-add-field").click(function () {
    if (!IS_ADDING_OR_EDITING_FIELD) {
      IS_ADDING_OR_EDITING_FIELD = true;
      $.ajax({
        url: '/reviews/planning/add_new_data_extraction_field/',
        data: {'review-id': $('#review-id').val()},
        type: 'get',
        cache: false,
        success: function (data) {
          $("#tbl-data-extraction tbody").append(data);
          $("#data-extraction-field-description").focus();
        }
      });
    }
  });

  // Hide or show the textarea for lookup values (select one field and select many field)
  $("table#tbl-data-extraction").on("change", "#data-extraction-field-type", function () {
    if ($(this).val() == 'O' || $(this).val() == 'M') {
      $(".no-select-field").hide();
      $(".select-field").show();
    }
    else {
      $(".select-field").hide();
      $(".no-select-field").show();
    }
  });

  // Cancel the creation of a new data extraction field
  $("table#tbl-data-extraction").on("click", "#btn-cancel-data-extraction-field", function () {
    IS_ADDING_OR_EDITING_FIELD = false;
    $(this).closest("tr").fadeOut(200, function () {
      $(this).remove();
      $("tr.data-extraction-field-hidden-for-edition").show();
      $("tr.data-extraction-field-hidden-for-edition").removeClass("data-extraction-field-hidden-for-edition");
    });
  });

  // Save a data extraction field
  $("table#tbl-data-extraction").on("click", "#btn-save-data-extraction-field", function () {
    var row = $(this).closest("tr");
    var description = $("#data-extraction-field-description").val();
    var field_type = $("#data-extraction-field-type").val();
    var lookup_values = $("#data-extraction-lookup-values").val();
    var review_id = $("#review-id").val();
    var field_id = $(row).attr("oid");
    var csrf_token = $(row).attr("csrf-token");
    var btn = $(this);

    $.ajax({
      url: '/reviews/planning/save_data_extraction_field/',
      data: {'review-id': review_id, 
        'description': description, 
        'field-type': field_type, 
        'lookup-values': lookup_values,
        'field-id': field_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(btn).ajaxEnable();
        if (field_id == 'None') {
          $(row).remove();
          $("#tbl-data-extraction tbody").append(data);
        }
        else {
          $("tr.data-extraction-field-hidden-for-edition").after(data);
          $("tr.data-extraction-field-hidden-for-edition").remove();
          $(row).remove();
        }
        IS_ADDING_OR_EDITING_FIELD = false;
        manageFieldOrder();
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $(btn).ajaxEnableError();
      },
      complete: function () {
        
      }
    });
  });

  // Remove a data extraction field
  $("table#tbl-data-extraction").on("click", ".btn-remove-data-extraction-field", function () { 
    var field_id = $(this).closest("tr").attr("oid");
    var review_id = $("#review-id").val();
    var btn = $(this);
    var row = $(this).closest("tr");
    
    $.ajax({
      url: '/reviews/planning/remove_data_extraction_field/',
      data: {'review-id': review_id, 'field-id': field_id},
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(row).fadeOut(200, function () {
          $(row).remove();
        });
      },
      error: function (jqXHR, textStatus, errorThrown) {

      },
      complete: function () {
        $(btn).ajaxEnable();
      }
    });
  });


  // Enable data extraction field for edition
  $("table#tbl-data-extraction").on("click", ".btn-edit-data-extraction-field", function () {
    if (!IS_ADDING_OR_EDITING_FIELD) {
      IS_ADDING_OR_EDITING_FIELD = true;
      var field_id = $(this).closest("tr").attr("oid");
      var review_id = $("#review-id").val();
      var btn = $(this);
      var row = $(this).closest("tr");

      $.ajax({
        url: '/reviews/planning/edit_data_extraction_field/',
        data: {'review-id': review_id, 'field-id': field_id},
        type: 'get',
        cache: false,
        beforeSend: function () {
          $(btn).ajaxDisable();
        },
        success: function (data) {
          $(row).hide();
          $(row).after(data);
          $(row).addClass("data-extraction-field-hidden-for-edition");
        },
        complete: function () {
          $(btn).ajaxEnable();
        }
      });
    }
  });

  var manageFieldOrder = function () {
    var orders = "";
    $("#tbl-data-extraction tbody tr").each(function () {
      var fieldId = $(this).attr("oid");
      var rowOrder = $(this).index();
      orders += fieldId + ":" + rowOrder + ",";
      $("[name='data-extraction-field-order']", this).val(rowOrder);
    });

    var review_id = $("#review-id").val();
    var csrf_token = $("[name='csrfmiddlewaretoken']").val();

    $.ajax({
      url: '/reviews/planning/save_data_extraction_field_order/',
      type: 'post',
      cache: false,
      data: {
        'csrfmiddlewaretoken': csrf_token,
        'review-id': review_id,
        'orders': orders
      }
    });
  };

  $("#tbl-data-extraction").on("click", ".js-order-field-up", function () {
    var i = $(this).closest("tr").index();
    if (i > 0) {
      var sibling = $("#tbl-data-extraction tbody tr:eq(" + (i - 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).before(row);
      manageFieldOrder();
    }
    return false;
  });

  $("#tbl-data-extraction").on("click", ".js-order-field-down", function () {
    var container = $(this).closest("tbody");
    var rows = $("tr", container).length - 1;
    var i = $(this).closest("tr").index();
    if (i < rows) {
      var sibling = $("#tbl-data-extraction tbody tr:eq(" + (i + 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).after(row);
      manageFieldOrder();
    }
    return false;
  });

});