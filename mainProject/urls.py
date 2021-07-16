from django.urls import path
from django.conf.urls import url
from .src.view.menuView import menuView
from .src.view.mainView import mainView
from .src.view.calendarView import calendarView

urlpatterns = [
    url(r'^$', menuView.as_view(), name='menu'),
    path(r'logout', menuView.logout, name='logout'),
    path(r'main', mainView.as_view(), name='main'),
    path(r'db_create_table', mainView.db_create_table, name='yk_db_create_table'),
    path(r'db_delete_table', mainView.db_delete_table, name='yk_db_delete_table'),
    path(r'db_drop_table', mainView.db_drop_table, name='yk_db_drop_table'),
    path(r'db_insert_table', mainView.db_insert_table, name='yk_db_insert_table'),
    
    path(r'calendar_view', calendarView.as_view(), name='calendar'),
    path(r'calendar_create', calendarView.create, name='yk_calendar_create'),
    path(r'calendar_popup_click', calendarView.popup_click, name='yk_calendar_popup_click'),
]