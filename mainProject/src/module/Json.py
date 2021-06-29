from django.http.response import HttpResponse         # http response return(json)
import json,traceback;                                # json use

# Jsonコントローラ
class JsonClass:
    
    # コンストラクタ
    def __init__(self):
        self._mes = "";
        self._param = "";
        self._paramArr = [];
        self._response = "";
        pass

    # Create Response
    def CreateResponse(self,Mode):
        if Mode == "mes":
            self._response = json.dumps({'result':self._param});
        elif Mode == "array":
            self._response = json.dumps({'result':self._paramArr});

    # Return Response
    def ReturnResponse(self):
        return HttpResponse(self._response);
    
    # param set
    def SetParam(self, param):
        self._param = param;
    # param get
    def GetParam(self):
        return self._param;
    # param set
    def SetParamArray(self, param):
        self._paramArr.append(param);
    # param get
    def GetParamArray(self):
        return self._paramArr;