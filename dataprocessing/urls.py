
from django.urls import path 
from . import views
  
app_name = 'dataprocessing'
urlpatterns = [ 
    path('', views.home_view, name = 'home'),
    path('database' , views.table, name = 'database'),
    path('subtable/query/city', views.subtable, name ='subtable')
    # path('subtable' , views.subtable, name = 'subtable'),
]