$(function () {
  IS_ADDING_NEW_FIELD = false;

  $("#btn-add-field").click(function () {
    if (!IS_ADDING_NEW_FIELD) {
      IS_ADDING_NEW_FIELD = true;
      $.ajax({
        url: '/reviews/planning/add_new_data_extraction_field/',
        data: {'review-id': $('#review-id').val()},
        type: 'get',
        cache: false,
        success: function (data) {
          $("#tbl-data-extraction tbody").prepend(data);
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
    IS_ADDING_NEW_FIELD = false;
    $(this).closest("tr").fadeOut(400, function () {
      $(this).remove();
    });
  });

  // Save a new data extraction field
  $("table#tbl-data-extraction").on("click", "#btn-save-data-extraction-field", function () {
    var row = $(this).closest("tr");
    var description = $("#data-extraction-field-description").val();
    var field_type = $("#data-extraction-field-type").val();
    var lookup_values = $("#data-extraction-lookup-values").val();
    var review_id = $("#review-id").val();
    var csrf_token = $(row).attr("csrf-token");

    $.ajax({
      url: '/reviews/planning/save_data_extraction_field/',
      data: {'review-id': review_id, 
        'description': description, 
        'field-type': field_type, 
        'lookup-values': lookup_values,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $(row).fadeOut(400, function () {
          $(this).remove();
          $("#tbl-data-extraction tbody").prepend(data);
        });
      },
      error: function (jqXHR, textStatus, errorThrown) {

      },
      complete: function () {
        IS_ADDING_NEW_FIELD = false;
      }
    });
  });

  // Remove a data extraction field
  $("table#tbl-data-extraction").on("click", ".btn-remove-data-extraction-field", function () { 
    var field_id = $(this).closest("tr").attr("oid");
    var review_id = $("#review-id").val();

    var row = $(this).closest("tr");
    
    $.ajax({
      url: '/reviews/planning/remove_data_extraction_field/',
      data: {'review-id': review_id, 'field-id': field_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).fadeOut(400, function () {
          $(row).remove();
        });
      },
      error: function (jqXHR, textStatus, errorThrown) {

      }
    });
  });

});