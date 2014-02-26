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

  // Cancel the creation of a new data field
  $("table#tbl-data-extraction").on("click", "#btn-cancel-data-extraction-field", function () {
    IS_ADDING_NEW_FIELD = false;
    $(this).closest("tr").fadeOut(400, function () {
      $(this).remove();
    });
  });

  // Save a new data field
  $("table#tbl-data-extraction").on("click", "#btn-save-data-extraction-field", function () {
    var description = $("#data-extraction-field-description").val();
    var field_type = $("#data-extraction-field-type").val();
    var review_id = $("#review-id").val();

    var row = $(this).closest("tr");

    $.ajax({
      url: '/reviews/planning/save_data_extraction_field/',
      data: {'review-id': review_id, 'description': description, 'field-type': field_type},
      type: 'get',
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

});