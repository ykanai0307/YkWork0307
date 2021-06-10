function SubmitTarget(url="",type=""){
  var formObject = document.getElementById('MainForm');
  if(type != ""){
      formObject.enctype="multipart/form-data";
  }
  formObject.action = url;
  formObject.method = "post";
  formObject.submit();
  formObject.action = "";
}
function FileUpload(){
    var file = $("#FileAttach").prop('files')[0];
    $("#FileAttachName").text(file.name);
}