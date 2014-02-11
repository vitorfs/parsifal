$(function () {
  var is_adding_or_editing_source = false;
  var source_editing_id = "";
  var source_editing_html = "";

  function saveSource() {
    var name = $("input#name").val();
    var url = $("input#url").val();
    var review_id = $("input#review-id").val();

    $.ajax({
      url: '/reviews/planning/save_source/',
      data: { 
        'name': name, 
        'url': url, 
        'review-id': review_id,
        'source-id': source_editing_id
      },
      type: 'get',
      cache: false,
      beforeSend: function () {

      },
      success: function(data, textStatus, jqXHR) {
        if (source_editing_id != "") {
          var row = $("#tbl-sources tbody tr[source-id='" + source_editing_id + "']");
          $(data).insertAfter(row);
          row.remove();
        }
        else {
          $("#tbl-sources tbody tr:first-child").remove();
          $("#tbl-sources tbody").prepend(data);          
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {

      },
      complete: function () {
        is_adding_or_editing_source = false;
        source_editing_id = "";
        source_editing_html = "";
      }
    });
  }

  function cancelSource() {
    if (source_editing_id != "") {
      $("#tbl-sources tbody tr[source-id='" + source_editing_id + "']").html(source_editing_html);
      source_editing_id = "";
      source_editing_html = "";
    }
    else {
      $("#tbl-sources tbody tr:first-child").remove();
    }
    is_adding_or_editing_source = false;
  }

  function removeSource() {
    var button = $(this);
    var row = $(this).closest("tr");
    review_id = $("input#review-id").val();
    source_id = row.attr("source-id");
    $.ajax({
      url: '/reviews/planning/remove_source/',
      data: { 'review-id': review_id, 'source-id': source_id },
      type: 'get',
      cache: false,
      beforeSend: function () {

      },
      error: function () {

      },
      success: function(data) {
        row.remove();
      },
      complete: function () {
        
      }
    });
  }

  function editSource() {
    if (!is_adding_or_editing_source) {
      is_adding_or_editing_source = true;
      var button = $(this);
      var row = $(this).closest("tr");
      var name = $("td:eq(0)", row).text();
      var url = $("td:eq(1) a", row).text();
      source_editing_id = row.attr("source-id");
      source_editing_html = row.html();

      var str_row = '<td><input value="' + name + '" id="name"></td>';
      str_row += '<td><input value="' + url + '" id="url"></td>';
      str_row += '<td><button type="button" class="btn btn-success btn-small btn-save-source">save</button> <button type="button" class="btn btn-warning btn-small btn-cancel-source">cancel</button></td>';
      
      row.html(str_row);

      $("#tbl-sources tbody tr td input:eq(0)").focus();
      }
  }

  $("#btn-add-source").click(function () {
    if (!is_adding_or_editing_source) {
      is_adding_or_editing_source = true;
      $("#tbl-sources tbody").prepend('<tr><td><input type="text" id="name"></td><td><input type="text" id="url"></td><td><button type="button" class="btn btn-success btn-small btn-save-source">save</button> <button type="button" class="btn btn-warning btn-small btn-cancel-source">cancel</button></td></tr>');
      $("#tbl-sources tbody tr:first-child td:first-child input").focus();
    }
  });  

  $("#btn-suggested-sources").click(function () {
    $.ajax({
      url: '/reviews/planning/suggested_sources/',
      data: { 'review-id': $('#review-id').val() },
      cache: false,
      type: 'get',
      success: function (data) {
        $("#modal-suggested-sources table tbody").html(data);
        $("#modal-suggested-sources").before("<div class='shade'></div>");
        $("#modal-suggested-sources").slideDown(400, function () {
          $("body").addClass("modal-open");
        });
      }
    });
  });

  $("#checkbox-all-sources").click(function () {
    var is_checked = $(this).is(":checked");
    $("#tbl-suggested-sources tbody tr td input").prop("checked", is_checked);
  });

  $("#btn-save-suggested-sources").click(function () {
    var modal = $(this).closest('div.modal');
    $.ajax({
      url: '/reviews/planning/add_suggested_sources/',
      data: $('#form-suggested-sources').serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        $("#tbl-sources tbody").append(data);
        modal.slideUp(400, function () {
          $("#tbl-suggested-sources input").prop("checked", false);
          $(".shade").remove();
          $("body").removeClass("modal-open");
        });
      }
    });
  });

  $("table#tbl-sources tbody").on("click", ".btn-remove-source", removeSource);
  $("table#tbl-sources tbody").on("click", ".btn-edit-source", editSource);
  $("table#tbl-sources tbody").on("click", ".btn-save-source", saveSource);
  $("table#tbl-sources tbody").on("click", ".btn-cancel-source", cancelSource);

});