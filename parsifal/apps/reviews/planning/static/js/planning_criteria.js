$(function () {
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

  $(".btn-remove-criteria").click(function () {
    var select = $(this).attr("data-target");
    var ids = $(select).val();
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
  
});