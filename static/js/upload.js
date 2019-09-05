
$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
            "<tr><td><img src='" + data.result.url + "' style='max-width: 350px; max-height: 350px;'></td>\
            \<td><img src='" + data.result.output_url1 + "'style='max-width: 350px; max-height: 350px;'></td>" +
            "<td><img src='" + data.result.output_url2 + "'style='max-width: 350px; max-height: 350px;'></td></tr>"
        )
      }
    }
  });
});
