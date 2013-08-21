$(function () {
  $.fn.bindAddSynonym = function () {
    $(this).keyup(function (event) {
      if (event.keyCode == 13) {
        var synonym = $(this).val();
        var keyword_id = $(this).closest("tr").attr("keyword-id");
        var review_id = $("#review-id").val();
        var input = $(this);
        $.ajax({
          url: '/reviews/planning/add_synonym/',
          data: { 'review-id': review_id, 'keyword-id': keyword_id, 'synonym': synonym },
          cache: false,
          type: 'get',
          success: function (data) {
            input.siblings("ul").append(data);
            input.val("");
            input.focus();
          }
        });
      }
    });
  };

  $(".add-synonym").bindAddSynonym();

  function saveKeyword() {
    var value = $(".edit-keyword").val();
    $(".edit-keyword").closest("td").html(value);
    $("#tbl-keywords td.keyword-row").bind("click", editKeyword);
  }

  function cancelEditKeyword(description) {
    $(".edit-keyword").closest("td").html(description);
    $("#tbl-keywords td.keyword-row").bind("click", editKeyword);
  }

  function editKeyword() {
    $("#tbl-keywords td.keyword-row").unbind("click");
    var description = $(this).text();
    var keyword_id = $(this).closest("tr").attr("keyword-id");
    $(this).html("<input type='text' value='" + description + "' class='edit-keyword'>");
    $(".edit-keyword").focus();
    $(".edit-keyword").blur(saveKeyword);
    $(".edit-keyword").keyup(function (event) {
      if (event.keyCode == 13) {
        saveKeyword();
      } else if (event.keyCode == 27) {
        cancelEditKeyword(description);
      }
    });
  }

  $("#tbl-keywords td.keyword-row").click(editKeyword);

  $("#import-pico-keywords").click(function () {
    $.ajax({
      url: '/reviews/planning/import_pico_keywords/',
      data: { 'review-id': $('#review-id').val() },
      cache: false,
      type: 'get',
      success: function (data) {
        $("#tbl-keywords tbody").append(data);
        $(".add-synonym").unbind("keyup");
        $(".add-synonym").bindAddSynonym();
        $(".btn-remove-keyword").unbind("click").bind("click", removeKeyword);
        $("#tbl-keywords td.keyword-row").unbind("click").bind("click", editKeyword);
      }
    });
  });

  function removeKeyword() {
    var row = $(this).closest("tr");
    keyword_id = row.attr("keyword-id");
    $.ajax({
      url: '/reviews/planning/remove_keyword/',
      data: {'review_id': $('#review-id').val(), 'keyword_id': keyword_id },
      type: 'get',
      cache: false,
      success: function (data) {
        if (data != "ERROR"){
          row.remove();
        }
      }
    });
  }

  $(".btn-remove-keyword").click(removeKeyword);

});