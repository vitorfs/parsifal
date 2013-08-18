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

  function saveQuestion() {
    var btn = $(this);
    var form = $(this).closest("form");
    $.ajax({
      url: '/reviews/planning/save_question/',
      data: form.serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
      },
      error: function () {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-success").addClass("text-error");
        msg.text('Something went wrong! Please contact the administrator.');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      },
      success: function(data) {
        $("input[name='question-id']", form).val(data);
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-error").addClass("text-success");
        msg.text('Your question have been saved successfully!');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      },
      complete: function () {
      }
    });
  }

  function removeQuestion() {
    var form = $(this).closest("form");
    $(form).closest("div.question").fadeOut();
    var question_id = $("input[name='question-id']", form).val();
    if (question_id != 'None') {
      $.ajax({
        url: '/reviews/planning/remove_question/',
        data: form.serialize(),
        type: 'post',
        cache: false,
        success: function (data) {

        }
      });
    }
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
  $(".btn-save-question").click(saveQuestion);
  $(".btn-remove-question").click(removeQuestion);

  $("#btn-add-sec-question").click(function () {
    $.ajax({
      url: '/reviews/planning/add_question/',
      data: { 'review-id': $('#review-id').val() },
      type: 'get',
      cache: false,
      success: function (data) {
        $('.questions-containers').append(data);
        $('html, body').animate({
            scrollTop: ($(".questions-containers .question:last-child").offset().top - 90)
        }, 1000);
        $('.btn-save-question').unbind('click').bind('click', saveQuestion);
        $('.btn-remove-question').unbind('click').bind('click', removeQuestion);
      }
    });
  });

  function addCriteria(criteria, type, input, select_list) {
    var review_id = $('#review-id').val();
    $.ajax({
      url: '/reviews/planning/add_criteria/',
      data: { 
        'criteria': criteria, 
        'review-id': review_id,
        'criteria-type': type
      },
      type: 'get',
      cache: false,
      success: function (data) {
        select_list.prepend(data);
        input.val("");
        input.focus();
      }
    });
  }

  $("input#input-inclusion").keyup(function (event) {
    if (event.keyCode == 13) {
      var criteria = $(this).val();
      if (criteria != ""){
        addCriteria(criteria, 'I', $("input#input-inclusion"), $("#inclusion-criteria"));
      }
    }
  });

  $("input#input-exclusion").keyup(function (event) {
    if (event.keyCode == 13) {
      var criteria = $(this).val();
      if (criteria != ""){
        addCriteria(criteria, 'E', $("input#input-exclusion"), $("#exclusion-criteria"));
      }
    }
  });

  $(".btn-save-objective").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/reviews/planning/save_objective/',
      data: $('#form-objective').serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        var msg = btn.siblings('.form-status-message');
        msg.removeClass("text-error").addClass("text-success");
        msg.text('Your review have been saved successfully!');
        msg.fadeIn();
        window.setTimeout(function () {
          msg.fadeOut();
        }, 2000);
      }
    });
  });

  $(".btn-remove-criteria").click(function () {
    var select = $(this).siblings("select");
    var ids = select.val();
    if (ids != null) {
      var review_id = $('#review-id').val();
      var str_ids = "";
      var i;
      for (i = 0 ; i < ids.length ; i++) {
        if (i == 0) {
          str_ids += ids[i];  
        }
        else {
          str_ids += "," + ids[i];
        }
      }
      $.ajax({
        url: '/reviews/planning/remove_criteria/',
        data: { 'review-id': review_id,  'criteria-ids': str_ids },
        type: 'get',
        cache: false,
        success: function (data) {
          $("option:selected", select).remove();
        }
      });
    }
  });

  $(".add-synonym").keyup(function (event) {
    if (event.keyCode == 13) {
      $(this).closest("ul").prepend("<li>" + $(this).val() + "</li>");
      $(this).val("");
      $(this).focus();
    }
  });

});