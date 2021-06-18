import sys;
import glob;
import os;
import urllib.request;
from ..module.Redirect import RedirectClass;      # Redirect
from django.shortcuts import render;              # disp rendering
from django.views.generic import View;

# Calendar create
class calendarView(View):
  # init
  def __init__(self, **kwargs):
      self._calender = "";
      self._redirect = "";
      self._mes = "";
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
          'message': self._mes
      };
      return render(request, self._veiw, context);
  # post
  def post(self, request, *args, **kwargs):
      context = {
          'message': 'test',
      };
      return render(request, self._veiw, context);


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

  # property
  def GetCalender(self):
      return self._calender;
  def SetCalender(self, value):
      self._calender = value;