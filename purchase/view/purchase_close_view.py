'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.external_urls import PURCHASE_TRANSACTION
from basudebpur_agro_erp.permission.purchase_permissions import hasUpdatePurchaseRecordAccess
import json
from django.shortcuts import redirect

class purchase_close_view(template):
    '''
    classdocs
    '''


    def get(self, request, transaction_number):
        r = requests.get(url = PURCHASE_TRANSACTION, params = {'transaction_number':transaction_number}) 
        if r.status_code is 200:
            json_data = r.json()
            
            if hasUpdatePurchaseRecordAccess(request.user):
                data = json_data['purchase_trx_details'][0]
                data['last_updated_by'] = request.user.username
                if 'receipt_details' in data.keys():
                    data['order_status'] = 'CANCELLED'
                    for line in data['receipt_details']:
                        if line['receipt_header_status'] == 'COMPLETE':
                            data['order_status'] = 'COMPLETE'
                            break
                    
                else:
                    data['order_status'] = 'CANCELLED'
                
                if 'transaction_header_id' in data.keys():
                    data.pop('transaction_header_id')
                if 'transaction_date' in data.keys():
                    data.pop('transaction_date')
                if 'buyer_id' in data.keys():
                    data.pop('buyer_id')
                if 'buyer_name' in data.keys():
                    data.pop('buyer_name')
                if 'supplier_id' in data.keys():
                    data.pop('supplier_id')
                if 'purchase_trx_lines' in data.keys():
                    data.pop('purchase_trx_lines')
                if 'amount' in data.keys():
                    data.pop('amount')
                if 'created_by' in data.keys():
                    data.pop('created_by')
                if 'creation_date' in data.keys():
                    data.pop('creation_date')
                if 'last_update_date' in data.keys():
                    data.pop('last_update_date')
                if 'receipt_details' in data.keys():
                    data.pop('receipt_details')
                jsondata = json.dumps(data)
                r = requests.put('{}'.format(PURCHASE_TRANSACTION), json = jsondata) 
                if r.status_code is 200:
                    return redirect('/purchase/')
                
                elif r.status_code == 422:
                    to_json = json.loads(r.content)['errors']
                    return HttpResponse(json.dumps(to_json), status = 422)
                    
                else:
                    template = jinja_template.get_template('internal_server_error.html')
                    return HttpResponse(template.render(request))
            else:
                template = jinja_template.get_template('access_denied.html')
                return HttpResponse(template.render(request))
        else:
            template = jinja_template.get_template('internal_server_error.html')
            return HttpResponse(template.render(request))
        