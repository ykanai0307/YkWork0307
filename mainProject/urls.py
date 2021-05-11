from django.urls import path
from django.conf.urls import url
from .src.view.mainView import mainView
from .src.view.sqliteView import sqliteView

urlpatterns = [
    url(r'^$', mainView.as_view(), name='yk'),
    path(r'file_upload', mainView.file_upload, name='yk_upload'),
    path(r'file_tokenizer', mainView.file_tokenizer, name='yk_tokenizer'),
    path(r'file_download', mainView.file_download, name='yk_download'),
    path(r'sql_lite_view', sqliteView.as_view(), name='yk_sql_lite_view'),
    path(r'sql_lite_create_table', sqliteView.create_table, name='yk_sql_lite_create_table'),
]