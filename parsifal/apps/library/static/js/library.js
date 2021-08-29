$(function () {

  'use strict';

  $(".js-jump-page").popover({
    html: true,
    content: function () {
      var first_page = "?p=1";
      var last_page_number = $("#library-documents").attr("data-num-pages");
      var last_page = "?p=" + last_page_number;

      var querystring = $("#search-form [name='q']").val();
      if (querystring.length > 0) {
        first_page += "&q=" + querystring;
        last_page += "&q=" + querystring;
      }

      var html = "<div><small><a href='" + first_page + "'>First page</a></small></div>";
      html += "<div><small><a href='" + last_page + "'>Last page</a></small></div>";
      return html;
    }
  });

  var hideAllSelectionMessages = function () {
    $(".js-message-select-all-pages").hide();
    $(".js-message-clear-selection").hide();
  };

  var showSelectAllPagesMessage = function () {
    hideAllSelectionMessages();
    $(".js-message-select-all-pages").show();
  };

  var showClearSelectionMessage = function () {
    hideAllSelectionMessages();
    $(".js-message-clear-selection").show();
  };

  var clearSelection = function () {
    $("#library-documents .js-document-checkbox").each(function () {
      $(this).unselectDocument();
    });
    $(".js-toggle-select-documents .glyphicon").removeClass().addClass("glyphicon glyphicon-unchecked");
    $(".select-all-pages").val("");
    hideAllSelectionMessages();
    modifyToolbarButtonsState();
  };

  var selectAllInPage = function () {
    var hasAtLeastOneDocument = $("#library-documents .js-document-checkbox").length > 0;
    if (hasAtLeastOneDocument) {
      $("#library-documents .js-document-checkbox").each(function () {
        $(this).selectDocument();
      });
      $(".js-toggle-select-documents .glyphicon").removeClass().addClass("glyphicon glyphicon-check");
      $(".select-all-pages").val("");
      showSelectAllPagesMessage();
      modifyToolbarButtonsState();
    }
  };

  $(".js-toggle-select-documents").click(function () {
    var isChecked = $(".glyphicon", this).hasClass("glyphicon-check");
    if (isChecked) {
      clearSelection();
    }
    else {
      selectAllInPage();
    }
  });

  $(".js-select-all-documents-in-page").click(function () {
    selectAllInPage();
  });

  $(".js-select-all-documents").click(function () {
    showClearSelectionMessage();
    $("#select-all-pages").val("all");
  });

  $(".js-clear-selection").click(function () {
    clearSelection();
  });

  $.fn.selectDocument = function () {
    var row = $(this).closest("tr");
    var checkbox = $("input[type='checkbox']", this);
    var icon = $(".glyphicon", this);

    $(checkbox).prop("checked", true);
    $(icon).removeClass().addClass("glyphicon glyphicon-check");
    $(row).addClass("bg-warning");
  };

  $.fn.unselectDocument = function () {
    var row = $(this).closest("tr");
    var checkbox = $("input[type='checkbox']", this);
    var icon = $(".glyphicon", this);

    $(checkbox).prop("checked", false);
    $(icon).removeClass().addClass("glyphicon glyphicon-unchecked");
    $(row).removeClass("bg-warning");
  };

  $(".js-document-checkbox").click(function () {
    var checkbox = $("input[type='checkbox']", this);
    var isChecked = $(checkbox).is(":checked");

    if (isChecked) {
      $(this).unselectDocument();
      $(".select-all-pages").val("");
      hideAllSelectionMessages();
    }
    else {
      $(this).selectDocument();
    }
    modifyToolbarButtonsState();
    modifySelectAllCheckboxState();
  });

  var modifySelectAllCheckboxState = function () {
    // Ensure the integrity of the check all button icon
    var totalDocumentsInThisPage = parseInt($("#library-documents").attr("data-num-documents"));
    var selectedDocuments = $("[name='document']:checked").length;
    var allDocumentsInThisPageAreSelected = (selectedDocuments === totalDocumentsInThisPage);

    if (allDocumentsInThisPageAreSelected) {
      $(".js-toggle-select-documents .glyphicon").removeClass().addClass("glyphicon glyphicon-check");
    }
    else {
      $(".js-toggle-select-documents .glyphicon").removeClass().addClass("glyphicon glyphicon-unchecked");
    }
  };

  var modifyToolbarButtonsState = function () {
    // Ensure the integrity of the delete and move buttons disabled state
    var selectedDocuments = $("[name='document']:checked").length;
    var atLeastOneDocumentIsSelected = (selectedDocuments > 0);

    if (atLeastOneDocumentIsSelected) {
      $(".js-selection-action").prop("disabled", false);
      $(".js-selection-action").closest(".btn-group").removeClass("not-allowed");      
    }
    else {
      $(".js-selection-action").prop("disabled", true);
      $(".js-selection-action").closest(".btn-group").addClass("not-allowed");
    }
  };

  /* Folder Management */

  var clearNewFolderFormState = function () {
    $(".js-add-folder-input").hide();
    $(".js-add-folder").show();
    $("#form-new-folder .form-group").removeClass().addClass("form-group has-feedback");
    $("#form-new-folder .form-control-feedback").removeClass().addClass("form-control-feedback")
    $("#form-new-folder .form-control-feedback").hide();
    $("#form-new-folder .errors").html("");
    $("#form-new-folder #id_name").val("");
  };

  $(".js-add-folder").click(function () {
    $(".js-add-folder").fadeOut(100, function () {
      $(".js-add-folder-input").fadeIn(100, function () {
        $(".js-add-folder-input #id_name").focus();
      });
    })
  });

  $(".js-add-shared-folder").click(function () {
    $(".js-add-shared-folder").fadeOut(100, function () {
      $(".js-add-shared-folder-input").fadeIn(100, function () {
        $(".js-add-shared-folder-input #id_name").focus();
      });
    });
  });

  $("#form-new-folder").submit(function () {
    var form = $(this);
    $.ajax({
      url: $(form).attr("action"),
      data: $(form).serialize(),
      type: $(form).attr("method"),
      cache: false,
      beforeSend: function () {
        $("#form-new-folder .form-group").removeClass().addClass("form-group has-feedback");
        $("#form-new-folder .form-control-feedback").removeClass().addClass("glyphicon glyphicon-refresh spin form-control-feedback");
        $("#form-new-folder #id_name").prop("readonly", true);
      },
      success: function (data) {
        $("#form-new-folder .form-group").removeClass().addClass("form-group has-feedback has-success");
        $("#form-new-folder .form-control-feedback").removeClass().addClass("glyphicon glyphicon-ok form-control-feedback");
        $("#form-new-folder .form-control-feedback").show();
        setTimeout(function () {
          $(".js-add-folder").before("<a href='/library/folders/" + data.folder.slug + "/' class='list-group-item'>" + data.folder.name + "</a>");
          clearNewFolderFormState();
        }, 200);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $("#form-new-folder .form-group").removeClass().addClass("form-group has-feedback has-error");
        $("#form-new-folder .form-control-feedback").removeClass().addClass("glyphicon glyphicon-remove form-control-feedback");
        $("#form-new-folder .form-control-feedback").show();
        $("#form-new-folder .errors").html("");
        jqXHR.responseJSON.name.forEach(function (error) {
          $("#form-new-folder .errors").append("<span class='help-block' style='margin-bottom: 0;'><small>" + error + "</small></span>");
        });
      },
      complete: function () {
        $("#form-new-folder #id_name").prop("readonly", false);
      }
    });
    return false;
  });

  $("#form-new-folder #id_name").blur(function () {
    var isEmpty = ($(this).val().trim().length === 0);
    if (isEmpty) {
      clearNewFolderFormState();
    }
  });

  
  $("#form-new-folder #id_name").keyup(function(e) {
    var KEYCODE_ESC = 27;
    if (e.keyCode == KEYCODE_ESC) {
      clearNewFolderFormState();
    }
  });

  $(".js-new-document").click(function () {
    var url = $("#modal-document").attr("data-remote-url");
    $.ajax({
      url: url,
      success: function (data) {
        $("#modal-document .modal-dialog").html(data.html);
      }
    });
    $("#modal-document").modal('show');
  });

  $("#modal-document").on("shown.bs.modal", function () {
    $("#modal-document textarea").expanding();
  });

  $("#modal-document").on("click", ".js-save-new-document", function () {
    var form = $("#form-new-document");
    $.ajax({
      url: $(form).attr("action"),
      data: $(form).serialize(),
      type: $(form).attr("method"),
      success: function (data) {
        if (data.status === 'success') {
          location.href = data.redirect_to;
        }
        else {
          $("#modal-document .modal-dialog").html(data.html);
        }
      }
    });
  });

  $(".js-document-details a").click(function (e) {
    e.stopPropagation();
  });

  $(".js-document-details").click(function () {
    var document_id = $(this).closest("tr").attr("data-id");
    var url = "/library/documents/" + document_id + "/";
    $.ajax({
      url: url,
      success: function (data) {
        $("#modal-document .modal-dialog").html(data.html);
      }
    });
    $("#modal-document").modal('show');
  });

  $("#modal-document").on("click", ".js-save-document", function () {
    var form = $("#form-document");
    var document_id = $(form).attr("data-document-id");
    $.ajax({
      url: $(form).attr("action"),
      data: $(form).serialize(),
      type: $(form).attr("method"),
      success: function (data) {
        if (data.status === 'success') {
          $("#library-documents tr[data-id='" + document_id + "'] td.js-document-details").html(data.html);
          $("#modal-document").modal('hide');
        }
        else {
          $("#modal-document .modal-dialog").html(data.html);
        }
      }
    });
  });

  $(".js-move-to").click(function () {
    var to_folder_id = $(this).attr("data-to-folder-id");
    $("#library-action").val("move");
    $("#action-folder-id").val(to_folder_id);
    $("#form-library").submit();
  });

  $(".js-copy-to").click(function () {
    var to_folder_id = $(this).attr("data-to-folder-id");
    $("#library-action").val("copy");
    $("#action-folder-id").val(to_folder_id);
    $("#form-library").submit();
  });

  $(".js-remove-from-folder").click(function () {
    $("#library-action").val("remove_from_folder");
    $("#form-library").submit();
  });

  $(".js-delete-completely").click(function () {
    $("#library-action").val("delete_documents");
    $("#form-library").submit();
  });

  $(".js-import-bibtex").click(function () {
    $("#input-bibtex").click();
  });

  $("#input-bibtex").change(function () {
    var form = $(this).closest("form");
    $(form).submit();
  });

});
