'''
Created on 25-Dec-2018

@author: tanumoy
'''

from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import json
from basudebpur_agro_erp.external_urls import SUPPLIER
import requests
from basudebpur_agro_erp.permission.supplier_permissions import hasUpdateSupplierAccess

class supplier_update_view(template):
    '''
    classdocs
    '''
    
    def put(self, request):
        if hasUpdateSupplierAccess(request.user):
            data = json.loads(request.body)
            if data['enabled_flag']:
                data['enabled_flag'] = 'Y'
            else:
                data['enabled_flag'] = 'N'
            data['last_updated_by'] = request.user.username
            if data['effective_from'] == '':
                data.pop('effective_from')
            if data['effective_to'] == '':
                data.pop('effective_to')
#             if data['effective_from']:
#                 data['effective_from'] = data['effective_from'].replace('/', '-')
#                 #data['effective_from'] = data['effective_from'].split(' ')[0]
#             if data['effective_to']:
#                 data['effective_to'] = data['effective_to'].replace('/', '-')
#                 #data['effective_to'] = data['effective_to'].split(' ')[0]
            for line in data['supplier_master_sites']:
                line['last_updated_by'] = request.user.username
                if 'supplier_site_id' not in line.keys():
                    line['created_by'] = request.user.username
#                 if line['inactive_date']:
#                     line['inactive_date'] = line['inactive_date'].replace('/', '-')
#                     #line['inactive_date'] = line['inactive_date'].split(' ')[0]
            
            jsondata = json.dumps(data)
            r = requests.put(SUPPLIER, json = jsondata) 
            if r.status_code is 200:
                to_json = {'message':'ok'}
                return HttpResponse(json.dumps(to_json))
            
            elif r.status_code == 422:
                to_json = json.loads(r.content)['errors']
                return HttpResponse(json.dumps(to_json), status = 422)
                
            else:
                template = jinja_template.get_template('internal_server_error.html')
                return HttpResponse(template.render(request))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
        
        