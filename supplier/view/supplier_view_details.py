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
            supplier_details = json_data['supplier_details'][0]
            
            if hasUpdateSupplierAccess(request.user):
                supplier_type = json.loads(requests.get(SUPPLIER_TYPE).text)
                if 'effective_from' in supplier_details:
                    supplier_details['effective_from'] = supplier_details['effective_from'].replace('-', '/')
                    supplier_details['effective_from'] = supplier_details['effective_from'].split(' ')[0]
                if 'effective_to' in supplier_details:
                    supplier_details['effective_to'] = json_data['effective_to'].replace('-', '/')
                    supplier_details['effective_to'] = supplier_details['effective_to'].split(' ')[0]
                if 'supplier_master_sites' in supplier_details:
                    for line in supplier_details['supplier_master_sites']:
                        line['last_updated_by'] = request.user.username
                        if 'inactive_date' in line:
                            line['inactive_date'] = line['inactive_date'].replace('-', '/')
                            line['inactive_date'] = line['inactive_date'].split(' ')[0]
                
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
        