from django.urls import path
from django.conf.urls import url
from .src.view.mainView import mainView
from .src.view.sqliteView import sqliteView

urlpatterns = [
    url(r'^$', mainView.as_view(), name='main'),
    path(r'db_create_table', mainView.db_create_table, name='yk_db_create_table'),
    path(r'db_delete_table', mainView.db_delete_table, name='yk_db_delete_table'),
    path(r'db_drop_table', mainView.db_drop_table, name='yk_db_drop_table'),
    path(r'db_insert_table', mainView.db_insert_table, name='yk_db_insert_table'),
    path(r'sql_lite_view', sqliteView.as_view(), name='yk_sql_lite_view'),
    path(r'sql_lite_create_table', sqliteView.create_table, name='yk_sql_lite_create_table'),
]