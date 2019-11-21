'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.external_urls import PURCHASE_TRANSACTION, SUPPLIER_LIST,\
    PURCHASE_ORDER_HEADER_STATUS
from django.views import defaults
import json

class purchase_view_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        supplier_list = json.loads(requests.get(SUPPLIER_LIST).text)
        po_header_statuses = json.loads(requests.get(PURCHASE_ORDER_HEADER_STATUS).text)
        r = requests.get(url = PURCHASE_TRANSACTION) 
        if r.status_code is 200:
            json_data = r.json()
            data= {'supplier_list' : supplier_list['supplierLists'],
                   'header_status' : po_header_statuses['purchaseOrderHeaderStatus'],
                   'pos' : json_data['purchase_trx_details']
                   }
            template = jinja_template.get_template('purchase/purchase-header-view.html')
            return HttpResponse(template.render(request, data=data))
        else:
            return HttpResponse(defaults.server_error(request))
        
    def post(self, request):        
        data = json.loads(request.body)
        search_params = data.copy()
        for key, value in data.items():
            if value == '':
                search_params.pop(key)
        r = requests.get(url = PURCHASE_TRANSACTION, params=search_params) 
        if r.status_code is 200:
            json_data = r.json()
            return HttpResponse(json.dumps(json_data['purchase_trx_details']))
        else:
            return HttpResponse(defaults.server_error(request))
                