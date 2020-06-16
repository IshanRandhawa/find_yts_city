
from django.urls import path 
from . import views
  
app_name = 'dataprocessing'
urlpatterns = [ 
    path('', views.home_view, name = 'home'), 
    path('table' , views.table, name = 'table'),
    path('subtable/<str:query>' , views.subtable, name = 'subtable'),
]