from django.conf.urls import url
from . import views

from django.urls import path

urlpatterns = [
    url(r'^$', views.start, name='start'),
    path('all/', views.All.as_view(), name='all'),
    path('home1/', views.Home.as_view(), name='home1'),
    # url(r'^checklist/', views.Home.as_view(), name='home'),
    path('checklist/', views.demo3, name='demo03'),

    path('home2/', views.Home2.as_view(), name='home2'),
    path('home3/', views.Home3.as_view(), name='home3'),
    # path('home2/', views.home2, name='home2'),
    # path('home3/', views.home3, name='home3'),
]
