function displayFormMessage(ref, type, message) {
  var msg = ref.siblings('.form-status-message');
  if (type == "text-success") {
    msg.removeClass("text-error").addClass("text-success");
  }
  else {
    msg.removeClass("text-success").addClass("text-error");
  }
  msg.text(message);
  msg.fadeIn();
  window.setTimeout(function () {
    msg.fadeOut();
  }, 2000);
}