from .DateTimeControl import DateTimeControlClass;            # datetime edit

# 受け取った値を設定し直すコントローラ
class SendValueShareClass:
    
    # コンストラクタ
    def __init__(self):
        self._request = None;
        self._dataArray = None;
        self._result = [];
        self._collum = [];
        self._work = [];
        pass

    # send data conversion
    def SendDataConversion(self):
        col = 0;
        if self._request != None:
            if self._request.method == "POST":
                if len(self._collum) > 0:
                    for col in range(len(self._collum)):
                        self._work.append( self._request.POST.getlist(str(self._collum[col])) );
                    self.ResultCreate(self._work);
                else:
                    pass; # 結果0件で返却。
            else: # get
                if len(self._collum) > 0:
                    for col in range(len(self._collum)):
                        self._work.append( self._request.GET.getlist(str(self._collum[col])) );
                    ResultCreate(self._work);
                else:
                    pass; # 結果0件で返却。
        elif self._dataArray != None:
            #for col in range(len(self._collum)):
                #self._work[col] = self._request.POST.getlist(str(self._collum[col]));
            pass;
        
    # 結果生成
    def ResultCreate(self,work):
        for rowNum in range(len(work[0])):
            # datetime convert
            dcc = DateTimeControlClass();
            # datetime (-) to (/) convert
            dcc.SetDateTimeStr( str(work[1][int(work[0][rowNum])].replace('-', '/')));
            dcc.DateTimeConvert(r'%Y/%m/%d %H:%M:%S',"hhMMss");
            # now
            dcc.NowDateTimeConvert();
            self._result.append( ( dcc.GetDateTimeHmsStr(),str(work[2][int(work[0][rowNum])]),dcc.GetDateTimeHmsNowStr(),dcc.GetDateTimeHmsNowStr(), ) );

    # collum set
    def SetCollum(self, value):
        self._collum.append(value);
    
    # request set
    def SetRequest(self, value):
        self._request = value;
    # data set
    def SetData(self, value):
        self._dataArray = value;
        
    # request get
    def GetRequest(self):
        return self._request;
    # data get
    def GetData(self):
        return self._dataArray;
    # result get
    def GetResult(self):
        return self._result;