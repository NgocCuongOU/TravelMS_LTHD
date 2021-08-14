from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('tags', views.TagViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('testing/', views.TestView.as_view()),
    # path('welcome/<str:name>/', views.welcome, name="welcome"),
    # re_path(r'^welcome2/(?P<year>[0-9]{2,3})/$', views.welcome2),
    path('admin/', admin_site.urls)
]