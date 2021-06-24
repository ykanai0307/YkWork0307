import sys;
import glob;
import os;
import urllib.request;
from django.http.response import Http404                # http response 404
from ..module.Redirect import RedirectClass;            # Redirect
from ..module.Json import JsonClass;                    # Json
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
      self._calender = "";
      self._redirect = "";
      self._json = "";
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
          self._data = self.SelectSql();
          for data in self._data:
               self._html.append("<label name=\"param\" class=\"param\" >" + data[3] + ":" + data[1] + "</label>");
          pass;
      except Exception as e:
          self._mes = e;
      context = {
          'message': self._mes,
          'registParam': self._html,
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
      cls._mes = "";
      Date = "";
      Memo = "";
      if request.method == 'POST':
          try:
              result = [];
              # post value get
              if request.POST.get('postData[Date]') != None:
                  Date = request.POST.get('postData[Date]');
              if request.POST.get('postData[Memo]') != None:
                  Memo = request.POST.get('postData[Memo]');
              result.append( ( Memo,"",Date,"",1 ) );
              
              # open
              cls._db.DbConnect(DBMode.SQLITE);
              # insert make
              mainView.SelfInsert(cls._db , cls._qr , result );
              
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
      cls._json.SetParam(cls._mes);
      cls._json.CreateResponse();
      return cls._json.ReturnResponse();

  @classmethod
  def SelectSql(cls):
      cls._db = DataBaseClass();
      cls._db.DbConnect(DBMode.SQLITE);
      cls._db.DbCursor();
      cls._qr = Query();
      mainView.SelfSelect(cls._db,cls._qr);
      return cls._db.FetchAll();
      
  # property
  def GetCalender(self):
      return self._calender;
  def SetCalender(self, value):
      self._calender = value;