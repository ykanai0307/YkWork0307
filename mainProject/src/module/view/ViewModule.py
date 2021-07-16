from ..Session import SessionClass  # Session

# 画面用コントローラ
class ViewModuleClass:
    
    # コンストラクタ
    def __init__(self):
        self._ses = "";
        self._auth = "";
        self._selecter = [];
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