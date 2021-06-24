import sys
import urllib.request
import datetime                                         # datetime use
from django.shortcuts import render                     # disp rendering
from django.views.generic import View                   # to class
from ..define.DBModeEnum import DBMode                  # DB mode(sqllite mysql)
from ..module.dirPath import dirPathClass               # path class
from ..module.DataBase import DataBaseClass             # DBbase class
from ..module.ViewGrid import ViewGridClass             # view class
from ..module.Redirect import RedirectClass             # Redirect
from ..module.Query import Query                        # all sql
from ..module.SendValueShare import SendValueShareClass # [post get list] convert

class mainView(View):

  # 初期処理
  def __init__(self, **kwargs):
      self._viewIns = None;
      self._sendValIns = None;
      self._sql = '';
      self._veiw = 'mainView.html';
  
  # GET_METHOD
  def get(self, request, *args, **kwargs):
      dirPathIns = dirPathClass();
      qr = Query();
      veiwMesTag = '<label for="mes" class="message">[%_MES_%]</label>';
      BindMes = '[%_MES_%]'
      mes = "";
      redirectIns = RedirectClass();
      
      # DB接続
      try:
          mes = request.GET.get("mes");
          if mes == None:
              mes = "";
          
          dbBase = DataBaseClass();
          self._viewIns = ViewGridClass();
          dbBase.DbConnect(DBMode.SQLITE);
          dbBase.DbCursor();
          
          mainView.SelfSelectTableCount(dbBase,qr);
          result = dbBase.FetchAll();
          if(int(result[0][0]) < 1): # Table not Exist
              # create table make
              self.SelfCreateTable(dbBase,qr,self);
          
          # select
          mainView.SelfSelect(dbBase,qr);
          # view create
          self._viewIns.SetData(dbBase.FetchAll());
          self._viewIns.CreateGrid();
          # db close
          dbBase.DbCloseCursor();
          dbBase.DbClose();
          
          context = {
            'message': veiwMesTag.replace(BindMes,mes),
            'SalesResult': self._viewIns.GetGrid(),
            'PlotGrafImg': '<img class="GrafImg" src="' + dirPathIns.GetUrlHost() + dirPathIns.GetSelfToStaticImgRelativeDirPath() + 'out.png' + '" alt="Graph" title="分析結果">',
          }
      except Exception as e:
          print('[DB Connection Error]', e)
          sys.exit(1) # プログラムをエラー終了
      
      return render(request, self._veiw, context)
  
  # POST_METHOD
  def post(self, request, *args, **kwargs):
      context = {
          'message': 'test',
      }
      return render(request, self._veiw, context)
  
  # DB_CREATE_TABLE
  def db_create_table(request):
      Mv = mainView();
      redirectIns = RedirectClass();
      qr = Query();
      Mv._viewIns = ViewGridClass();
      mes = "";
      if request.method == 'POST':
          dbBase = DataBaseClass();
          try:
              # open
              dbBase.DbConnect(DBMode.SQLITE);
              # create table make
              mainView.SelfCreateTable(dbBase,qr,Mv);
              # view create
              Mv._viewIns.CreateGrid();
              # submit
              dbBase.DbCloseCursor();
              dbBase.DbCommit();
              mes = qr.GetTableName() + " create success";
          except Exception as e:
              dbBase.DbRollback();
              mes = qr.GetTableName() + " create failed [" + str(e) + "]";
          dbBase.DbClose();
          pass
      else:
          mes = "";
      redirectIns.SetUrl('main');
      redirectIns.SetParam('mes=' + mes);
      return redirectIns.RedirectParam(); # redirect
      
  # DB_DROP_TABLE
  def db_drop_table(request):
      Mv = mainView();
      redirectIns = RedirectClass();
      qr = Query();
      mes = "";
      if request.method == 'POST':
          dbBase = DataBaseClass();
          try:
              # open
              dbBase.DbConnect(DBMode.SQLITE);
              # drop make
              mainView.SelfDropTable(dbBase,qr,Mv);
              # submit
              dbBase.DbCommit();
              mes = qr.GetTableName() + " drop success";
          except Exception as e:
              dbBase.DbRollback();
              mes = qr.GetTableName() + " drop failed [" + str(e) + "]";
          dbBase.DbClose();
          pass
      else:
          mes = "";
      redirectIns.SetUrl('main');
      redirectIns.SetParam('mes=' + mes);
      return redirectIns.RedirectParam(); # redirect
      
  # DB_DELETE_TABLE
  def db_delete_table(request):
      Mv = mainView();
      redirectIns = RedirectClass();
      qr = Query();
      Mv._viewIns = ViewGridClass();
      mes = "";
      if request.method == 'POST':
          dbBase = DataBaseClass();
          try:
              # open
              dbBase.DbConnect(DBMode.SQLITE);
              # delete make
              mainView.SelfDelete(dbBase,qr,Mv);
              # submit
              dbBase.DbCommit();
              dbBase.DbCloseCursor();
              
              mes = qr.GetTableName() + " delete success";
          except Exception as e:
              dbBase.DbRollback();
              mes = qr.GetTableName() + " delete failed [" + str(e) + "]";
          dbBase.DbClose();
          pass
      else:
          mes = "";
      redirectIns.SetUrl('main');
      redirectIns.SetParam('mes=' + mes);
      return redirectIns.RedirectParam(); # redirect
      
  # DB_INSERT_TABLE
  def db_insert_table(request):
      Mv = mainView();
      redirectIns = RedirectClass();
      qr = Query();
      mes = "";
      Mv._viewIns = ViewGridClass();
      Mv._sendValIns = SendValueShareClass();
      if request.method == 'POST':
          
          # post value convert
          Mv._sendValIns.SetRequest(request);
          Mv._sendValIns.SetCollum('check');
          Mv._sendValIns.SetCollum('Txt');
          Mv._sendValIns.SetCollum('Word');
          Mv._sendValIns.SetCollum('Excel');
          Mv._sendValIns.SetCollum('Active');
          Mv._sendValIns.SendDataConversion();
          
          dbBase = DataBaseClass();
          try:
              # open
              dbBase.DbConnect(DBMode.SQLITE);
              # insert make
              mainView.SelfInsert(dbBase,qr,Mv._sendValIns.GetResult());
              # select
              mainView.SelfSelect(dbBase,qr);
              # view create
              Mv._viewIns.SetData(dbBase.FetchAll());
              Mv._viewIns.CreateGrid();
              
              # submit
              dbBase.DbCommit();
              dbBase.DbCloseCursor();
              
              mes = qr.GetTableName() + " insert success";
          except Exception as e:
              dbBase.DbRollback();
              mes = qr.GetTableName() + " insert failed [" + str(e) + "]";
          dbBase.DbClose();
      else:
          mes = "";
      redirectIns.SetUrl('main');
      redirectIns.SetParam('mes=' + mes);
      return redirectIns.RedirectParam(); # redirect
      
  # (privateMethod)creat table
  @classmethod
  def SelfCreateTable(cls,dbBase,sqlClass,SelfClass):
      try:
          dbBase.DbCursor();
          sqlClass.SetTableName("CopyTable");
          sqlClass.SetCollum("No INTEGER PRIMARY KEY AUTOINCREMENT");
          sqlClass.SetCollum("Txt TEXT DEFAULT NULL");
          sqlClass.SetCollum("Word TEXT NOT NULL DEFAULT \"\"");
          sqlClass.SetCollum("Excel TEXT NOT NULL DEFAULT \"\"");
          sqlClass.SetCollum("CreateDate TIMESTAMP DEFAULT NULL");
          sqlClass.SetCollum("Active INTEGER NOT NULL DEFAULT '0'");
          cls._sql = sqlClass.CreateTable();
          dbBase.DbExecute(cls._sql);
          sqlClass.ClearCollum();
      except Exception as e:
          raise;
          
  # (privateMethod)drop table
  @classmethod
  def SelfDropTable(cls,dbBase,sqlClass,SelfClass):
      try:
          dbBase.DbCursor();
          sqlClass.SetTableName("CopyTable");
          cls._sql = sqlClass.DropTable();
          dbBase.DbExecute(cls._sql);
          dbBase.DbCloseCursor();
      except Exception as e:
          raise;

  # (privateMethod)selectTableCount
  @classmethod
  def SelfSelectTableCount(cls,dbBase,sqlClass):
      try:
          sqlClass.SetTableName("CopyTable");
          cls._sql = sqlClass.TableSelectCount();
          dbBase.DbExecute(cls._sql);
      except Exception as e:
          raise;
          
  # (privateMethod)select
  @classmethod
  def SelfSelect(cls,dbBase,sqlClass):
      try:
          sqlClass.SetTableName("CopyTable");
          sqlClass.SetCollum("No");
          sqlClass.SetCollum("Txt");
          sqlClass.SetCollum("Word");
          sqlClass.SetCollum("Excel");
          sqlClass.SetCollum("CreateDate");
          sqlClass.SetCollum("Active");
          cls._sql = sqlClass.Select();
          sqlClass.ClearCollum();
          dbBase.DbExecute(cls._sql);
      except Exception as e:
          raise;
     
  # (privateMethod)insert
  @classmethod
  def SelfInsert(cls,dbBase,sqlClass,formData):
      try:
          dbBase.DbCursor();
          sqlClass.SetTableName("CopyTable");
          sqlClass.SetCollum("Txt");
          sqlClass.SetCollum("Word");
          sqlClass.SetCollum("Excel");
          sqlClass.SetCollum("CreateDate");
          sqlClass.SetCollum("Active");
          cls._sql = sqlClass.Insert();
          sqlClass.ClearCollum();
          dbBase.DbExecuteMany(cls._sql,formData);
      except Exception as e:
          raise;
          
  # (privateMethod)delete
  @classmethod
  def SelfDelete(cls,dbBase,sqlClass,SelfClass):
      try:
          dbBase.DbCursor();
          sqlClass.SetTableName("CopyTable");
          cls._sql = sqlClass.Delete();
          dbBase.DbExecute(cls._sql);
      except Exception as e:
          raise;