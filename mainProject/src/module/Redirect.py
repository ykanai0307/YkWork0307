from django.shortcuts import redirect  # redirect use

# Redirectコントローラ
class RedirectClass:
    
    # コンストラクタ
    def __init__(self):
        self._url = "";
        self._param = "";
        pass

    # Redirect
    def RedirectParam(self):
        # redirect
        response = redirect(self.GetUrl());
        response['location'] += '?' + self.GetParam();
        return response;
        
    # Redirect
    def Redirect(self):
        response = redirect(self.GetUrl());
        return response;
    
    # url set
    def SetUrl(self, url):
        self._url = url;
    # data get
    def GetUrl(self):
        return self._url;
        
    # param set
    def SetParam(self, param):
        self._param = param;
    def GetParam(self):
        return self._param;