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
from purchase.view.purchase_view_view import purchase_view_view
from purchase.view.purchase_add_view import purchase_add_view
from django.contrib.auth.decorators import login_required
from purchase.view.purchase_update_view import purchase_update_view
from purchase.view.purchase_receipt_add_view import purchase_receipt_add_view
from purchase.view.purchase_receipt_update_view import purchase_receipt_update_view
from purchase.view.print_purchase_challan import print_purchase_challan
from purchase.view.purchase_view_details import purchase_view_details
from purchase.view.purchase_receipt_cancel_view import purchase_receipt_cancel_view
from purchase.view.receipt_view_view import receipt_view_view
from purchase.view.purchase_close_view import purchase_close_view

urlpatterns = [
    path('', login_required(purchase_view_view.as_view()), name='purchase_view'),
    path('receipt/', login_required(receipt_view_view.as_view()), name='receipt_view'),
    path('<str:transaction_number>/add_receipt/', login_required(purchase_receipt_add_view.as_view()), name='add_purchase_receipt'),
    path('<str:transaction_number>/update_receipt/<str:challan_number>/', login_required(purchase_receipt_update_view.as_view()), name='update_purchase_receipt'),
    path('<str:transaction_number>/cancel_receipt/<str:challan_number>/', login_required(purchase_receipt_cancel_view.as_view()), name='purchase_receipt_cancel'),
    path('<str:transaction_number>/print_challan/<str:challan_number>/', login_required(print_purchase_challan.as_view()), name='print_purchase_challan'),
    path('add/', login_required(purchase_add_view.as_view()), name='purchase_add'),
    path('update/', login_required(purchase_update_view.as_view()), name='purchase_update'),
    path('<str:transaction_number>/', login_required(purchase_view_details.as_view()), name='purchase_details'),
    path('<str:transaction_number>/close_po/', login_required(purchase_close_view.as_view()), name='close_po')
]
