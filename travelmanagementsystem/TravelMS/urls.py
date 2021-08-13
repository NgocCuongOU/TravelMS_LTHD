from django.contrib import admin
from django.urls import path, re_path
from . import views
from .admin import admin_site

urlpatterns = [
    path('', views.index, name="index"),
    path('testing/', views.TestView.as_view()),
    path('welcome/<str:name>/', views.welcome, name="welcome"),
    re_path(r'^welcome2/(?P<year>[0-9]{2,3})/$', views.welcome2),
    path('admin/', admin_site.urls)
]