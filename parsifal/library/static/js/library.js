$(function () {

  'use strict';

  $(".js-jump-page").popover({
    html: true,
    content: function () {
      var last_page = $("#library-documents").attr("data-num-pages");
      var html = "<div><small><a href='?page=1'>First page</a></small></div>";
      html += "<div><small><a href='?page=" + last_page + "'>Last page</a></small></div>";
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
    $("#library-documents .js-document-checkbox").each(function () {
      $(this).selectDocument();
    });
    $(".js-toggle-select-documents .glyphicon").removeClass().addClass("glyphicon glyphicon-check");
    $(".select-all-pages").val("");
    showSelectAllPagesMessage();
    modifyToolbarButtonsState();
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
    $(".select-all-pages").val("all");
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
    }
    else {
      $(".js-selection-action").prop("disabled", true);
    }
  };

  /* Folder Management */

  $(".js-add-folder").click(function () {
    var url = $(this).attr("data-remote-url");
    //$("#modal-add-folder .modal-body").load(url);
  });

  $("#form-add-folder").submit(function () {
    var form = $(this);
    var submitButton = $("button[type='submit']", form);
    $.ajax({
      url: $(form).attr("action"),
      data: $(form).serialize(),
      type: $(form).attr("method"),
      cache: false,
      beforeSend: function () {
        $(submitButton).ajaxDisable();
      },
      success: function (data) {
        $("#modal-add-folder .modal-body").html(data)
      },
      error: function () {

      },
      complete: function () {
        $(submitButton).ajaxEnable();
      }
    });
    return false;
  });

});
