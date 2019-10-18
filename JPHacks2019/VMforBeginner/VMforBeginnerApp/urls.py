from django.conf.urls import url
from . import views

from django.urls import path
 
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    # url(r'^checklist/', views.Home.as_view(), name='home'),
    path('checklist/', views.demo3, name='demo03'),
]