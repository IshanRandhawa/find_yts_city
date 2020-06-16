
from django.urls import path   
# importing views from views..py 
from .views import home_view , table 
  

urlpatterns = [ 
    path('', home_view ), 
    path('table' , table ),
] 
