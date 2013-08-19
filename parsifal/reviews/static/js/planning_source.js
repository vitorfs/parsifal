$(function () {
  var is_adding_source = false;

  function saveSource() {
    var name = $("input#name").val();
    var url = $("input#url").val();
    var id = $("input#review-id").val();

    $.ajax({
      url: '/reviews/planning/add_source/',
      data: { name: name, url: url, id: id },
      type: 'get',
      cache: false,
      beforeSend: function () {

      },
      success: function(data, textStatus, jqXHR) {
        $("#tbl-sources tbody tr:first-child").remove();
        $("#tbl-sources tbody").prepend(data);
        $(".btn-remove-source").unbind("click").bind("click", removeSource);
      },
      error: function (jqXHR, textStatus, errorThrown) {

      },
      complete: function () {
        is_adding_source = false;
      }
    });
  }

  function cancelSource() {
    $("#tbl-sources tbody tr:first-child").remove();
    is_adding_source = false;
  }

  function removeSource() {
    var button = $(this);
    var row = $(this).closest("tr");
    review_id = $("input#review-id").val();
    source_id = row.attr("source-id");
    $.ajax({
      url: '/reviews/planning/remove_source/',
      data: { review_id: review_id, source_id: source_id },
      type: 'get',
      cache: false,
      beforeSend: function () {
        button.html("removing…");
        button.attr("disabled", true);
      },
      error: function () {
        button.html("remove");
        button.attr("disabled", false);
      },
      success: function(data) {
        row.remove();
      },
      complete: function () {
        
      }
    });
  }

  $("#btn-add-source").click(function () {
    if (!is_adding_source) {
      is_adding_source = true;
      $("#tbl-sources tbody").prepend('<tr><td><input type="text" id="name"></td><td><input type="text" id="url"></td><td><button type="button" class="btn btn-success btn-small btn-save-source">save</button> <button type="button" class="btn btn-warning btn-small btn-cancel-source">cancel</button></tr>');
      $("#tbl-sources tbody tr:first-child td:first-child input").focus();
      $(".btn-save-source").unbind("click").bind("click", saveSource);
      $(".btn-cancel-source").unbind("click").bind("click", cancelSource);
    }
  });  

  $("#btn-suggested-sources").click(function () {
    $("#modal-suggested-sources").slideDown();
  });

  $(".btn-remove-source").click(removeSource);
});