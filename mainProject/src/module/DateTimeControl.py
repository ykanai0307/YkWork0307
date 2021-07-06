from datetime import datetime as dt;

# DateTime timestampを変換するコントローラ
class DateTimeControlClass:
    
    # コンストラクタ
    def __init__(self):
        self._dateTime = None;
        self._dateTimeStr = None;
        self._dateTimeHmsStr = None;
        self._dateTimeHmsNowStr = None;
        pass

    # datetime conversion
    def DateTimeConvert(self,regex,mode):
        # yyyyMMdd(string)を yyyyMMdd hh:mm:ss(datetime)へ変換する。'%Y%m%d %H:%M:%S'
        if mode == "hhMMss" :
            self._dateTime = dt.strptime( str(self._dateTimeStr + " 01:01:01") ,regex);
            self._dateTimeHmsStr = str(self._dateTime.year) + "/" + self.pad( str(self._dateTime.month), '0>2' ) + "/" + self.pad( str(self._dateTime.day), '0>2' ) + " 01:01:01";
        else:
            self._dateTime = dt.strptime(str(self._dateTimeStr) ,regex);
            self._dateTimeHmsStr = str(self._dateTime.year) + "/" + self.pad( str(self._dateTime.month), '0>2' ) + "/" + self.pad( str(self._dateTime.day), '0>2' );

    # now datetime conversion
    def NowDateTimeConvert(self):
        self._dateTimeHmsNowStr = str(dt.today().year) + "/" + self.pad( str(dt.today().month), '0>2' ) + "/" +  self.pad( str(dt.today().day), '0>2')  + " 01:01:01";
    
    # 0padding
    def pad(self,value,unit):
        return format(value, unit);

    # DateTimeHms set
    def SetDateTimeHmsStr(self, value):
        self._dateTimeHmsStr = value;
    # DateTimeHms get
    def GetDateTimeHmsStr(self):
        return self._dateTimeHmsStr;
    # DateTimeHmsNow set
    def SetDateTimeHmsNowStr(self, value):
        self._dateTimeHmsNowStr = value;
    # DateTimeHmsNow get
    def GetDateTimeHmsNowStr(self):
        return self._dateTimeHmsNowStr;
        
    # DateTime set
    def SetDateTimeStr(self, value):
        self._dateTimeStr = value;
    # DateTime get
    def GetDateTimeStr(self):
        return self._dateTimeStr;