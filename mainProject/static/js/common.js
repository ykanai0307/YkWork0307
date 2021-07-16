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
    
    // auth select login
    $('#header').on('click','#login',function(){
        try {
            SubmitTarget('./','post');
        } catch(e) {
            alert("select change faild [" + e.message + "]");
        }
    });
    
    // logout
    $('#header').on('click','#logout',function(){
        try {
            SubmitTarget('logout','post');
        } catch(e) {
            alert("select change faild [" + e.message + "]");
        }
    });
});

// submit
function SubmitTarget(url,method){
  var formObject = document.getElementById('MainForm');
  if(url != null){
      formObject.action = url;
  }
  if(method == "get"){
      formObject.method = "get";
  }else{
      formObject.method = "post";
  }
  formObject.submit();
  formObject.action = "";
  return true;
}
