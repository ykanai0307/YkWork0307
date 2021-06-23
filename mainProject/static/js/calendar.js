// calendar get(main)
$(function(){
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
    
    // day click
    $('.DayList').click(function(e) {
        var num = $('.DayList').index(this);
        var lbl = $('.DayList').eq(num).children('label');
        var pos = 0;
        pos = num % 7;
        var label = $('#Calender').find('label.Week')[pos];
        // TODO 表示位置の調整を行う。
        //$('#CalenderPopUp').offset({top: (e.clientY - 130), left: (e.clientX - 80)});
        //alert(window.pageYOffset);
        //alert(e.clientY);
        $('#CalenderPopUp').offset({top: (window.pageYOffset + e.clientY) - 135, left: (window.pageXOffset + e.clientX) - 115});
        
        $('#CalenderPopUp').find('label.day').text(zeroPadding( lbl[0].textContent ,2) + " " + label.innerText);
        $('#CalenderPopUp').css('visibility','Visible');
        
        
        //postData = {};
        //postData['part'] = lbl[0].textContent;
        
        // csrf_token (post)
        //var csrf_token = getCookie("csrftoken");
        //var url = "/mainProject/calendar_popup_click";
        //post(url,postData,csrf_token);
        
    });
});

// post(ajax)
function post(url,postData,csrf_token){
    $.ajax({
      'url':url,
      'type':'POST',
      'data':{
        'postData': JSON.stringify(postData),
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
function zeroPadding(NUM, LEN){
    return ( Array(LEN).join('0') + NUM ).slice( -LEN );
}

// csrf_token get(django)
function getCookie(name) {
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