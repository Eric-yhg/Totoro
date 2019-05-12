"""Totoro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from cmdb import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', views.acc_login,name="acc_login"),
    url(r'^accounts/logout/$', views.acc_logout, name="acc_logout"),
    url(r'^register/', views.register),
    url(r'^User_list/', views.User_list, name="User_list"),
    url(r'^User_add/', views.User_add, name="User_add"),
    url(r'^User_del/(.+)/$', views.User_del, name="User_del"),
    url(r'^User_edit/(.+)/$', views.User_edit, name="User_edit"),
    url(r'^asset/', views.asset, name="asset"),
    # url(r'^report/', views.report, name='report'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^index/', views.index, name='index'),
    url(r'^detail/(?P<asset_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^$', views.index),

]
