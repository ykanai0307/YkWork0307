// calendar(main)
$(function(){
    // global var
    var currentDate = '20210624';
    var currentDateTime = "";
    var responseResult;
    
    var initCarendarPopUpTop = 0;
    var scroll = 0;
    
    try {
        var startDate = MonthStartGet(0,1);    // MonthStartate
        var endDate = MonthEndGet(1,0);        // MonthEndDate
        dateList = DayList(startDate,endDate); // Day list create
        
        //alert(dateList[0]["date"]);
    } catch(e) {
        alert("this month get faild [" + e.message + "]");
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
            var lblTmp = lbl[0].innerText.split('\n');
            currentDateTime = new Date(hankakuZenkaku($('#year')[0].innerText).toString(), zeroPadding(hankakuZenkaku($('#month')[0].innerText),2).toString(), zeroPadding(hankakuZenkaku(lblTmp[0]),2).toString(), "01", "01", "01");
            var monthCateg = lbl[0].classList[1].split('_');
            if(monthCateg[0] == "LastMonth"){
                currentDateTime.setMonth(currentDateTime.getMonth()-1);
            }
            currentDateTime = new Date(currentDateTime.setDate(zeroPadding(lblTmp[0],2).toString()));
            currentDate = 'YYYY-MM-DD';
            currentDate = currentDate.replace(/YYYY/g, currentDateTime.getFullYear());
            currentDate = currentDate.replace(/MM/g, zeroPadding(currentDateTime.getMonth(),2));
            currentDate = currentDate.replace(/DD/g, zeroPadding(currentDateTime.getDate(),2));
            
            if(lblTmp.length > 0 && lblTmp[0] == ""){
                return true;
            }
            
            // CalenderPopUp create
            let popUpHtml = CreatePopUp();
            
            // CalenderPopUp view set
            $('#CalenderPopUpView').html(popUpHtml);
            
            // Label to date
            var holidayLabel = "";
            if(lblTmp.length > 1){
                holidayLabel = '\n' + lblTmp[1];
            }
            $('#CalenderPopUp').find('label.day').text(zeroPadding( lblTmp[0] ,2) + " " + label.innerText + " " + holidayLabel);
            
            // init(select) val set
            postData = {};
            postData['Mode'] = "Set";
            postData['Date'] = currentDate;
            var url = "/mainProject/calendar_popup_click";
            responseResult = post(url,false,postData,"Set",getCookie("csrftoken"));
            
            // date compare
            if( ( responseResult.length > 0 ) && ( responseResult[0].length > 0 ) && ( responseResult[0][0].length > 0 ) ){
                let date1 = new Date(responseResult[0][0][0]);
                let date2 = new Date(currentDate + " 01:01:01");
                if(date1.getTime() == date2.getTime()){
                    $("input[name=\"PopUpMemo\"]").val(responseResult[0][0][1]);
                }
            }
            
            // CalenderPopUp view position adjust
            initCarendarPopUpTop = (window.pageYOffset + e.clientY) - 135;
            $('#CalenderPopUp').offset({top: initCarendarPopUpTop, left: (window.pageXOffset + e.clientX) - 115});
            
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
            postData['Mode'] = "Regist";
            postData['Date'] = currentDate;
            postData['Memo'] = $("input[name=\"PopUpMemo\"]").val();
            
            // csrf_token (post)
            var csrf_token = getCookie("csrftoken");
            var url = "/mainProject/calendar_popup_click";
            post(url,true,postData,"Regist",csrf_token);
        } catch(e) {
            alert("popup regist faild [" + e.message + "]");
        }
    });
    
    // popup position fix
    $(window).scroll(function(e) {
      try {
          scroll = $(this).scrollTop();
          $('#CalenderPopUp').offset({top: initCarendarPopUpTop});
      } catch(e) {
          alert("scroll pos get faild [" + e.message + "]");
      }
    });
    
    $('#Calender').on('click','#LastMonth',function(e){
      var dateList = new Array();
      try {
        var startDate = MonthStartGet(-1,1);   // MonthStartate
        var endDate = MonthEndGet(0,0);        // MonthEndDate
        dateList = DayList(startDate,endDate); // Day list create
      } catch(e) {
          alert("LastMonth click faild [" + e.message + "]");
      }
    });
});

// MonthStartDate
function MonthStartGet(duration,addDate){
    var startDate = false;
    try {
        var dateVal = new Date();
        dateVal.setMonth(dateVal.getMonth() + duration);
        startDate = new Date(dateVal.setDate(addDate));
    } catch(e) {
        alert("MonthStartGet get faild [" + e.message + "]");
    }
    return startDate;
}

// MonthEndDate
function MonthEndGet(duration,addDate){
    var endDate = false;
    try {
        var dateVal = new Date();
        dateVal.setMonth(dateVal.getMonth() + duration);
        endDate = new Date(dateVal.setDate(addDate));
    } catch(e) {
        alert("MonthEndGet get faild [" + e.message + "]");
    }
    return endDate;
}

// Day list create
function DayList(startDate,endDate){
    var dateList = new Array();
    try {
        for(var d = startDate; d <= endDate; d.setDate(d.getDate()+1)) {
            var dateData = d.getFullYear() + '-' + zeroPadding( (d.getMonth()+1) ,2) + '-' + zeroPadding( d.getDate() ,2);
            var dateArray = {
               date: dateData, 
               week: getWeekly()[d.getDay()],
               holiday: getHoliday(dateData)
            };
            dateList.push(dateArray);
        };
    } catch(e) {
        alert("DayList create faild [" + e.message + "]");
    }
    return dateList;
}

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
function post(url,async,postData,status,csrf_token){
    $.ajax({
      'url':url,
      'async': async,
      'type':'POST',
      'data':{
        'postData': postData,
        // 'postData': JSON.stringify(postData),
      },
      'dataType':'json',
      'beforeSend':function(xhr, settings) { // for django csrf token(start)
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrf_token);
          }
      }, // for django csrf token(end)
      'success':function(response){
          switch (status) {
            case "Regist":
              OnSuccess(response);
              break;
            case "Set":
              OnSet(response);
              break;
            default:
              OnSuccess(response);
              break;
          }
      },
      'complete':function(response){
      },
      'error':function(XMLHttpRequest, textStatus, errorThrown){
        alert("XMLHttpRequest : " + XMLHttpRequest.status + "/" + "errorThrown    : " + errorThrown.message );
      },
    });
    return responseResult;
}

// response success(Regist)
function OnSuccess(response){
    responseResult = response.result;
}
// response success(Set)
function OnSet(response){
    responseResult = response.result;
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