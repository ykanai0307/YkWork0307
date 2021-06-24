function SubmitTarget(url="",type="",method=""){
  var formObject = document.getElementById('MainForm');
  if(type != ""){
      formObject.enctype="multipart/form-data";
  }
  formObject.action = url;
  if(method == "get"){
      formObject.method = "get";
  }else{
      formObject.method = "post";
  }
  formObject.submit();
  formObject.action = "";
}
function FileUpload(){
    var file = $("#FileAttach").prop('files')[0];
    $("#FileAttachName").text(file.name);
}