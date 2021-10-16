from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostViewSet, "posts")
router.register('tags', views.TagViewSet, "tags")
router.register('users', views.UserViewSet, "user")
router.register('categories', views.CategoryViewSet, "category")
router.register('tours', views.TourViewSet, "tour")
router.register('comment-post', views.CommentPostViewSet, "comment-post")
router.register('comment-tour', views.CommentTourViewSet, "comment-tour")
router.register('tour-schedules', views.TourSchedulesViewSet, "tour-schedules")
router.register('tour-images', views.TourImagesViewSet, "tour-images")

urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view()),
    # path('testing/', views.TestView.as_view()),
    # path('welcome/<str:name>/', views.welcome, name="welcome"),
    # re_path(r'^welcome2/(?P<year>[0-9]{2,3})/$', views.welcome2),
    path('admin/', admin_site.urls)
]