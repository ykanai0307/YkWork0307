# Sqlクラス
class Query:
    
    # コンストラクタ
    def __init__(self):
        self._sql = "";
        self._data = [];
        
        self._from = "";
        self._whereList = [];
        self._where = "";
        self._group = "";
        self._table = "";
        self._collum = [];
        pass;

    # createTableSQL作成
    def CreateTable(self):
        self._sql = "create table " + self._table + "( "
        i=0;
        for col in self._collum:
            if (len(self._collum) - 1) <= i:
                self._sql += str(self._collum[i]);
            else:
                self._sql += str(self._collum[i] + ",");
            i = i + 1;
        self._sql += " )";
        return self._sql;

    # dropTable作成
    def DropTable(self):
        self._sql = "drop table " + self._table + " ;";
        return self._sql;
    
    # selectSQL作成(テーブル存在確認)
    def TableSelectCount(self):
        self._sql = "SELECT COUNT(*) ct FROM sqlite_master WHERE TYPE='table' AND name='" + self._table + "'";
        return self._sql;
    
    # selectSQL作成
    def Select(self):
        self._sql = "select ";
        
        # column設定
        i=0;
        for col in self._collum:
            if (len(self._collum) - 1) <= i:
                self._sql += str(self._collum[i]);
            else:
                self._sql += str(self._collum[i] + ",");
            i = i + 1;
        # where設定
        self._whereList.insert(0," where 1 = 1 ");
        for where in self._whereList:
            self._where += str(where);
        self._from = " from "+ self._table;
        return self._sql + self._from + self._where;
        
    # insertSQL作成
    def Insert(self):
        self._sql = "insert into "+ self._table + " (";
        
        # column設定
        i=0;
        for col in self._collum:
            if (len(self._collum) - 1) <= i:
                self._sql += str(self._collum[i] + ")");
            else:
                self._sql += str(self._collum[i] + ",");
            i = i + 1;
            
        self._sql += " VALUES (";
        for counter in range(len(self._collum)):
            if (len(self._collum) - 1) <= counter:
                self._sql += "?)";
            else:
                self._sql += "?,";
        return self._sql;
        
    # updateSQL作成
    def Update(self):
        self._sql = "update "+ self._table + " set ";
        
        # collum設定
        i=0;
        for col in self._collum:
            if (len(self._collum) - 1) <= i:
                self._sql += str(self._collum[i] + "");
            else:
                self._sql += str(self._collum[i] + ",");
            i = i + 1;
        # where設定
        self._whereList.insert(0," where 1 = 1 ");
        for where in self._whereList:
            self._where += str(where);
        return self._sql + self._where;

    # deleteSQL作成
    def Delete(self):
        self._sql = "delete from " + self._table + "";
        # where設定
        self._whereList.insert(0," where 1 = 1 ");
        for where in self._whereList:
            self._where += str(where);
        return self._sql + self._where;
    
    # SQL取得(プロパティ)
    def GetSql(self):
        return self._sql; #gettert
    
    # Collum属性
    def SetCollum(self, value):
        self._collum.append(value); #setter
    def ClearCollum(self):
        self._collum = [];
        
    # Where属性
    def SetWhereList(self, value):
        self._whereList.append(value); #setter
    def ClearWhereList(self):
        self._whereList = [];
        self.ClearWhere();
    def ClearWhere(self):
        self._where = "";
        
    # data
    def SetData(self, value):
        self._data.append(value); #setter
    def GetData(self):
        return self._data;
        
    # Table名
    def SetTableName(self, value):
        self._table = value; #setter
    def GetTableName(self):
        return self._table;