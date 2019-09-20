'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.URLS import CUSTOMER, CUSTOMER_TYPE
import json
from basudebpur_agro_erp.permission.customer_permissions import hasUpdateCustomerAccess

class customer_view_details(template):
    '''
    classdocs
    '''


    def get(self, request, customer_code):
        r = requests.get(url = CUSTOMER, params = {'customer_code':customer_code}) 
        if r.status_code is 200:
            json_data = r.json()
            customer_details = json_data['customer_details'][0]
            customer_type = json.loads(requests.get(CUSTOMER_TYPE).text)
            if customer_details['effective_from']:
                #customer_details['effective_from'] = customer_details['effective_from'].replace('-', '/')
                customer_details['effective_from'] = customer_details['effective_from'].split(' ')[0]
            if customer_details['effective_to']:
                #customer_details['effective_to'] = customer_details['effective_to'].replace('-', '/')
                customer_details['effective_to'] = customer_details['effective_to'].split(' ')[0]
            for line in customer_details['customer_master_sites']:
                line['last_updated_by'] = request.user.username
#                 if line['inactive_date']:
#                     #line['inactive_date'] = line['inactive_date'].replace('-', '/')
#                     line['inactive_date'] = line['inactive_date'].split(' ')[0]
            
            data= {'customer_code' : customer_type['lookup_details'],
                   'details' : json_data['customer_details'][0]}
            if hasUpdateCustomerAccess(request.user):                
                template = jinja_template.get_template('customer/customer-site-update.html')
                return HttpResponse(template.render(request, data=data))
            else:
                template = jinja_template.get_template('customer/customer-site-view.html')
                return HttpResponse(template.render(request, data=data))
        else:
            template = jinja_template.get_template('internal_server_error.html')
            return HttpResponse(template.render(request))
        