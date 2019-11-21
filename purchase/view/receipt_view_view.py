'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.external_urls import RECEIPT, RECEIPT_HEADER_STATUS
from django.views import defaults
import json

class receipt_view_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        receipt_header_statuses = json.loads(requests.get(RECEIPT_HEADER_STATUS).text)
        r = requests.get(url = RECEIPT, params={'source_transaction_type':'PURCHASE'}) 
        if r.status_code is 200:
            json_data = r.json()
            data= {'header_status' : receipt_header_statuses['lookup_details'],
                   'pos' : json_data['receipt_details']
                   }
            template = jinja_template.get_template('purchase/purchase-search-receipt.html')
            return HttpResponse(template.render(request, data=data))
        else:
            return HttpResponse(defaults.server_error(request))
        
    def post(self, request):        
        data = json.loads(request.body)
        search_params = data.copy()
        search_params['source_transaction_type'] = 'PURCHASE'
        for key, value in data.items():
            if value == '':
                search_params.pop(key)
        r = requests.get(url = RECEIPT, params=search_params) 
        if r.status_code is 200:
            json_data = r.json()
            return HttpResponse(json.dumps(json_data['receipt_details']))
        else:
            return HttpResponse(defaults.server_error(request))
                