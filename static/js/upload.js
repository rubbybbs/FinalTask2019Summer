
$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      let stylesheet = 'max-width: 400px; max-height: 400px;'
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
            "<tr><td><img src='" + data.result.url + "' style="+stylesheet+"></td>\
            \<td><img src='" + data.result.output_url1 + "'style="+stylesheet+"></td>" +
            "<td><img src='" + data.result.output_url2 + "'style="+stylesheet+"></td></tr>"
        )
      }
    }
  });
});
