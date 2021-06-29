import sys;
import glob;
import os;
import urllib.request;
from django.http.response import Http404                # http response 404
from ..module.Redirect import RedirectClass;            # Redirect
from ..module.Json import JsonClass;                    # Json
from ..module.DateTimeControl import DateTimeControlClass; # datetime edit
from ..module.DataBase import DataBaseClass             # DBbase class
from ..define.DBModeEnum import DBMode                  # DB mode(sqllite mysql)
from ..module.Query import Query                        # all sql
from ..module.SendValueShare import SendValueShareClass # [post get list] convert
from .mainView import mainView
from django.shortcuts import render;                    # disp rendering
from django.views.generic import View;

# Calendar create
class calendarView(View):
  # init
  def __init__(self, **kwargs):
      self._table = "T_PLANS";
      self._calender = "";
      self._redirect = "";
      self._json = "";
      self._datetime = "";
      self._db = "";
      self._qr = "";
      self._send = "";
      self._mes = "";
      
      self._data = [];
      self._html = [];
      
      self._veiw = 'calendarView.html';
  # get
  def get(self, request, *args, **kwargs):
      try:
          self._mes = request.GET.get("mes");
          if self._mes == None:
              self._mes = "get";
          pass;
      except Exception as e:
          self._mes = e;
      context = {
          'message': self._mes,
      };
      return render(request, self._veiw, context);
  # post
  def post(self, request, *args, **kwargs):
      context = {
          'message': 'test',
      };

  # calendar create
  @classmethod
  def create(cls,request):
      cls._calender = calendarView();  # self
      cls._redirect = RedirectClass(); # redirect
      cls._mes = "";
      if request.method == 'POST':
          try:
              cls._mes = "calendar create success";
          except Exception as e:
              cls._mes = "calendar create faild [" + str(e) + "]";
          pass;
      else: # GET
          cls._mes = "";
      cls._redirect.SetUrl('calendar');
      cls._redirect.SetParam('mes=' + cls._mes);
      return cls._redirect.RedirectParam(); # redirect
      
  # calendar popup click
  @classmethod
  def popup_click(cls,request):
      cls._calender = calendarView();  # self
      cls._json = JsonClass();
      cls._db = DataBaseClass();
      cls._qr = Query();
      cls._send = SendValueShareClass();
      cls._data = [];
      cls._datetime = DateTimeControlClass();
      cls._mes = "";
      Mode = "";
      Date = "";
      Memo = "";
      if request.method == 'POST':
          try:
              insResult = ();
              upResult = ();
              valueList = ();
              # post value get
              if request.POST.get('postData[Mode]') != None:
                  Mode = request.POST.get('postData[Mode]');
              if request.POST.get('postData[Date]') != None:
                  Date = request.POST.get('postData[Date]');

              if Mode == "Set":
                  valueList = ( str(Date + " 01:01:01"),0, );
                  cls._data = cls.SelectSql(valueList);
              elif Mode == "Regist":
                  if request.POST.get('postData[Memo]') != None:
                      Memo = request.POST.get('postData[Memo]');
                  cls._datetime.NowDateTimeConvert();
                  insResult = ( ( ( str(Date + " 01:01:01"),str(Memo),cls._datetime.GetDateTimeHmsNowStr(),cls._datetime.GetDateTimeHmsNowStr() ) ,) );
                  valueList = ( str(Date + " 01:01:01"),0, );
                  
                  # open
                  cls._db.DbConnect(DBMode.SQLITE);
                  
                  # select
                  cls._data = cls.SelectSql(valueList);
                  cls._db.DbCloseCursor();
                  if len(cls._data) > 0:
                      # update
                      upResult = ( str(Memo),str(Date + " 01:01:01"),0 );
                      cls._db.DbCursor();
                      mainView.SelfUpdate(cls._db , cls._qr , upResult );
                  else:
                      # insert
                      cls._db.DbCursor();
                      mainView.SelfInsert(cls._db , cls._qr , insResult );
                  
                  # submit
                  cls._db.DbCommit();
                  cls._db.DbCloseCursor();
                  cls._mes = "[" + str(Date) + " " + str(Memo) + "] calendar create success";
                  
          except Exception as e:
              cls._mes = "calendar create faild [" + str(e) + "]";
          pass;
      else: # GET
          cls._mes = "calendar create faild (get)";
          raise Http404;
      # Response return
      if cls._mes == "":
          cls._json.SetParamArray(cls._data);
          cls._json.CreateResponse("array");
      else:
          cls._json.SetParam(cls._mes);
          cls._json.CreateResponse("mes");
      return cls._json.ReturnResponse();

  @classmethod
  def SelectSql(cls,valueList):
      cls._db = DataBaseClass();
      cls._db.DbConnect(DBMode.SQLITE);
      cls._db.DbCursor();
      cls._qr = Query();
      calendarView.SelfSelect(cls._db,cls._qr,valueList);
      return cls._db.FetchAll();
      
  # (privateMethod)select
  @classmethod
  def SelfSelect(cls,dbBase,sqlClass,valueList):
      try:
          sqlClass.SetTableName("T_PLANS");
          sqlClass.SetCollum("CalendarDateTime");
          sqlClass.SetCollum("Txt");
          sqlClass.SetWhereList(" AND CalendarDateTime = ? ");
          sqlClass.SetWhereList(" AND Active = ? ");
          cls._sql = sqlClass.Select();
          dbBase.DbBindExecute(cls._sql,valueList);
          sqlClass.ClearCollum();
          sqlClass.ClearWhereList();
      except Exception as e:
          raise;
      
  # property
  def GetCalender(self):
      return self._calender;
  def SetCalender(self, value):
      self._calender = value;