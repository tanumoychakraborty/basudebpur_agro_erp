'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import json
from basudebpur_agro_erp.external_urls import CUSTOMER_TYPE, CUSTOMER
import requests
from basudebpur_agro_erp.permission.customer_permissions import hasAddCustomerAccess

class customer_add_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        if hasAddCustomerAccess(request.user):
            customer_type = json.loads(requests.get(CUSTOMER_TYPE).text)
            
            data= {'customer_type' : customer_type['lookup_details'] }
            template = jinja_template.get_template('customer/customer-site-add.html')
            return HttpResponse(template.render(request, data={'details' : data}))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
    
    def post(self, request):
        if hasAddCustomerAccess(request.user):
            data = json.loads(request.body)
            data['created_by'] = request.user.username
            data['last_updated_by'] = request.user.username
            if data['effective_from'] == '':
                data.pop('effective_from')
            if data['effective_to'] == '':
                data.pop('effective_to')
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
            for line in data['customer_master_sites']:
                line['created_by'] = request.user.username
                line['last_updated_by'] = request.user.username
#                 if line['inactive_date']:
#                     line['inactive_date'] = line['inactive_date'].replace('/', '-')
#                     #line['inactive_date'] = line['inactive_date'].split(' ')[0]
            jsondata = json.dumps(data)
            
            r = requests.post(url = CUSTOMER, json = jsondata)
            if r.status_code is 200:
                to_json = {'message':'ok'}
                return HttpResponse(json.dumps(to_json))
            elif r.status_code == 422:
                to_json = json.loads(r.content)['errors']
                return HttpResponse(json.dumps(to_json), status = 422)
            else:
                template = jinja_template.get_template('./internal_server_error.html')
                return HttpResponse(template.render(request))
        else:
            template = jinja_template.get_template('./access_denied.html')
            return HttpResponse(template.render(request))
        
