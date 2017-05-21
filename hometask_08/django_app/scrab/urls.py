##from django.shortcuts import render

# Create your views here.


from django.conf.urls import url, include
from . import views
from rest_framework import routers
from django.shortcuts import render, get_object_or_404

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
     
    url(r'^coin/(?P<coin>[\w]+)/$', views.coin_rate, name='coin_rate'),
    url(r'^search/$', views.search, name='search'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
