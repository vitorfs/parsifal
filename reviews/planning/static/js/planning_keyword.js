$(function () {

  function saveKeyword(keyword_id, old_description) {
    var description = $(".edit-keyword").val();
    $.ajax({
      url: '/reviews/planning/save_keyword/',
      data: { 'review-id': $("#review-id").val(), 'keyword-id': keyword_id, 'description': description },
      type: 'get',
      cache: false,
      success: function (data) {
        $(".edit-keyword").closest("td").html(data);
        $("#tbl-keywords td.keyword-row").bind("click", editKeyword);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        cancelEditKeyword(old_description);
      }
    });
  }

  function cancelEditKeyword(description) {
    $(".edit-keyword").closest("td").html(description);
    $("#tbl-keywords td.keyword-row").bind("click", editKeyword);
  }

  function editKeyword() {
    $("#tbl-keywords td.keyword-row").unbind("click");
    var description = $(this).text();
    var keyword_id = $(this).closest("tr").attr("keyword-id");
    $(this).html("<input type='text' value='" + description + "' class='edit-keyword form-control' maxlength='200'>");
    $(".edit-keyword").focus();

    $(".edit-keyword").blur(function () {
        if ($(this).val() == description) {
          cancelEditKeyword(description);
        }
        else {
          saveKeyword(keyword_id, description);  
        }
    });

    $(".edit-keyword").keyup(function (event) {
      if (event.keyCode == 13) {
        if ($(this).val() == description) {
          cancelEditKeyword(description);
        }
        else if ($(this).val() == "") {
          cancelEditKeyword(description);
        }
        else {
          saveKeyword(keyword_id, description);
        }
      } else if (event.keyCode == 27) {
        cancelEditKeyword(description);
      }
    });
  }
 
  function saveSynonym(synonym_id, old_description) {
    var btn = $(".edit-synonym").closest("ul").siblings(".add-synonym");
    var description = $(".edit-synonym").val();
    $.ajax({
      url: '/reviews/planning/save_synonym/',
      data: { 'review-id': $("#review-id").val(), 'synonym-id': synonym_id, 'description': description },
      type: 'get',
      cache: false,
      success: function (data) {
        if (data == "") {
          $(".edit-synonym").closest("li").remove();  
        }
        else {
          $(".edit-synonym").closest("li").html(data);
        }
        $("#tbl-keywords td ul li").unbind("click").bind("click", editSynonym);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        cancelEditSynonym(old_description);
      },
      complete: function () {
        btn.show();
      }
    });    
  }

  function cancelEditSynonym(description) {
    var btn = $(".edit-synonym").closest("ul").siblings(".add-synonym");
    $(".edit-synonym").closest("li").html(description);
    $("#tbl-keywords td ul li").bind("click", editSynonym);
    $(this).closest("ul").siblings(".add-synonym").show();
    btn.show();
  }

  function editSynonym() {
    $("#tbl-keywords td ul li").unbind("click");
    var btn_add_synonym = $(this).closest("ul").siblings(".add-synonym");
    btn_add_synonym.hide();
    var description = $(this).text();
    var synonym_id = $(this).attr("synonym-id");
    $(this).html("<input type='text' value='" + description + "' class='edit-synonym form-control' maxlength='200'>");
    $(".edit-synonym").focus();
    $(".edit-synonym").blur(function () {
      if (description != $(".edit-synonym").val()) {
        saveSynonym(synonym_id, description);
      }
      else {
        cancelEditSynonym(description);
      }
    });
    $(".edit-synonym").keyup(function (event) {
      if (event.keyCode == 13) {
        saveSynonym(synonym_id, description);
      } else if (event.keyCode == 27) {
        cancelEditSynonym(description);
      }
    });
  }

  $("#tbl-keywords td ul li").click(editSynonym);

  $("#import-pico-keywords").click(function () {
    $.ajax({
      url: '/reviews/planning/import_pico_keywords/',
      data: { 'review-id': $('#review-id').val() },
      cache: false,
      type: 'get',
      success: function (data) {
        $("#tbl-keywords tbody").append(data);
        $("#tbl-keywords td.keyword-row").unbind("click").bind("click", editKeyword);
      }
    });
  });

  function removeKeyword() {
    var row = $(this).closest("tr");
    keyword_id = row.attr("keyword-id");
    $.ajax({
      url: '/reviews/planning/remove_keyword/',
      data: {'review-id': $('#review-id').val(), 'keyword-id': keyword_id },
      type: 'get',
      cache: false,
      success: function (data) {
        row.remove();
      }
    });
  }

  function saveNewKeyword() {
    var review_id = $("#review-id").val();
    var description = $("#input-add-keyword").val();
    $.ajax({
      url: '/reviews/planning/add_new_keyword/',
      data: { 'review-id': review_id, 'description': description },
      cache: false,
      type: 'get',
      success: function (data) {
        $("#tbl-keywords tbody tr:eq(0)").remove();
        $("#tbl-keywords tbody").prepend(data);
        $("#tbl-keywords td.keyword-row").unbind("click").bind("click", editKeyword);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $("#tbl-keywords tbody tr:eq(0)").remove();
      }
    });
  }

  function cancelNewKeyword() {
    $("#tbl-keywords tbody tr:eq(0)").remove();
  }

  $.fn.addKeywordSettings = function () {
    $(this).keyup(function (event) {
      if (event.keyCode == 13) {
        if ($("#input-add-keyword").val() != "") {
          saveNewKeyword();  
        }
        else {
          cancelNewKeyword();
        }
      } else if (event.keyCode == 27) {
        cancelNewKeyword();
      }
    });
    
    $(this).blur(cancelNewKeyword);
  };

  $("#add-keyword").click(function () {
    $.ajax({
      url: '/reviews/planning/new_keyword/',
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

  $("#tbl-keywords td.keyword-row").click(editKeyword);

  $("table#tbl-keywords tbody").on("click", ".btn-remove-keyword", removeKeyword);
  $("table#tbl-keywords tbody").on("keyup", ".add-synonym", function (event) {
    if (event.keyCode == 13) {
      var synonym = $(this).val();
      if (synonym != "") {
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
            $("#tbl-keywords td ul li").unbind("click").bind("click", editSynonym);
          }
        });        
      }
    }
  });

});