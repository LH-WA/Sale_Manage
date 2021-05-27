"""Sales_Management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from Entity_Info.views import index, logins, regist, logout, show_chart, goods_info_input, supplier_info_input
from Relation_Info.views import company_branch_delivery

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('login/', logins),
    path('regist/', regist),
    path('logout/', logout),
    path('show/', show_chart),
    path('goods_info_input/', goods_info_input),
    path('supplier_info_input/', supplier_info_input),
    path('test/', company_branch_delivery),
]
