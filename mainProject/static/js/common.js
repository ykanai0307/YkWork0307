//ready
$(function(){
    // menu click
    $('#hamburger-menu').on('click','#menu-btn-check',function(){
        try {
          var visibility = $('#Menu').css('visibility');
          if(visibility == 'visible'){
              $('#Menu').css('visibility','hidden');
          }else{
              $('#Menu').css('visibility','visible');
          }
        } catch(e) {
            alert("popup regist faild [" + e.message + "]");
        }
    });
});

$(window).on('load',function(){
    // submit
    function SubmitTarget(url,type,method){
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
});