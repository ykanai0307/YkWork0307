import sys
import urllib.request
from django.shortcuts import render                     # disp rendering
from ..module.UserAgent import UserAgentClass           # User Agent
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
      self._agent = '';
      self._authNum = '';
      self._vm = '';
      self._ses = '';
      self._selecter = [];
      self._pc = False;
      self._veiw = 'menuView.html';
  
  # GET_METHOD
  def get(self, request, *args, **kwargs):
      try:
          self._vm = ViewModuleClass();
          # user agent
          self._pc = self._vm.UserAgent(request);
          # auth
          self._authNum = self._vm.Auth(request);
          self._selecter = self._vm.AuthSelect();
          context = {
            'message': self._mes,
            'authState' : self._authNum,
            'selecter' : self._selecter,
            'pc' : self._pc,
          }
      except Exception as e:
          print('[DB Connection Error]', e)
          sys.exit(1) # プログラムをエラー終了
      
      return render(request, self._veiw, context)
  
  # POST_METHOD
  def post(self, request, *args, **kwargs):
      try:
          self._vm = ViewModuleClass();
          # user agent
          self._pc = self._vm.UserAgent(request);
      
          # login check
          self._auth = AuthClass();
          if request.POST.get("auth") != None:
              self._auth.SetFormAuth(request.POST.get("auth"));
          self._auth.Auth();
          if (int(self._auth.GetFormAuth()) < 1) and ( (request.POST.get("userid") != None) and (request.POST.get("userid") != "") ) and ( (request.POST.get("pass") != None) and (request.POST.get("pass") != "") ):
              if( self._auth.LoginCheck(request.POST.get("userid"),request.POST.get("pass")) ):
                  pass; # admin login OK
              else:
                  self._auth.AuthClear();
          else:
              pass;
          
          # session
          self._ses = SessionClass(request);
          self._ses.SetExp(1800); # 30 sec
          self._ses.DelKey('Auth');
          self._ses.SetValue('Auth',self._auth.GetAuth()[0]);
          auth = self._ses.GetValue('Auth');
          if auth != None :
              if int(auth) < 1: # admin
                  self._selecter = ["selected",""];
              else:
                  self._selecter = ["","selected"];
          else:
              self._selecter = ["","selected"];
          context = {
              'message': 'test',
              'authState' : auth,
              'selecter' : self._selecter,
              'pc' : self._pc,
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