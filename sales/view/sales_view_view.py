'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.URLS import SALES_TRANSACTION, CUSTOMER_LIST,\
    SALES_ORDER_HEADER_STATUS
from django.views import defaults
import json

class sales_view_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        customer_list = json.loads(requests.get(CUSTOMER_LIST).text)
        so_header_statuses = json.loads(requests.get(SALES_ORDER_HEADER_STATUS).text)
        r = requests.get(url = SALES_TRANSACTION) 
        if r.status_code is 200:
            json_data = r.json()
            data= {'customer_list' : customer_list['customerLists'],
                   'header_status' : so_header_statuses['lookup_details'],
                   'sos' : json_data['sales_trx_details']
                   }
            template = jinja_template.get_template('sales/sales-header-view.html')
            return HttpResponse(template.render(request, data=data))
        else:
            return HttpResponse(defaults.server_error(request))
        
    def post(self, request):        
        data = json.loads(request.body)
        search_params = data.copy()
        for key, value in data.items():
            if value == '':
                search_params.pop(key)
        r = requests.get(url = SALES_TRANSACTION, params=search_params) 
        if r.status_code is 200:
            json_data = r.json()
            return HttpResponse(json.dumps(json_data['sales_trx_details']))
        else:
            return HttpResponse(defaults.server_error(request))
                