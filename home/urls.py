
from django.urls import path,include
from .views import *

urlpatterns = [
    
    path('' , home , name="home"),
    path('course/<slug>' ,view_course , name="course"),
    path('Contact', contact, name="Contact"),
    path('become_pro/' , become_pro , name="become_pro"),
    path('charge/' , charge , name="charge"),
    path('login/'  , login_attempt , name="login"),
    path('register/'  ,signup , name="register"),
    path('search',search, name="search"),
    path('about',about, name='about'),
    path('logout_attempt/' , logout_attempt , name="logout")
    
  
]