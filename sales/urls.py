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
from sales.view.sales_view_view import sales_view_view
from sales.view.sales_add_view import sales_add_view
from django.contrib.auth.decorators import login_required
from sales.view.sales_view_details import sales_view_details
from sales.view.sales_update_view import sales_update_view
from sales.view.print_sales_challan import print_sales_challan
from sales.view.receipt_view_view import receipt_view_view
from sales.view.sales_receipt_add_view import sales_receipt_add_view
from sales.view.sales_receipt_update_view import sales_receipt_update_view
from sales.view.sales_receipt_cancel_view import sales_receipt_cancel_view
from sales.view.sales_close_view import sales_close_view

urlpatterns = [
    path('', login_required(sales_view_view.as_view()), name='sales_view'),
    path('receipt/', login_required(receipt_view_view.as_view()), name='receipt_view'),
    path('<str:transaction_number>/add_receipt/', login_required(sales_receipt_add_view.as_view()), name='add_sales_receipt'),
    path('<str:transaction_number>/update_receipt/<str:challan_number>/', login_required(sales_receipt_update_view.as_view()), name='update_sales_receipt'),
    path('<str:transaction_number>/cancel_receipt/<str:challan_number>/', login_required(sales_receipt_cancel_view.as_view()), name='sales_receipt_cancel'),
    path('<str:transaction_number>/print_challan/<str:challan_number>/', login_required(print_sales_challan.as_view()), name='print_sales_challan'),
    path('add/', login_required(sales_add_view.as_view()), name='sales_add'),
    path('update/', login_required(sales_update_view.as_view()), name='sales_update'),
    path('<str:transaction_number>/', login_required(sales_view_details.as_view()), name='sales_details'),
    path('<str:transaction_number>/close_so/', login_required(sales_close_view.as_view()), name='close_so')
]
