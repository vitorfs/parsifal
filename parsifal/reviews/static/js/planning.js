$(function () {
  $("#btn-add-source").click(function () {
    $("#tbl-sources tbody").prepend('<tr><td><input type="text" id="name"></td><td><input type="text" id="url"></td><td><button type="button" class="btn btn-success btn-small">save</button> <button type="button" class="btn btn-warning btn-small">cancel</button></tr>');
    $("#tbl-sources tbody tr:first-child td:first-child input").focus();
  });  

  $("#btn-suggested-sources").click(function () {
    $("#modal-suggested-sources").slideDown();
  });
});