'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.external_urls import CUSTOMER_SEARCH, CUSTOMER_TYPE
from django.views import defaults
import json
from basudebpur_agro_erp.util import clearDictionary

class customer_view_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        customer_type = json.loads(requests.get(CUSTOMER_TYPE).text)
        r = requests.get(url = CUSTOMER_SEARCH) 
        if r.status_code is 200:
            json_data = r.json()
            data= {'customer_type' : customer_type['lookup_details'],
                   'customers' : clearDictionary(json_data['customer_details'], '')}
            template = jinja_template.get_template('customer/customer-header-view.html')
            return HttpResponse(template.render(request, data=data))
        else:
            return HttpResponse(defaults.server_error(request))
        
    def post(self, request):        
        data = json.loads(request.body)
        search_params = data.copy()
        for key, value in data.items():
            if value == '':
                search_params.pop(key)
        r = requests.get(url = CUSTOMER_SEARCH, params=search_params) 
        if r.status_code is 200:
            json_data = r.json()
            return HttpResponse(json.dumps(json_data['customer_details']))
        else:
            return HttpResponse(defaults.server_error(request))
                