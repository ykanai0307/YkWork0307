# CreateTable Sqlクラス
class CreateTableSql:
    
    # コンストラクタ
    def __init__(self):
        self._sql = ""
        pass

    # SalesTable登録
    def InsertTableSales(self):
        self._sql = "insert into SalesTable( "
        #self._sql += "No INTEGER,"
        self._sql += "SalesDate ,"
        self._sql += "ProductName ,"
        self._sql += "SalesShopCode ,"
        self._sql += "ProductCode ,"
        self._sql += "ProductSalesPrice ,"
        self._sql += "CreateDate ,"
        self._sql += "Active"
        self._sql += " )"
        return self._sql
        
    # SQL取得(プロパティ)
    def GetSql(self):
        return self._sql #getter