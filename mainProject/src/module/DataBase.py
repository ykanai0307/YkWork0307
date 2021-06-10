#import MySQLdb
import sqlite3
from ..define.DBModeEnum import DBMode

# DBコントローラ
class DataBaseClass:
    
    # コンストラクタ
    def __init__(self):
        self._conn = ""
        self._cursor=""
        self._host = '127.0.0.1'
        self._port = 3306
        self._user = 'root'
        self._pwd = 'kanai'
        self._db = 'ykdb'
        self._charset = 'utf8'
        pass

    # 接続
    def DbConnect(self,sqlMode):
        #if (sqlMode == DBMode.MYSQL):
        #    self._conn = MySQLdb.connect(
        #        host=self._host,
        #        port=self._port,
        #        user=self._user,
        #        password=self._pwd,
        #        database=self._db,
        #        charset=self._charset
        #    )
        #elif (sqlMode == DBMode.SQLITE):
        if (sqlMode == DBMode.SQLITE):
            dbname = 'ykdb.db'
            self._conn = sqlite3.connect(dbname)
        else:
            pass
    
    # db close
    def DbClose(self):
        if(self._conn != None):
            self._conn = None;

    # cursor set
    def DbCursor(self):
        if(self._conn != None):
            self._cursor = self._conn.cursor();
            
    # cursor close
    def DbCloseCursor(self):
        if(self._cursor != None):
            self._cursor.close();
            
    # execute
    def DbExecute(self,sql):
        if(self._cursor != None):
            self._cursor.execute(sql);
            sql="";
            
    # execute
    def DbExecuteMany(self,sql,data):
        if(self._cursor != None):
            print(data);
            self._cursor.executemany(sql,data);
            sql="";

    # fetch all
    def FetchAll(self):
        if(self._cursor != None):
            return self._cursor.fetchall();
        else:
            return None;
            
    # commit
    def DbCommit(self):
        if(self._conn != None):
            self._conn.commit()
    
    # rollback
    def DbRollback(self):
        if(self._conn != None):
            self._conn.rollback()

    # コネクション取得(プロパティ)
    def GetDbConn(self):
        return self._conn #getter
        
    # カーソル取得(プロパティ)
    def GetDbCursor(self):
        return self._cursor #getter
     
    def SetSelfDirPath(self, value):
        self._conn = value #setter