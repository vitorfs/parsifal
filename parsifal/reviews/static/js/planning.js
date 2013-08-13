$(function () {

  function addSource() {
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
      },
      error: function (jqXHR, textStatus, errorThrown) {

      },
      complete: function () {

      }
    });
  }

  $("#btn-add-source").click(function () {
    $("#tbl-sources tbody").prepend('<tr><td><input type="text" id="name"></td><td><input type="text" id="url"></td><td><button type="button" class="btn btn-success btn-small btn-save-source">save</button> <button type="button" class="btn btn-warning btn-small">cancel</button></tr>');
    $("#tbl-sources tbody tr:first-child td:first-child input").focus();
    $(".btn-save-source").unbind("click").bind("click", addSource);
  });  

  $("#btn-suggested-sources").click(function () {
    $("#modal-suggested-sources").slideDown();
  });

  $(".btn-remove-source").click(function () {
    var row = $(this).closest("tr");
    row.remove();
  });
});