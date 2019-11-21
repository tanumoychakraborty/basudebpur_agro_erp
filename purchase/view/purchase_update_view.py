'''
Created on 25-Dec-2018

@author: tanumoy
'''

from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse, HttpResponseRedirect
from basudebpur_agro_erp.permission.purchase_permissions import hasUpdatePurchaseRecordAccess
import json
from basudebpur_agro_erp.external_urls import PURCHASE_TRANSACTION, SUPPLIER_LIST,\
    PURCHASE_ORDER_HEADER_STATUS
import requests
from django.shortcuts import redirect
from django.views import defaults

class purchase_update_view(template):
    '''
    classdocs
    '''
    
    def put(self, request):
        if hasUpdatePurchaseRecordAccess(request.user):
            data = json.loads(request.body)
            data['last_updated_by'] = request.user.username
            #data['transaction_date'] = data['transaction_date'].replace('/', '-')
            for line in data['purchase_trx_lines']:
                if line['booking_unit_price'] == '':
                    line.pop('booking_unit_price')
                if line['booking_quantity'] == '':
                    line.pop('booking_quantity')
                line['last_updated_by'] = request.user.username
                if 'transaction_line_id' not in line.keys():
                    line['created_by'] = request.user.username
                    
            
            jsondata = json.dumps(data)
            r = requests.put('{}'.format(PURCHASE_TRANSACTION), json = jsondata) 
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
        
        