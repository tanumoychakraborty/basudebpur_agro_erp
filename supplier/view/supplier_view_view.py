'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.external_urls import SUPPLIER_SEARCH, SUPPLIER_TYPE
from django.views import defaults
import json

class supplier_view_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        supplier_type = json.loads(requests.get(SUPPLIER_TYPE).text)
        r = requests.get(url = SUPPLIER_SEARCH) 
        if r.status_code is 200:
            json_data = r.json()
            data= {'supplier_type' : supplier_type['lookup_details'],
                   'suppliers' : json_data['supplier_details'] }
            template = jinja_template.get_template('supplier/supplier-header-view.html')
            return HttpResponse(template.render(request, data=data))
        else:
            return HttpResponse(defaults.server_error(request))
        
    def post(self, request):        
        data = json.loads(request.body)
        search_params = data.copy()
        for key, value in data.items():
            if value == '':
                search_params.pop(key)
        r = requests.get(url = SUPPLIER_SEARCH, params=search_params) 
        if r.status_code is 200:
            json_data = r.json()
            return HttpResponse(json.dumps(json_data['supplier_details']))
        else:
            return HttpResponse(defaults.server_error(request))
                