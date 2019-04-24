'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import json
from basudebpur_agro_erp.URLS import SUPPLIER_TYPE, SUPPLIER
import requests
from basudebpur_agro_erp.permission.supplier_permissions import hasAddSupplierAccess

class supplier_add_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        if hasAddSupplierAccess(request.user):
            supplier_type = json.loads(requests.get(SUPPLIER_TYPE).text)
            
            data= {'supplier_type' : supplier_type['lookup_details'] }
            template = jinja_template.get_template('supplier/supplier-site-add.html')
            return HttpResponse(template.render(request, data=data))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
    
    def post(self, request):
        if hasAddSupplierAccess(request.user):
            data = json.loads(request.body)
            data['created_by'] = request.user.username
            data['last_updated_by'] = request.user.username
            if data['enabled_flag']:
                data['enabled_flag'] = 'Y'
            else:
                data['enabled_flag'] = 'N'
#             if data['effective_from']:
#                 data['effective_from'] = data['effective_from'].replace('/', '-')
#                 #data['effective_from'] = data['effective_from'].split(' ')[0]
#             if data['effective_to']:
#                 data['effective_to'] = data['effective_to'].replace('/', '-')
#                 #data['effective_to'] = data['effective_to'].split(' ')[0]
            for line in data['supplier_master_sites']:
                line['created_by'] = request.user.username
                line['last_updated_by'] = request.user.username
#                 if line['inactive_date']:
#                     line['inactive_date'] = line['inactive_date'].replace('/', '-')
#                     #line['inactive_date'] = line['inactive_date'].split(' ')[0]
            jsondata = json.dumps(data)
            
            r = requests.post(url = SUPPLIER, json = jsondata)
            if r.status_code is 200:
                to_json = {'message':'ok'}
                return HttpResponse(json.dumps(to_json))
            else:
                template = jinja_template.get_template('./internal_server_error.html')
                return HttpResponse(template.render(request))
        else:
            template = jinja_template.get_template('./access_denied.html')
            return HttpResponse(template.render(request))
        
