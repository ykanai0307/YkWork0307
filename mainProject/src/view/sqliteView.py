import sys
import glob
import os
import urllib.request
from ..module.dirPath import dirPathClass
from ..module.DataBase import DataBaseClass
from ..module.CreateTable import CreateTableSql
from ..define.DBModeEnum import DBMode
from django.shortcuts import render, redirect
from django.views.generic import View

class sqliteView(View):

  def __init__(self, **kwargs):
      self._var = ''
      self._sql = ''
      self._view_result = ""
      self._data_result = ""
      self._veiwUrl = 'sqlLiteView.html'

  def get(self, request, *args, **kwargs):
      dirPathIns = dirPathClass()
      result = []
      data_result = []
      veiwMesTag = '<label for="mes" class="message">[%_MES_%]</label>'
      BindMes = '[%_MES_%]'
      
      # DB接続
      try:
          #データ表示
          sql = "select name from sqlite_master where type = 'table';"
          docs = self.sql_fetch_all(sql)
          self.view_result(docs,"table")
          result = self.GetResult()
          
          sql = "select * from " + doc[0] + " where 1 = 1;"
          docs = self.sql_fetch_all(sql)
          self.view_result(docs,"data")
          data_result = self.GetResult()
          
          mes = "OK"
      except Exception as e:
          mes = e
      context = {
          'SalesResult': result,
          'SalesDataResult': data_result,
          'message': veiwMesTag.replace(BindMes,str(mes))
      }
      return render(request, self._veiwUrl, context)
    
  def post(self, request, *args, **kwargs):
      context = {
          'message': 'test',
      }
      return render(request, self._veiwUrl, context)
      
  # テーブル作成
  def create_table(request):
      sv = sqliteView()
      veiwMesTag = '<label for="mes" class="message">[%_MES_%]</label>'
      BindMes = '[%_MES_%]'
      mes = ""
      if request.method == 'POST':
          try:
              dbBase = DataBaseClass()
              dbBase.DbConnect(DBMode.SQLITE)
              dbBase.DbCursor()
              sv._sql = CreateTableSql().CreateTableSales();
              print(sv._sql)
              dbBase.DbExecute(sv._sql)
              sv._sql=""
              dbBase.DbCommit()
              mes = "create table成功。"
          except Exception as e:
              dbBase.DbRollback()
              mes = "create table失敗。"
          pass
      else:
          mes = ""
      context = {
          'message': veiwMesTag.replace(BindMes,mes),
      }
      return render(request, sv._veiwUrl, context)
      
  # データ取得
  def sql_fetch_all(self,sql):
      try:
          dbBase = DataBaseClass()
          dbBase.DbConnect(DBMode.SQLITE)
          dbBase.DbCursor()
          
          # レコードを登録
          # persons = [(1, 'Steave'), (2, 'Eric'), (3, 'Mike')]
          # cur.executemany("INSERT INTO members VALUES (?, ?)", persons)

          dbBase.DbExecute(sql)
          # カーソルを取得。
          cursor = dbBase.GetDbCursor()
          return cursor.fetchall()
      except Exception as e:
          return e
          
  # 表示
  def view_result(self,docs,mode):
      _result = []
      _data_result = []
      try:
          for doc in docs:
              if mode == "table":
                  _result.append("<tr class='body'>" + "<td>" + doc[0] + "</td>" + "</tr>")
              elif mode == "data":
                  _result.append("<tr class='body'>" + "<td>" + doc[0] + "</td>" + "</tr>")
          self.SetResult(_result)
      except Exception as e:
          pass

  # 表示用テーブル取得(プロパティ)
  def GetResult(self):
      return self._view_result #getter
        
  def SetResult(self, value):
      self._view_result = value #setter
          
  # 表示用データ取得(プロパティ)
  def GetDataResult(self):
      return self._data_result #getter
        
  def SetDataResult(self, value):
      self._data_result = value #setter