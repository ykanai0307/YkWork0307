import sys
import urllib.request
from django.shortcuts import render                     # disp rendering
from ..module.Auth import AuthClass                     # Auth
from ..module.Session import SessionClass               # Session
from ..module.view.ViewModule import ViewModuleClass    # ViewModule
from ..module.Redirect import RedirectClass             # Redirect
from django.views.generic import View                   # to class

class menuView(View):

  # 初期処理
  def __init__(self, **kwargs):
      self._mes = '';
      self._auth = '';
      self._authNum = '';
      self._vm = '';
      self._ses = '';
      self._selecter = [];
      self._veiw = 'menuView.html';
  
  # GET_METHOD
  def get(self, request, *args, **kwargs):
      try:
          self._vm = ViewModuleClass();
          self._authNum = self._vm.Auth(request);
          self._selecter = self._vm.AuthSelect();
          context = {
            'message': self._mes,
            'authState' : self._authNum,
            'selecter' : self._selecter
          }
      except Exception as e:
          print('[DB Connection Error]', e)
          sys.exit(1) # プログラムをエラー終了
      
      return render(request, self._veiw, context)
  
  # POST_METHOD
  def post(self, request, *args, **kwargs):
      try:
          self._auth = AuthClass();
          self._ses = SessionClass(request);
          self._ses.SetExp(1800); # 30 sec
          if request.POST.get("auth") != None:
              self._auth.SetFormAuth(request.POST.get("auth"));
          self._auth.Auth();
          self._ses.DelKey('Auth');
          self._ses.SetValue('Auth',self._auth.GetAuth()[0]);
          auth = self._ses.GetValue('Auth');
          if auth != None :
              if int(auth) < 1:
                self._selecter = ["selected",""];
              else:
                self._selecter = ["","selected"];
          else:
              self._selecter = ["","selected"];
          context = {
              'message': 'test',
              'authState' : self._ses.GetValue('Auth'),
              'selecter' : self._selecter
          };
      except Exception as e:
          print('[DB Connection Error]', e)
          sys.exit(1) # プログラムをエラー終了
      return render(request, self._veiw, context);
  
  # logout
  @classmethod
  def logout(cls,request):
      redirectIns = RedirectClass();
      try:
          cls._ses = SessionClass(request);
          cls._ses.DelKey('Auth');
          cls._ses.SetExp(0); # time clear
          cls._ses.ClearSession();
      except Exception as e:
          cls._mes = "logout faild [" + str(e) + "]";
      redirectIns.SetUrl('menu');
      return redirectIns.Redirect(); # redirect