import sys
import urllib.request
from django.shortcuts import render                     # disp rendering
from django.views.generic import View                   # to class

class menuView(View):

  # 初期処理
  def __init__(self, **kwargs):
      self._mes = '';
      self._veiw = 'menuView.html';
  
  # GET_METHOD
  def get(self, request, *args, **kwargs):
      try:
          context = {
            'message': self._mes,
          }
      except Exception as e:
          print('[DB Connection Error]', e)
          sys.exit(1) # プログラムをエラー終了
      
      return render(request, self._veiw, context)
  
  # POST_METHOD
  def post(self, request, *args, **kwargs):
      context = {
          'message': 'test',
      };
      return render(request, self._veiw, context);