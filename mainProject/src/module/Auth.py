from .DataBase import DataBaseClass   # DBbase class
from .Query import Query              # all sql
# datetime edit
from .DateTimeControl import DateTimeControlClass;
from ..define.DBModeEnum import DBMode       # DB mode(sqllite mysql)

# 権限設定コントローラ
class AuthClass:
    
    # コンストラクタ
    def __init__(self):
        self._auth = ();
        self._fauth = 1;
        self._db = "";
        self._qr = "";
        self._sql = "";
        self._datetime = "";
        pass;

    # Auth Select
    def Auth(self):
        self._db = DataBaseClass();
        self._qr = Query();
        self._datetime = DateTimeControlClass();
        valueList = ();
        try:
            self._db.DbConnect(DBMode.SQLITE);
            self._db.DbCursor();
            self.AuthSelectTableCount(self._db,self._qr);
            result = self._db.FetchAll();
            if(int(result[0][0]) < 1): # Table not Exist
                self.AuthCreate(self._db,self._qr,self._datetime);
            else:
                # self.AuthDropTable(self._db,self._qr);
                pass;
            # auth select
            self.AuthSelect(self._db,self._qr,( int(self.GetFormAuth()),int(0) , ),"where");
            self.SetAuth( self._db.FetchAll()[0] );
        except Exception as e:
            self._db.DbRollback();
            raise;

    # LoginCheck
    def LoginCheck(self,userid,password):
        try:
            if ( userid == "admin" ) and ( password == "admin01" ):
                return True;
            else:
                return False;
        except Exception as e:
            return False;
    
    # auth clear
    def AuthClear(self):
        try:
            self.SetAuth( (None,"") );
        except Exception as e:
            return False;

    # (privateMethod)Auth create
    @classmethod
    def AuthCreate(cls,db,query,datetime):
        try:
            # create table make
            cls.AuthCreateTable(db,query);
            db.DbCloseCursor();
            # insert
            datetime.NowDateTimeConvert();
            valueList = ( 
            ( 0,"admin",datetime.GetDateTimeHmsNowStr(),datetime.GetDateTimeHmsNowStr() , ),
            ( 1,"general",datetime.GetDateTimeHmsNowStr(),datetime.GetDateTimeHmsNowStr() , ),
             );
            cls.AuthInsert(db,query,valueList);
            db.DbCommit();
            db.DbCloseCursor();
        except Exception as e:
            raise;

    # (privateMethod)Auth create table
    @classmethod
    def AuthCreateTable(cls,db,query):
        try:
            db.DbCursor();
            query.SetTableName("M_AUTH");
            query.SetCollum("Auth INTEGER NOT NULL PRIMARY KEY");
            query.SetCollum("AuthName TEXT DEFAULT NULL");
            query.SetCollum("Update_Dt TIMESTAMP DEFAULT NULL");
            query.SetCollum("Create_Dt TIMESTAMP DEFAULT NULL");
            query.SetCollum("Active INTEGER NOT NULL DEFAULT 0");
            cls._sql = query.CreateTable();
            db.DbExecute(cls._sql);
            query.ClearCollum();
        except Exception as e:
            raise;
            
    # (privateMethod)Auth drop table
    @classmethod
    def AuthDropTable(cls,db,query):
        try:
            db.DbCursor();
            query.SetTableName("M_AUTH");
            cls._sql = query.DropTable();
            db.DbExecute(cls._sql);
            db.DbCloseCursor();
        except Exception as e:
            raise;
            
    # (privateMethod)selectTableCount
    @classmethod
    def AuthSelectTableCount(cls,db,query):
        try:
            query.SetTableName("M_AUTH");
            cls._sql = query.TableSelectCount();
            db.DbExecute(cls._sql);
        except Exception as e:
            raise;
    
    # (privateMethod)select
    @classmethod
    def AuthSelect(cls,db,query,valueList=(),mode=""):
        try:
            db.DbCursor();
            query.SetTableName("M_AUTH");
            query.SetCollum("Auth");
            query.SetCollum("AuthName");
            if mode == "where":
                query.SetWhereList(" AND Auth = ? ");
                query.SetWhereList(" AND Active = ? ");
            cls._sql = query.Select();
            db.DbBindExecute(cls._sql,valueList);
            query.ClearCollum();
            query.ClearWhereList();
        except Exception as e:
            raise;
            
    # (privateMethod)insert
    @classmethod
    def AuthInsert(cls,db,query,valueList=()):
        try:
            db.DbCursor();
            query.SetTableName("M_AUTH");
            query.SetCollum("Auth");
            query.SetCollum("AuthName");
            query.SetCollum("Update_Dt");
            query.SetCollum("Create_Dt");
            cls._sql = query.Insert();
            query.ClearCollum();
            db.DbExecuteMany(cls._sql,valueList);
        except Exception as e:
            raise;
    
    # auth set
    def SetAuth(self, value):
        self._auth = value;
    # auth get
    def GetAuth(self):
        return self._auth;
        
    # form select auth set
    def SetFormAuth(self, num):
        self._fauth = num;
    # form select auth get
    def GetFormAuth(self):
        return self._fauth;