from django.http.response import HttpResponse         # http response return(json)
import json,traceback;                                # json use

# Jsonコントローラ
class JsonClass:
    
    # コンストラクタ
    def __init__(self):
        self._mes = "";
        self._param = "";
        self._response = "";
        pass

    # Create Response
    def CreateResponse(self):
        self._response = json.dumps({'result':self._param});

    # Return Response
    def ReturnResponse(self):
        return HttpResponse(self._response);
    
    # param set
    def SetParam(self, param):
        self._param = param;
    # param get
    def GetParam(self):
        return self._param;