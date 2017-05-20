"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

'''
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
'''

from django.conf.urls import include, url
from django.contrib import admin
import blog.urls
from rest_framework import routers
from scrab import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'coins', views.CoinViewSet)
router.register(r'rating', views.RatingViewSet)
router.register(r'groups', views.GroupViewSet)

 

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    ##url(r'^b/', include('blog.urls')),
    url(r'', include('scrab.urls')),
    url(r'^api/', include(router.urls)),
    #url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    
]
