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

  $("#confirm-deletion").click(function () {
    var button = $(this);
    var review_id = $("input#review-id").val();
    var source_id = $(this).attr("data-source-id");
    var row = $("#tbl-sources tr[source-id='" + source_id + "']");;
    $.ajax({
      url: '/reviews/planning/remove_source/',
      data: { 'review-id': review_id, 'source-id': source_id },
      type: 'get',
      cache: false,
      success: function(data) {
        $(row).remove();
      },
      complete: function () {
        $("#modal-confirm-source-deletion").modal('hide');
      }
    });
  });

  function editSource() {
    if (!is_adding_or_editing_source) {
      is_adding_or_editing_source = true;
      var button = $(this);
      var row = $(this).closest("tr");
      var name = $("td:eq(0)", row).text();
      var url = $("td:eq(1) a", row).text();
      source_editing_id = row.attr("source-id");
      source_editing_html = row.html();

      var str_row = '<td><input value="' + name + '" id="name" class="form-control"></td>';
      str_row += '<td><input value="' + url + '" id="url" class="form-control"></td>';
      str_row += '<td class="text-right"><button type="button" class="btn btn-success btn-sm btn-save-source"><span class="glyphicon glyphicon-ok"></span> save</button> <button type="button" class="btn btn-default btn-sm btn-cancel-source">cancel</button></td>';
      
      row.html(str_row);

      $("#tbl-sources tbody tr td input:eq(0)").focus();
      }
  }

  $("#btn-add-source").click(function () {
    if (!is_adding_or_editing_source) {
      is_adding_or_editing_source = true;
      $("#tbl-sources tbody").prepend('<tr><td><input type="text" id="name" class="form-control"></td><td><input type="text" id="url" class="form-control"></td><td class="text-right"><button type="button" class="btn btn-success btn-sm btn-save-source"><span class="glyphicon glyphicon-ok"></span> save</button> <button type="button" class="btn btn-default btn-sm btn-cancel-source">cancel</button></td></tr>');
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
    $.ajax({
      url: '/reviews/planning/add_suggested_sources/',
      data: $('#form-suggested-sources').serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        $("#tbl-sources tbody").append(data);
        $("#modal-suggested-sources").modal("hide");
        $("#tbl-suggested-sources input").prop("checked", false);
      }
    });
  });

  $("table#tbl-sources tbody").on("click", ".btn-edit-source", editSource);
  $("table#tbl-sources tbody").on("click", ".btn-save-source", saveSource);
  $("table#tbl-sources tbody").on("click", ".btn-cancel-source", cancelSource);

  $("table#tbl-sources tbody").on("click", ".js-start-remove", function () {
    var row = $(this).closest("tr");
    var source_id = $(row).attr("source-id");
    var name = $("td:eq(0)", row).text();
    $("#delete-source-name").text(name);
    $("#confirm-deletion").attr("data-source-id", source_id);
    $("#modal-confirm-source-deletion").modal('show');
  });

});