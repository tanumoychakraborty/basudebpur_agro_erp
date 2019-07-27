'''
Created on 17-Jul-2019

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
from basudebpur_agro_erp.permission.purchase_permissions import hasAddPurchaseRecordAccess
import json
import requests
from basudebpur_agro_erp.URLS import ITEM_LIST, UNIT_OF_MEASURE,\
    PURCHASE_ORDER_HEADER_STATUS, RECEIPT
import random

class purchase_receipt_add_view(template):
    '''
    classdocs
    '''

    def get(self, request, transaction_number):
        if hasAddPurchaseRecordAccess(request.user):
            item_list = json.loads(requests.get(ITEM_LIST).text)
            uom = json.loads(requests.get(UNIT_OF_MEASURE).text)
#            po_line_statuses = requests.get(PURCHASE_ORDER_LINES_STATUS)
            po_receipt_statuses = json.loads(requests.get(PURCHASE_ORDER_HEADER_STATUS).text)
#             po_type = json.loads(requests.get(PURCHASE_ORDER_TYPE).text)
#             supplier_list = json.loads(requests.get(SUPPLIER_LIST).text)
#             
#             data= {'user' : request.user.username,
#                    'po_type' : po_type['purchaseOrderType'],
#                    'supplier_list' : supplier_list['supplierLists'],
#                    'item_list' : item_list['itemDetailsList'],
#                    'uom' : uom['UnitOfMeasure']
#                    }
            data = {'transaction_number': transaction_number,
                    'item_list': item_list['itemDetailsList'],
                    'uom' : uom['UnitOfMeasure'],
                    'po_receipt_statuses' : po_receipt_statuses['purchaseOrderHeaderStatus']}
            template = jinja_template.get_template('purchase/purchase-receipt-add.html')
            return HttpResponse(template.render(request, data=data))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
     
    def post(self, request, transaction_number):
        if hasAddPurchaseRecordAccess(request.user):
            data = json.loads(request.body)
            data['challan_number'] = str(random.randint(0, 1000))
            data['receipt_number'] = str(random.randint(0, 1000))
            data['challan_date'] = data['receipt_date']
            data['source_transaction_header_id'] = transaction_number
            data['source_transaction_type'] = 'PURCHASE'            
            data['created_by'] = request.user.username
            data['last_updated_by'] = request.user.username
            
            for line in data['receipt_lines']:
                line['created_by'] = request.user.username
                line['last_updated_by'] = request.user.username
                if line['unit_price'] == '':
                    line.pop('unit_price')
                if line['quantity'] == '':
                    line.pop('quantity')
                
            jsondata = json.dumps(data)
            
            r = requests.post(url = RECEIPT, json = jsondata) 
            if r.status_code is 200:
                to_json = {'message':'ok'}
                return HttpResponse(json.dumps(to_json))
            else:
                template = jinja_template.get_template('internal_server_error.html')
                return HttpResponse(template.render(request))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
         