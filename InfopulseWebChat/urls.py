"""InfopulseWebChat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

from InfopulseWebChatApp.admin_page import get_all_users, add_user_to_ban, delete_user_from_ban
from InfopulseWebChatApp.views import IndexController, RegistrationController, LoginController, AdminController, \
    ChatController, BanController



urlpatterns = [
    url(r'^$',IndexController.as_view(),name="index"),
    url(r'^registration$',RegistrationController.as_view(),name="registration"),
    url(r'^login$',LoginController.as_view(),name="login"),
    url(r'^admin$',AdminController.as_view(),name="admin"),
    url(r'^chat$',ChatController.as_view(),name="chat"),
    url(r'^ban$',BanController.as_view(),name="ban"),
    url(r'^getusers$',get_all_users,name="get_users"),
    url(r'^add_user$',add_user_to_ban, name="add_user"),
    url(r'^del_user/(\d+)$', delete_user_from_ban,name="del_user")
]
