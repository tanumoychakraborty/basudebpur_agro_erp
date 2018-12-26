'''
Created on 25-Dec-2018

@author: tanumoy
'''

from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse, HttpResponseRedirect
from basudebpur_agro_erp.permission.purchase_permissions import hasUpdatePurchaseRecordAccess
import json
from basudebpur_agro_erp.URLS import PURCHASE_TRANSACTION, SUPPLIER_LIST,\
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
            data['transaction_date'] = data['transaction_date'].replace(' ','T')
            for line in data['purchase_trx_lines']:
                line['last_updated_by'] = request.user.username
            jsondata = json.dumps(data)
            r = requests.put('{}'.format(PURCHASE_TRANSACTION), json = jsondata) 
            if r.status_code is 200:
                to_json = {'message':'ok'}
                return HttpResponse(json.dumps(to_json))
                
            else:
                template = jinja_template.get_template('internal_server_error.html')
                return HttpResponse(template.render(request))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
        
        