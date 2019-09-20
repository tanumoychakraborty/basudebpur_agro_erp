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
from customer.view.customer_view_view import customer_view_view
from customer.view.customer_add_view import customer_add_view
from customer.view.customer_update_view import customer_update_view
from customer.view.customer_view_details import customer_view_details
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(customer_view_view.as_view()), name='customer_view'),
    path('add/', login_required(customer_add_view.as_view()), name='customer_add'),
    path('update/', login_required(customer_update_view.as_view()), name='customer_update'),
    path('<str:customer_code>/', login_required(customer_view_details.as_view()), name='customer_details'),
]
