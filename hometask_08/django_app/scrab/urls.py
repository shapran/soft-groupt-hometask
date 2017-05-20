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
    #url(r'^api1/', include(router.urls)),
    #url(r'^api1/', include('rest_framework.urls', namespace='rest_framework'))
    
    #url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    #url(r'^post/new/$', views.post_new, name='post_new'),
    #url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
]
