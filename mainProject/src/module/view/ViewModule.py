from ..Session import SessionClass        # Session
from ..UserAgent import UserAgentClass    # User Agent

# 画面用コントローラ
class ViewModuleClass:
    
    # コンストラクタ
    def __init__(self):
        self._ses = "";
        self._auth = "";
        self._selecter = [];
        self._agent = "";
        pass

    # auth get
    def Auth(self,request):
        self._ses = SessionClass(request);
        self._auth = self._ses.GetValue('Auth');
        return self._auth;
        
    # auth select set
    def AuthSelect(self):
        if self._auth != None :
            if int(self._auth) < 1 :
              self._selecter = ["selected",""];
            else:
              self._selecter = ["","selected"];
        else:
            self._selecter = ["","selected"];
        return self._selecter;
    
    # user agent
    def UserAgent(self,request):
        pc = False;
        self._agent = UserAgentClass();
        self._agent.SetAgent(str(request.META["HTTP_USER_AGENT"]));
        self._agent.MobileOrPc();
        if self._agent.GetPc() == True:
            pc = True;
        elif self._agent.GetMoblie() == True:
            pc = False;
        return pc;