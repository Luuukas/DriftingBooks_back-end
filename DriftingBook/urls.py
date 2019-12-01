"""DriftingBook URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import Userdb
from . import register

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('addUser/', Userdb.addUser),
    path('delUser/', Userdb.delUser),
    path('uploadajax/', Userdb.upload),
    path('getBookInfos/', Userdb.getBookInfos),
    path('addBook/', Userdb.addBook),
    path('login/', Userdb.login),
    path('get_sms/', register.send_sms_view),
    path('register/', register.register)
]
