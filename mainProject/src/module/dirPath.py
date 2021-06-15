from os.path import abspath, join, split
import os;

# パスコントローラ
class dirPathClass:

    #コンストラクタ
    def __init__(self):
        self.UrlHost = r"http://localhost:8000/"
        
        self.OutDir = r"C:/Work/"
        
        self.SqlitePath = os.path.dirname(abspath(join(__file__,'../../../')));
        
        # 自身ディレクトリ指定
        self.self_dir = abspath(__file__)
        # mainProject直下のstatic/resultを参照
        self.selfToStaticResultDir = abspath(join(__file__, '../../../static/result')) + '/'
        # mainProject直下のstatic/uploadを参照
        self.selfToStaticUploadDir = abspath(join(__file__, '../../../static/upload')) + '/'
        
        self.selfToStaticImgDir = abspath(join(__file__, '../../../static/img')) + '/'
        
        self.selfToStaticResultRelativeDir = r"mainProject/static/result/"
        
        self.selfToStaticImgRelativeDir = r"mainProject/static/img/"

    # Sqlite
    def GetSqlitePath(self):
        return self.SqlitePath;
    #setter
    def SetSqlitePath(self, value):
        self.SqlitePath = value;

    # static/uploadを取得(プロパティ)
    def GetUrlHost(self):
        return self.UrlHost #getter
        
    # static/uploadを取得(プロパティ)
    def GetOutDir(self):
        return self.OutDir #getter
        
    # static/uploadを取得(プロパティ)
    def GetSelfToStaticImgDir(self):
        return self.selfToStaticImgDir #getter
    
    # 自身ディレクトリ取得(プロパティ)
    def GetSelfDirPath(self):
        return self.self_dir #getter
     
    def SetSelfDirPath(self, value):
        self.self_dir = value #setter
    
    # static/resultを取得(プロパティ)
    def GetSelfToStaticResultDirPath(self):
        return self.selfToStaticResultDir #getter
     
    def SetSelfToStaticResultDirPath(self, value):
        self.selfToStaticResultDir = value #setter
        
    # static/uploadを取得(プロパティ)
    def GetSelfToStaticUploadDirPath(self):
        return self.selfToStaticUploadDir #getter
     
    def SetSelfToStaticUploadDirPath(self, value):
        self.selfToStaticUploadDir = value #setter
        
    # static/uploadを取得(プロパティ)
    def GetSelfToStaticResultRelativeDirPath(self):
        return self.selfToStaticResultRelativeDir #getter
        
    # static/uploadを取得(プロパティ)
    def GetSelfToStaticImgRelativeDirPath(self):
        return self.selfToStaticImgRelativeDir #getter