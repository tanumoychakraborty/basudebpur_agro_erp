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
from supplier.view.supplier_view_view import supplier_view_view
from supplier.view.supplier_add_view import supplier_add_view
from supplier.view.supplier_update_view import supplier_update_view
from supplier.view.supplier_view_details import supplier_view_details
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(supplier_view_view.as_view()), name='supplier_view'),
    path('add/', login_required(supplier_add_view.as_view()), name='supplier_add'),
    path('update/', login_required(supplier_update_view.as_view()), name='supplier_update'),
    path('<str:supplier_code>/', login_required(supplier_view_details.as_view()), name='supplier_details'),
]
