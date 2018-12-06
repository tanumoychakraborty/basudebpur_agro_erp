"""basudebpur_agro_erp URL Configuration

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
from django.urls import path
from login.view.login_view import login_view
from login.view.logout_view import logout_view
from login.view.home_view import home_view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', login_view.as_view(), name='login'),
    path('logout/', logout_view.as_view(), name='logout'),
    path('', login_required(home_view.as_view()), name='home'),
]
