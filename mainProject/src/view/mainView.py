import sys
import glob
import os
import urllib.request
import chardet
import MySQLdb
import matplotlib.pyplot as plt # 折れ線グラフ
from ..module.tokenizerMain import tokenizerMainClass
from ..module.dirPath import dirPathClass
from ..module.DataBase import DataBaseClass
from ..define.DBModeEnum import DBMode
from django.shortcuts import render, redirect
from pprint import pprint
from os.path import abspath, join, split
from django.views.generic import View
from django.core.files.storage import FileSystemStorage

class mainView(View):

  def __init__(self, **kwargs):
      self._var = ''      
      self.__veiwUrl = 'mainView.html'

  def get(self, request, *args, **kwargs):
      dirPathIns = dirPathClass()
      
      # DB接続
      try:
          dbBase = DataBaseClass()
          dbBase.DbConnect(DBMode.MYSQL)
          dbBase.DbCursor()
          
          # レコードを登録
          # persons = [(1, 'Steave'), (2, 'Eric'), (3, 'Mike')]
          # cur.executemany("INSERT INTO members VALUES (?, ?)", persons)
          
          sql = "SELECT ProductName,SalesShopCode,ProductCode,SUM(ProductSalesPrice) ProductSalesPriceSum,YEAR(SalesDate) SalesDateY FROM SalesTable group by YEAR(SalesDate);"
          dbBase.DbExecute(sql)
          # カーソルを取得。
          cursor = dbBase.GetDbCursor()
          docs = cursor.fetchall()
          yearlist = []
          salesMoneylist = []
          for doc in docs:
              yearlist.append(int(doc[4]));
              salesMoneylist.append(doc[3])
              self._var += "<tr class='body'>" + "<td>" + doc[0] + "</td>" + "<td>" + doc[1] + "</td>" + "<td>" + doc[2] + "</td>" + "<td>" + str(doc[3]) + "</td>" + "<td>" + str(doc[4]) + "</td>" + "</tr>"
          x = yearlist
          y = salesMoneylist
          
          plt.plot(x, y);
          plt.xlabel("売上日(年)",size="medium", color="blue",fontname="MS Gothic")
          plt.ylabel("商品売上",labelpad=1, weight="bold" ,size = "medium",rotation="horizontal",fontname="MS Gothic")
          plt.savefig(dirPathIns.GetSelfToStaticImgDir() + 'out.png')
          plt.close()
          context = {
            'message': "",
            'SalesResult': self._var,
            'PlotGrafImg': '<img class="GrafImg" src="' + dirPathIns.GetUrlHost() + dirPathIns.GetSelfToStaticImgRelativeDirPath() + 'out.png' + '" alt="Graph" title="分析結果">',
          }
      except Exception as e:
          print('[DB Connection Error]', e)
          sys.exit(1) # プログラムをエラー終了
      
      return render(request, self.__veiwUrl, context)
    
  def post(self, request, *args, **kwargs):
      context = {
          'message': 'test',
      }
      return render(request, self.__veiwUrl, context)
  
  # ファイルアップロード
  def file_upload(request):
      mes = ""
      errFlg = False
      dirPathIns = dirPathClass()
      veiwMesTag = '<label for="mes" class="message">[%_MES_%]</label>'
      BindMes = '[%_MES_%]'
      if request.method == 'POST':
          if not 'FileAttach' in request.FILES:
              errFlg = True
              mes = 'ファイルを選択してください。'
          if not (errFlg):
              file_obj = request.FILES['FileAttach']
              file_name = file_obj.name
              if not (os.path.isfile(file_name)):
                  fs = FileSystemStorage(location=dirPathIns.GetSelfToStaticUploadDirPath())
                  filename = fs.save(file_name, file_obj)
                  mes = filename + ' ： upload成功。'
              else:
                  mes = file_name + ' ： upload失敗。(既に存在します。)'
      else:
          mes = ""
      context = {
          'message': veiwMesTag.replace(BindMes,mes),
      }
      return render(request, 'mainView.html', context)
      
  # ファイル品詞分解
  def file_tokenizer(request):
      mes = ""
      dirPathIns = dirPathClass()
      veiwMesTag = '<label for="mes" class="message">[%_MES_%]</label>'
      BindMes = '[%_MES_%]'
      if request.method == 'POST':
          # メイン処理
          os.chdir(dirPathIns.GetSelfToStaticUploadDirPath())
          FileDocxList = glob.glob('*.docx')
          tokenizerMainIns = tokenizerMainClass()
          result = tokenizerMainIns.MainToManyFile(FileDocxList)
          mes = "品詞解析成功。"
      else:
          mes = ""
      
      context = {
          'message': veiwMesTag.replace(BindMes,mes),
      }
      return render(request, 'mainView.html', context)
      
  # ファイルダウンロード
  def file_download(request):
      mes = ""
      dirPathIns = dirPathClass()
      veiwMesTag = '<label for="mes" class="message">[%_MES_%]</label>'
      BindMes = '[%_MES_%]'
      if request.method == 'POST':
          # メイン処理
          url = dirPathIns.GetUrlHost() + dirPathIns.GetSelfToStaticResultRelativeDirPath() + r"result.csv"
          save_dir = dirPathIns.GetOutDir()
          save_path = save_dir + "result.csv"
          try:
              if (os.path.isdir(save_dir)):
                      urllib.request.urlretrieve(url, save_path)
                      mes = save_path + ":保存完了。"
              else:
                  os.mkdir(save_dir)
                  urllib.request.urlretrieve(url, save_path)
                  mes = save_path + ":保存完了。"
          except Exception as e:
              mes = e
      else:
          mes = ""
      context = {
          'message': veiwMesTag.replace(BindMes,mes),
      }
      return render(request, 'mainView.html', context)