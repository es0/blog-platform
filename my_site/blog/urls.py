from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    #path('',views.home, name="home"),
    #re_path(r'^$', views.post_list, name="post_list"),
    re_path(r'^$', views.PostListView.as_view(), name='post_list'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',views.post_detail, name="post_detail"),
    ]
