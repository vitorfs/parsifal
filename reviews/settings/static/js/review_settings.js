$(function () {
  $(".btn-save-settings").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/review_settings/save/',
      data: $("#review-settings-form").serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).disable();
      },
      success: function (data) {
        if (data != "") {
          location.href = data;
        }
      },
      complete: function () {
        $(btn).enable();
      }
    });
  });

  $("#btn-transfer-ownership").click(function () {
    $("#modal-transfer").open();
  });

  $("#btn-save-transfer").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/review_settings/transfer/',
      data: {
        'review-id': $("#review-id").val(),
        'transfer-user': $("#transfer-user").val(),
        'csrfmiddlewaretoken': $("#danger-zone-form input[name='csrfmiddlewaretoken']").val()
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).disable();
      },
      success: function (data) {
        if (data != "") {
          location.href = data;
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $("#modal-transfer p.text-error").text(jqXHR.responseText);
      },
      complete: function () {
        $(btn).enable();
      }
    });
  });
  
  $("#btn-delete-review").click(function () {

  });

});