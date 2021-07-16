# sessionコントローラ
class SessionClass:
    
    # コンストラクタ
    def __init__(self,request=None):
        self._request = request;
        pass;

    # set expiry
    def SetExp(self,num):
        try:
            if self._request != None:
                if not self.ExistsKey("_session_expiry") or (num == 0):
                    self._request.session.set_expiry(num);
        except Exception as e:
            raise;

    # set session
    def SetValue(self,key,value):
        try:
            if self._request != None:
                if not self.ExistsKey(key):
                    self._request.session[key] = value;
        except Exception as e:
            raise;
            
    # get session
    def GetValue(self,key):
        try:
            if self._request != None:
                if self.ExistsKey(key):
                    return self._request.session[key];
                else:
                    return None;
        except Exception as e:
            return None;
            
    # exists session key check
    def ExistsKey(self,key):
        try:
            if self._request != None:
                return (key in self._request.session);
        except Exception as e:
            return False;
            
    # session set num check
    def SessionNum(self):
        try:
            if self._request != None:
                return len(self._request.session.keys());
        except Exception as e:
            return 0;
            
    # del session
    def DelKey(self,key):
        try:
            if self._request != None:
                if self.ExistsKey(key):
                    del self._request.session[key];
        except Exception as e:
            raise;
            
    # clear session
    def ClearSession(self):
        try:
            if self._request != None:
                self._request.session.clear();
        except Exception as e:
            raise;
    
    # request set
    def SetRequest(self, request):
        self._request = request;
    # request get
    def GetRequest(self):
        return self._request;