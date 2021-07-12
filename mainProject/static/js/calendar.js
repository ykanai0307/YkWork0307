// calendar(main)
var responseResult;
var DefhhMMss = " 01:01:01";
var DefStarthhMMss = " 00:00:01";
var DefEndhhMMss = " 23:59:59";
$(function(){
    // global var
    var currentDate = '20210624';
    var currentDateTime = "";
    
    var initCarendarPopUpTop = 0;
    var scroll = 0;
    
    var currentMonth = new Date().getMonth();
    var currentYear = new Date().getFullYear();
    
    var startDatePos = 0;
    var endDatePos = 0;
    
    try {
        MainCreateCalendar(currentYear,currentMonth);
    } catch(e) {
        alert("this month get faild [" + e.message + "]");
    }
    
    // day click event
    $('#CalenderView').on('click','.DayList',function(e){
        try {
            var num = $('.DayList').index(this);
            var lbl = $('.DayList').eq(num).children('label');
            var pos = 0;
            pos = num % 7;
            var label = $('#CalenderView').find('label.Week')[pos];
            
            // select (year month date) set
            var lblTmp = lbl[0].innerText.replace("〇", "").split('\n');
            currentDateTime = new Date(hankakuZenkaku($('#year')[0].innerText).toString(), zeroPadding(hankakuZenkaku($('#month')[0].innerText),2).toString(), zeroPadding(hankakuZenkaku(Number(lblTmp[0]).toString()),2).toString(), "01", "01", "01");
            var monthCateg = lbl[0].classList[1].split('_');
            if(monthCateg[0] == "LastMonth"){
                currentDateTime.setMonth(currentDateTime.getMonth()-1);
            }
            currentDateTime = new Date(currentDateTime.setDate(zeroPadding(Number(lblTmp[0]),2).toString()));
            currentDate = 'YYYY/MM/DD';
            currentDate = currentDate.replace(/YYYY/g, currentDateTime.getFullYear());
            currentDate = currentDate.replace(/MM/g, zeroPadding(currentDateTime.getMonth(),2));
            currentDate = currentDate.replace(/DD/g, zeroPadding(currentDateTime.getDate(),2));
            
            if(lblTmp.length > 0 && lblTmp[0] == ""){
                return true;
            }
            
            // CalenderPopUp create
            var popUpHtml = CreatePopUp();
            
            // CalenderPopUp view set
            $('#CalenderPopUpView').html(popUpHtml);
            
            // Label to date
            var holidayLabel = "";
            if(lblTmp.length > 1){
                holidayLabel = '\n' + lblTmp[1];
            }
            $('#CalenderPopUp').find('label.day').text(zeroPadding( Number(lblTmp[0]) ,2) + " " + label.innerText + " " + holidayLabel);
            
            // init(select) val set
            postData = {};
            postData['Mode'] = "Set";
            postData['Date'] = currentDate;
            var url = "/mainProject/calendar_popup_click";
            responseResult = post(url,false,postData,"Set",getCookie("csrftoken"));
            
            // date compare
            if( ( responseResult.length > 0 ) && ( responseResult[0].length > 0 ) && ( responseResult[0][0].length > 0 ) ){
                var date1 = new Date(responseResult[0][0][0]);
                var date2 = new Date(currentDate + DefhhMMss);
                if(date1.getTime() == date2.getTime()){
                    $("input[name=\"PopUpMemo\"]").val(responseResult[0][0][1]);
                }
            }
            
            // CalenderPopUp view position adjust
            initCarendarPopUpTop = (window.pageYOffset + e.clientY) - 135;
            $('#CalenderPopUp').offset({top: initCarendarPopUpTop, left: (window.pageXOffset + e.clientX) - 115});
            
            // CalenderPopUp view
            $('#CalenderPopUp').css('visibility','visible');
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
    
    // popup close click
    $('#CalenderPopUpView').on('click','#Close',function(){
        try {
            $('#CalenderPopUp').css('visibility','collapse');
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
    
    // LastMonth click
    $('#CalenderView').on('click','#LastMonth',function(e){
      try {
          currentMonth -= 1;
          if(currentMonth < 0){
              currentYear -= 1;
              currentMonth = 11;
          }
          MainCreateCalendar(currentYear,currentMonth);
      } catch(e) {
          alert("LastMonth click faild [" + e.message + "]");
      }
    });
    
    // NextMonth click
    $('#CalenderView').on('click','#NextMonth',function(e){
      try {
          currentMonth += 1;
          if(currentMonth > 11){
              currentYear += 1;
              currentMonth = 0;
          }
          MainCreateCalendar(currentYear,currentMonth);
      } catch(e) {
          alert("LastMonth click faild [" + e.message + "]");
      }
    });
});

// db to carendarData get
function GetCarendarData(Year,Month){
   try {
       postData = {};
       postData['Mode'] = "SetAll";
       var s = Year + "/" + zeroPadding((Month + 1).toString(),2) + "/01" + DefStarthhMMss;
       var e = Year + "/" + zeroPadding((Month + 2).toString(),2) + "/01" + DefEndhhMMss;
       var startDate = new Date(s).setDate(1);
       var endDate = new Date(e).setDate(0);
       var startDate = getStringFromDate(new Date(startDate));
       var endDate = getStringFromDate(new Date(endDate));
       postData['startDate'] = startDate;
       postData['endDate'] = endDate;
       
       //postData['Date'] = Year + zeroPadding( Month.toString() ,2);
       postData['Memo'] = $("input[name=\"PopUpMemo\"]").val();
       
       // csrf_token (post)
       var csrf_token = getCookie("csrftoken");
       var url = "/mainProject/calendar_popup_click";
       var result = [];
       post(url,false,postData,"SetAll",csrf_token);
       if( ( responseResult.length > 0 ) && ( responseResult[0].length > 0 ) && ( responseResult[0][0].length > 0 ) ){
           for(var i = 0;i<responseResult[0].length;i++) {
               result.push(responseResult[0][i][0]);
           }
       }
       return result;
   } catch(e) {
       alert("GetCarendarData faild [" + e.message + "]");
   }
}

// date to string
function getStringFromDate(date) {
   try {
       var year_str = date.getFullYear();
       // 月だけ+1すること
       var month_str = 1 + date.getMonth();
       var day_str = date.getDate();
       var hour_str = date.getHours();
       var minute_str = date.getMinutes();
       var second_str = date.getSeconds();
       
       format_str = 'YYYY/MM/DD hh:mm:ss';
       format_str = format_str.replace(/YYYY/g, year_str);
       format_str = format_str.replace(/MM/g, zeroPadding(month_str,2));
       format_str = format_str.replace(/DD/g, zeroPadding(day_str,2));
       format_str = format_str.replace(/hh/g, zeroPadding(hour_str,2));
       format_str = format_str.replace(/mm/g, zeroPadding(minute_str,2));
       format_str = format_str.replace(/ss/g, zeroPadding(second_str,2));
       
       return format_str;
   } catch(e) {
       alert("getStringFromDate faild [" + e.message + "]");
   }
};

// create
function MainCreateCalendar(Year,Month){
    try {
        var startDate = MonthStartGet(Year,Month,1);    // MonthStartate
        var endDate = MonthEndGet(Year,Month + 1,0);    // MonthEndDate
        var dateList = DayList(startDate,endDate);      // Day list create

        var nextStartDate = MonthStartGet(Year,Month + 1,1);
        var nextEndDate = MonthEndGet(Year,Month + 2,0);
        var nextDateList = DayList(nextStartDate,nextEndDate);
        
        var lastStartDate = MonthStartGet(Year,Month - 1,1);
        var lastEndDate = MonthEndGet(Year,Month,0);
        var lastDateList = DayList(lastStartDate,lastEndDate);
        
        var beforeLastStartDate = MonthStartGet(Year,Month - 2,1);
        var beforeLastEndDate = MonthEndGet(Year,Month - 1,0);
        var beforeLastDateList = DayList(beforeLastStartDate,beforeLastEndDate);
        
        var CalendarHtml = CreateCalendar(Month,Year,dateList,nextDateList,lastDateList,beforeLastDateList,GetCarendarData(Year,Month));
        $('#CalenderView').html(CalendarHtml);
        $('#CalenderView').css('visibility','visible');
        return true;
    } catch(e) {
        alert("CalendarCreate faild [" + e.message + "]");
        return false;
    }
}

// MonthStartDate
function MonthStartGet(currentYear,currentMonth,addDate){
    var startDate = false;
    try {
        var dateVal = new Date();
        dateVal.setFullYear(currentYear);
        dateVal.setMonth(currentMonth);
        startDate = new Date(dateVal.setDate(addDate));
    } catch(e) {
        alert("MonthStartGet get faild [" + e.message + "]");
    }
    return startDate;
}

// MonthEndDate
function MonthEndGet(currentYear,currentMonth,addDate){
    var endDate = false;
    try {
        var dateVal = new Date();
        dateVal.setFullYear(currentYear);
        dateVal.setMonth(currentMonth);
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
            var dateData = d.getFullYear() + '/' + zeroPadding( (d.getMonth()+1) ,2) + '/' + zeroPadding( d.getDate() ,2);
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

// create Calendar
function CreateCalendar(month,year,dateList,nextDateList,lastDateList,beforeLastDateList,CarendarDataList){
    var startPos = $.inArray(dateList[0]["week"], getWeekly());
    var rowSum = Math.ceil( (startPos + dateList.length) / 7 );
    var MonthViewCss = "";
    if(String((month + 1)).length > 1){
        MonthViewCss = "MonthViewTwoUnit";
    }else{
        MonthViewCss = "MonthView";
    }
    
    // CalenderPopUp create
    var CalendarHtml = "<table id=\"Calender\">";
    CalendarHtml += "  <tr>";
    CalendarHtml += "    <td class=\"RoundMark_left\" rowspan=\"" + (rowSum + 4) + "\" ><label class=\"RoundMark\">〇</label></td>";
    CalendarHtml += "    <td class=\"height-15px\" colspan=\"7\" ></td>";
    CalendarHtml += "    <td class=\"RoundMark_right\" rowspan=\"" + (rowSum + 4) + "\"><label class=\"RoundMark\">〇</label></td>";
    CalendarHtml += "  </tr>";
    CalendarHtml += "  <tr>";
    CalendarHtml += "    <td class=\"MonthView\" rowspan=\"2\"><label id=\"month\" class=\"" + MonthViewCss + "\">" + (month + 1) + "</label></td>";
    CalendarHtml += "    <td colspan=\"2\"><label class=\"MonthEnglishView\">" + MonthEnglishList()[month] + "</label></td>";
    CalendarHtml += "    <td rowspan=\"2\" colspan=\"2\">"; // LastMonth
    CalendarHtml += LastNextMonthHtml(lastDateList,beforeLastDateList,(month + 1),"Last");
    CalendarHtml += "    </td>";
    CalendarHtml += "    <td rowspan=\"2\" colspan=\"2\">"; // nextMonth
    CalendarHtml += LastNextMonthHtml(nextDateList,dateList,(month + 1),"Next");
    CalendarHtml += "    </td>";
    CalendarHtml += "  </tr>";
    CalendarHtml += "  <tr>";
    CalendarHtml += "    <td><label id=\"year\" class=\"YearView\" colspan=\"2\">" + year + "</label></td>";
    CalendarHtml += "  </tr>";
    CalendarHtml += "  <tr>";
    CalendarHtml += "    <td class=\"Td_Week\"><label class=\"Week Week_sun\">SUN</label></td>";
    CalendarHtml += "    <td class=\"Td_Week\"><label class=\"Week Week_mon\">MON</label></td>";
    CalendarHtml += "    <td class=\"Td_Week\"><label class=\"Week Week_tue\">TUE</label></td>";
    CalendarHtml += "    <td class=\"Td_Week\"><label class=\"Week Week_wed\">WED</label></td>";
    CalendarHtml += "    <td class=\"Td_Week\"><label class=\"Week Week_thu\">THU</label></td>";
    CalendarHtml += "    <td class=\"Td_Week\"><label class=\"Week Week_fri\">FRI</label></td>";
    CalendarHtml += "    <td class=\"Td_Week Border_last_right\"><label class=\"Week Week_sat\">SAT</label></td>";
    CalendarHtml += "  </tr>";
    
    // LastMonth
    for(var l = (lastDateList.length - startPos); l < lastDateList.length;l++) {
        var day = new Date(lastDateList[l]["date"] + DefhhMMss).getDate();
        switch (lastDateList[l]["week"]) {
          case "SUN":
            CalendarHtml += "  <tr>";
            CalendarHtml += "<td class=\"DayList Td_Day\"><label class=\"Day LastMonth_sun\">" + day + "</label></td>";
            break;
          case "MON":
            CalendarHtml += "<td class=\"DayList Td_Day\"><label class=\"Day LastMonth_mon\">" + day + "</label></td>";
            break;
          case "TUE":
            CalendarHtml += "<td class=\"DayList Td_Day\"><label class=\"Day LastMonth_tue\">" + day + "</label></td>";
            break;
          case "WED":
            CalendarHtml += "<td class=\"DayList Td_Day\"><label class=\"Day LastMonth_wed\">" + day + "</label></td>";
            break;
          case "THU":
            CalendarHtml += "<td class=\"DayList Td_Day\"><label class=\"Day LastMonth_thu\">" + day + "</label></td>";
            break;
          case "FRI":
            CalendarHtml += "<td class=\"DayList Td_Day\"><label class=\"Day LastMonth_fri\">" + day + "</label></td>";
            break;
          case "SAT":
            CalendarHtml += "<td class=\"DayList Td_Day Border_last_right\"><label class=\"Day LastMonth_sat\">" + day + "</label></td>";
            CalendarHtml += "  </tr>";
            break;
          default:
            break;
        }    
    }
    
    var currentRowNum = 0;
    var cssBorderUnder = "";
    var cssBorderLast = "";
    var cssToday = "";
    var RegistMemoMarkHtml = "<span class=\"Circle\">〇</span>";
    var RegistMemoMarkSpaceHtml = "<span class=\"Circle\">&nbsp;&nbsp;&nbsp;〇</span>";
    var HolidayHtml = "";
    
    // ThisMonth
    for(var i = 0; i < dateList.length;i++) {
        var day = new Date(dateList[i]["date"] + DefhhMMss).getDate();
        HolidayHtml = "<br/><label class=\"HolidayName\">" + dateList[i]["holiday"] + "</label>";
        
        // today search
        var now = new Date();
        var now = new Date(now.getFullYear().toString() + "/" + zeroPadding( now.getMonth() + 1 ,2).toString() + "/" + zeroPadding( now.getDate() ,2).toString() + DefhhMMss);
        // today select
        if(now.getTime() == new Date(dateList[i]["date"] + DefhhMMss).getTime()){
            cssToday = "today";
        }else{
            cssToday = "";
        }
        
        if(rowSum <= currentRowNum){
            cssBorderUnder = "";
        }else{
            cssBorderUnder = "Border_under";
        }
        
        var Mark = "";
        if( $.inArray( (dateList[i]["date"] + DefhhMMss), CarendarDataList) > -1 ){
            if(day.toString().length < 2){
                Mark = RegistMemoMarkSpaceHtml;
            }else{
                Mark = RegistMemoMarkHtml;
            }
        }
        
        switch (dateList[i]["week"]) {
          case "SUN":
            CalendarHtml += "  <tr>";
            CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssToday + "\"><label class=\"Day ThisMonth_sun\">" + day + Mark + HolidayHtml + "</label></td>";
            break;
          case "MON":
            CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssToday + "\"><label class=\"Day ThisMonth_mon\">" + day + Mark + HolidayHtml + "</label></td>";
            break;
          case "TUE":
            CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssToday + "\"><label class=\"Day ThisMonth_tue\">" + day + Mark + HolidayHtml + "</label></td>";
            break;
          case "WED":
            CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssToday + "\"><label class=\"Day ThisMonth_wed\">" + day + Mark + HolidayHtml + "</label></td>";
            break;
          case "THU":
            CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssToday + "\"><label class=\"Day ThisMonth_thu\">" + day + Mark + HolidayHtml + "</label></td>";
            break;
          case "FRI":
            CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssToday + "\"><label class=\"Day ThisMonth_fri\">" + day + Mark + HolidayHtml + "</label></td>";
            break;
          case "SAT":
            if( (dateList.length-1) == i){
                cssBorderLast = "Border_last";
                CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssBorderLast + " " + cssToday + "\"><label class=\"Day ThisMonth_sat\">" + day + Mark + HolidayHtml + "</label></td>";
            }else{
                cssBorderLast = "Border_last_right";
                CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssBorderLast + " " + cssToday + "\"><label class=\"Day ThisMonth_sat\">" + day + Mark + HolidayHtml + "</label></td>";
            }
            CalendarHtml += "  </tr>";
            currentRowNum += 1;
            break;
          default:
            break;
        }
    };
    // empty day add
    if( (dateList.length + startPos) < (rowSum * 7) ){
        for(var n = (dateList.length + startPos); n < (rowSum * 7);n++) {
            CalendarHtml += "<td class=\"DayList Td_Day " + cssBorderUnder + " " + cssBorderLast + "\"><label class=\"Day ThisMonth_sat\"></label></td>";
        }
    }
    
    CalendarHtml += "  <tr>";
    CalendarHtml += "    <td class=\"RoundMark_left\" colspan=\"8\" ><label class=\"RoundMark\">〇</label></td>";
    CalendarHtml += "    <td class=\"RoundMark_right\" ><label class=\"RoundMark\">〇</label></td>";
    CalendarHtml += "  </tr>";
    CalendarHtml += "</table>";
    
    return CalendarHtml;
}

// LastMonth
function LastNextMonthHtml(lastDateList,beforeLastDateList,month,Mode){
    var startPos = $.inArray(lastDateList[0]["week"], getWeekly());
    var rowSum = Math.ceil( (startPos + lastDateList.length) / 7 );

    if(Mode == "Last"){
      if(month == 1){
        month = 12;
      }else{
        month -= 1;
      }
      var CalendarHtml = "<table id=\"LastMonth\">";
    }else{
      if(month == 12){
        month = 1;
      }else{
        month += 1;
      }
      var CalendarHtml = "<table id=\"NextMonth\">";
    }
    CalendarHtml += "    <tr>";
    CalendarHtml += "      <td rowspan=\"7\"><label class=\"month\">" + month + "</label></td>";
    CalendarHtml += "      <td><label class=\"ThisMonth_sun\">S</label></td>";
    CalendarHtml += "      <td><label class=\"Day ThisMonth_mon\">M</label></td>";
    CalendarHtml += "      <td><label class=\"Day ThisMonth_tue\">T</label></td>";
    CalendarHtml += "      <td><label class=\"Day ThisMonth_wed\">W</label></td>";
    CalendarHtml += "      <td><label class=\"Day ThisMonth_thu\">T</label></td>";
    CalendarHtml += "      <td><label class=\"Day ThisMonth_fri\">F</label></td>";
    CalendarHtml += "      <td><label class=\"ThisMonth_sat\">S</label></td>";
    CalendarHtml += "    </tr>";
    
    for(var l = (beforeLastDateList.length - startPos); l < beforeLastDateList.length;l++) {
        var day = new Date(beforeLastDateList[l]["date"] + DefhhMMss).getDate();
        switch (beforeLastDateList[l]["week"]) {
          case "SUN":
            CalendarHtml += "  <tr>";
            CalendarHtml += "<td><label class=\"LastMonth_sun\">" + day + "</label></td>";
            break;
          case "MON":
            CalendarHtml += "<td><label class=\"LastMonth_mon\">" + day + "</label></td>";
            break;
          case "TUE":
            CalendarHtml += "<td><label class=\"LastMonth_tue\">" + day + "</label></td>";
            break;
          case "WED":
            CalendarHtml += "<td><label class=\"LastMonth_wed\">" + day + "</label></td>";
            break;
          case "THU":
            CalendarHtml += "<td><label class=\"LastMonth_thu\">" + day + "</label></td>";
            break;
          case "FRI":
            CalendarHtml += "<td><label class=\"LastMonth_fri\">" + day + "</label></td>";
            break;
          case "SAT":
            CalendarHtml += "<td><label class=\"LastMonth_sat\">" + day + "</label></td>";
            CalendarHtml += "  </tr>";
            break;
          default:
            break;
        }    
    }
    // ThisMonth
    for(var i = 0; i < lastDateList.length;i++) {
        var day = new Date(lastDateList[i]["date"] + DefhhMMss).getDate();
        
        switch (lastDateList[i]["week"]) {
          case "SUN":
            CalendarHtml += "  <tr>";
            CalendarHtml += "<td><label class=\"ThisMonth_sun\">" + day + "</label></td>";
            break;
          case "MON":
            CalendarHtml += "<td><label class=\"Day ThisMonth_mon\">" + day + "</label></td>";
            break;
          case "TUE":
            CalendarHtml += "<td><label class=\"Day ThisMonth_tue\">" + day + "</label></td>";
            break;
          case "WED":
            CalendarHtml += "<td><label class=\"Day ThisMonth_wed\">" + day + "</label></td>";
            break;
          case "THU":
            CalendarHtml += "<td><label class=\"Day ThisMonth_thu\">" + day + "</label></td>";
            break;
          case "FRI":
            CalendarHtml += "<td><label class=\"Day ThisMonth_fri\">" + day + "</label></td>";
            break;
          case "SAT":
            CalendarHtml += "<td><label class=\"ThisMonth_sat\">" + day + "</label></td>";
            CalendarHtml += "  </tr>";
            break;
          default:
            break;
        }
    };
    
    CalendarHtml += "  </table>";
    return CalendarHtml;
}

// create popup
function CreatePopUp(){
    // CalenderPopUp create
    var popUpHtml = " <table id=\"CalenderPopUp\">";
    popUpHtml += "  <tr>";
    popUpHtml += "    <td class=\"day\"><label class=\"day\">17 tue</label><input type=\"button\" id=\"Close\" name=\"Close\" value=\"×\"/></td>";
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

// MonthEnglish
function MonthEnglishList(){
    var month_english_list = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'];
    return month_english_list;
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
    for (var i=0; i < holiday.length; i++) {
          if (new Date(fDate + DefhhMMss).getTime() == new Date(holiday[i]["date"] + DefhhMMss).getTime()){
              result = holiday[i]["name"];
          }
    }
    return result;
}

// Weekly get
function getWeekly(){
    var week = ["日","月","火","水","木","金","土"];
    var weekEnglish = ["SUN","MON","TUE","WED","THU","FRI","SAT"];
    return weekEnglish;
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