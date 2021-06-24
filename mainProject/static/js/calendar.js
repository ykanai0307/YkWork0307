// calendar(main)
$(function(){
    // global var
    var currentDate = '20210624';
    
    try {
        // 月初
        //var startDate = new Date(new Date().setDate(1));
        var startDate = new Date();
        startDate.setMonth(startDate.getMonth() + 1);
        startDate = new Date(startDate.setDate(1));
        
        // 月末
        var monthEnd = new Date();
        //monthEnd.setMonth(monthEnd.getMonth() + 1);
        monthEnd.setMonth(monthEnd.getMonth() + 2);
        endDate = new Date(monthEnd.setDate(0));
        
        var dateList = new Array();
        
        // 月単位の曜日
        for(var d = startDate; d <= endDate; d.setDate(d.getDate()+1)) {
          var dateData = d.getFullYear() + '-' + zeroPadding( (d.getMonth()+1) ,2) + '-' + zeroPadding( d.getDate() ,2);
          var dateArray = {
           date: dateData, 
           week: getWeekly()[d.getDay()],
           holiday: getHoliday(dateData)
          };
          dateList.push(dateArray);
        };
        
        //alert(dateList[0]["date"]);
    } catch(e) {
        alert("calendar get faild [" + e.message + "]");
    }
    
    // day click event
    $('#Calender').on('click','.DayList',function(e){
        try {
            var num = $('.DayList').index(this);
            var lbl = $('.DayList').eq(num).children('label');
            var pos = 0;
            pos = num % 7;
            var label = $('#Calender').find('label.Week')[pos];
            
            // select (year month date) set
            currentDate = $('#year')[0].innerText + zeroPadding(hankakuZenkaku($('#month')[0].innerText),2) + zeroPadding(lbl[0].textContent,2);
            
            // CalenderPopUp create
            let popUpHtml = CreatePopUp();
            
            // CalenderPopUp view set
            $('#CalenderPopUpView').html(popUpHtml);
            
            // Label to date
            $('#CalenderPopUp').find('label.day').text(zeroPadding( lbl[0].textContent ,2) + " " + label.innerText);
            
            // init(select) val set
            // TODO:[data:memo] (仮)後で取得方法かえる。29日が二つあると両方に設定される。なおす。
            for (let i=0; i < $('.param').length; i++) {
                var param = $('.param')[i].innerText.split(':');
                if(param[0] == currentDate){
                    $("input[name=\"PopUpMemo\"]").val(param[1]);
                }
            }
            
            // CalenderPopUp view position adjust
            $('#CalenderPopUp').offset({top: (window.pageYOffset + e.clientY) - 135, left: (window.pageXOffset + e.clientX) - 115});
            
            // CalenderPopUp view
            $('#CalenderPopUp').css('visibility','Visible');
        } catch(e) {
            alert("ppopup create faild [" + e.message + "]");
        }
    });
    
    // PopUp regist click event
    $('#CalenderPopUpView').on('click','#PopUpRegist',function(){
        try {
            postData = {};
            postData['Date'] = currentDate;
            postData['Memo'] = $("input[name=\"PopUpMemo\"]").val();
            
            // csrf_token (post)
            var csrf_token = getCookie("csrftoken");
            var url = "/mainProject/calendar_popup_click";
            post(url,postData,csrf_token);
        } catch(e) {
            alert("popup regist faild [" + e.message + "]");
        }
    });
});

// create popup
function CreatePopUp(){
    // CalenderPopUp create
    let popUpHtml = " <table id=\"CalenderPopUp\">";
    popUpHtml += "  <tr>";
    popUpHtml += "    <td class=\"day\"><label class=\"day\">17 tue</label><input type=\"button\" name=\"Close\" value=\"×\"/></td>";
    popUpHtml += "  </tr>";
    popUpHtml += "  <tr>";
    popUpHtml += "    <td class=\"memo\"><input type=\"text\" name=\"PopUpMemo\" placeholder=\"メモを入力\"/></td>";
    popUpHtml += "  </tr>";
    popUpHtml += "  <tr>";
    popUpHtml += "    <td class=\"button\"><input type=\"button\" name=\"PopUpRegist\" id=\"PopUpRegist\" value=\"REGIST\"/></td>";
    popUpHtml += "  </tr>";
    popUpHtml += " </table>";
    return popUpHtml;
}

// post(ajax)
function post(url,postData,csrf_token){
    $.ajax({
      'url':url,
      'type':'POST',
      'data':{
        'postData': postData,
        // 'postData': JSON.stringify(postData),
      },
      'dataType':'json',
      'beforeSend':function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrf_token);
          }
      },
      'success':function(response){
          alert(response.result);
      },
      'error':function(XMLHttpRequest, textStatus, errorThrown){
        alert("XMLHttpRequest : " + XMLHttpRequest.status + "/" + "errorThrown    : " + errorThrown.message );
      },
    });
    return false;
}

// holiday get
function getHoliday(fDate){
    var holiday = Holiday();
    var result = "";
    for (let i=0; i < holiday.length; i++) {
          if (new Date(fDate).getTime() == new Date(holiday[i]["date"]).getTime()){
              result = holiday[i]["name"];
          }
    }
    return result;
}

// Weekly get
function getWeekly(){
    return ["日","月","火","水","木","金","土"];
}

// 0padding(NUM=値,LEN=桁数)
function zeroPadding(num,len){
    return(Array(len).join("0")+num ).slice(-len);
}

// hankaku to zenkaku
function hankakuZenkaku(text){
    var hen = text.replace(/[Ａ-Ｚａ-ｚ０-９]/g,function(s){
        return String.fromCharCode(s.charCodeAt(0)-0xFEE0);
    });
    return hen;
}

// csrf_token get(django)
function getCookie( name ) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// csrf_token check
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}