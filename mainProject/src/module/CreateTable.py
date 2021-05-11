# CreateTable Sqlクラス
class CreateTableSql:
    
    # コンストラクタ
    def __init__(self):
        self._sql = ""
        pass

    # SalesTable作成
    def CreateTableSales(self):
        self._sql = "create table SalesTable( "
        self._sql += "No INTEGER,"
        self._sql += "SalesDate TIMESTAMP NOT NULL DEFAULT \"1900/01/01 01:01:01\","
        self._sql += "ProductName TEXT,"
        self._sql += "SalesShopCode TEXT NOT NULL DEFAULT \"00000000\","
        self._sql += "ProductCode TEXT NOT NULL DEFAULT \"00000000\","
        self._sql += "ProductSalesPrice TEXT NOT NULL DEFAULT 0,"
        self._sql += "CreateDate TIMESTAMP DEFAULT NULL,"
        self._sql += "Active INTEGER NOT NULL DEFAULT '0',"
        self._sql += "PRIMARY KEY (No,ProductCode)"
        self._sql += " )"
        return self._sql
        
    # SQL取得(プロパティ)
    def GetSql(self):
        return self._sql #getter