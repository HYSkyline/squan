$("#avatarimg").on("change", function(e) {

  var file = e.target.files[0]; //获取图片资源

  // 只选择图片文件
  if (!file.type.match('image.*')) {
    return false;
  }

  var reader = new FileReader();

  reader.readAsDataURL(file); // 读取文件

  // 渲染文件
  reader.onload = function(arg) {
    var img = '<label class="control-label" for="avatarimg"><img class="preview" src="' + arg.target.result + '" alt="preview" /></label>';
    var commitLabel = '<label class="control-label" for="avatarimg" id="avatarimgCommit">上传头像</label>'
    $("#avatarPreview").empty().append(img);
    $("#avatarLabel").empty();
  }
});
