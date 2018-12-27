'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.URLS import SUPPLIER, SUPPLIER_TYPE
import json
from basudebpur_agro_erp.permission.supplier_permissions import hasUpdateSupplierAccess

class supplier_view_details(template):
    '''
    classdocs
    '''


    def get(self, request, supplier_code):
        r = requests.get(url = SUPPLIER, params = {'supplier_code':supplier_code}) 
        if r.status_code is 200:
            json_data = r.json()
            
            if hasUpdateSupplierAccess(request.user):
                supplier_type = json.loads(requests.get(SUPPLIER_TYPE).text)
            
                data= {'supplier_code' : supplier_type['lookup_details'],
                       'details' : json_data['supplier_details'][0]}
                
                template = jinja_template.get_template('supplier/supplier-site-update.html')
                return HttpResponse(template.render(request, data=data))
            else:
                template = jinja_template.get_template('supplier/sales-site-view.html')
                return HttpResponse(template.render(request, data=json_data[0]))
        else:
            template = jinja_template.get_template('internal_server_error.html')
            return HttpResponse(template.render(request))
        