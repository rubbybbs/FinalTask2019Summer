
$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
          // "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
            "<tr><td><img src='" + data.result.url + "' style='max-width: 400px; max-height: 400px;'></td>\
            \<td><img src='" + data.result.output_url + "'style='max-width: 400px; max-height: 400px;'></td></tr>"
        )
      }
    }
  });

});
