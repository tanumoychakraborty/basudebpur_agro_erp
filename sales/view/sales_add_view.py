'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
from basudebpur_agro_erp.permission.purchase_permissions import hasAddPurchaseRecordAccess
import json
from basudebpur_agro_erp.URLS import PURCHASE_TRANSACTION, ITEM_LIST,\
    UNIT_OF_MEASURE, PURCHASE_ORDER_LINES_STATUS, PURCHASE_ORDER_HEADER_STATUS,\
    PURCHASE_ORDER_TYPE, SUPPLIER_LIST
import requests
from django.shortcuts import redirect

class sales_add_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        if hasAddPurchaseRecordAccess(request.user):
            item_list = json.loads(requests.get(ITEM_LIST).text)
            uom = json.loads(requests.get(UNIT_OF_MEASURE).text)
#             po_line_statuses = requests.get(PURCHASE_ORDER_LINES_STATUS)
#             po_header_statuses = requests.get(PURCHASE_ORDER_HEADER_STATUS)
            po_type = json.loads(requests.get(PURCHASE_ORDER_TYPE).text)
            supplier_list = json.loads(requests.get(SUPPLIER_LIST).text)
            
            data= {'user' : request.user.username,
                   'po_type' : po_type['purchaseOrderType'],
                   'supplier_list' : supplier_list['supplierLists'],
                   'item_list' : item_list['itemDetailsList'],
                   'uom' : uom['UnitOfMeasure']
                   }
            template = jinja_template.get_template('sales/sales-line-add.html')
            return HttpResponse(template.render(request, data=data))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
    
    def post(self, request):
        if hasAddPurchaseRecordAccess(request.user):
            data = json.loads(request.body)
            data['order_status'] = 'BOOKED'
            data['created_by'] = request.user.username
            data['last_updated_by'] = request.user.username
            if data['transaction_date']:
                data['transaction_date'] = data['transaction_date'].replace(' ','T')
            for line in data['purchase_trx_lines']:
                line['line_status'] = 'BOOKED'
                line['created_by'] = request.user.username
                line['last_updated_by'] = request.user.username
            jsondata = json.dumps(data)
            
            r = requests.post(url = PURCHASE_TRANSACTION, json = jsondata) 
            if r.status_code is 200:
                to_json = {'message':'ok'}
                return HttpResponse(json.dumps(to_json))
            else:
                template = jinja_template.get_template('internal_server_error.html')
                return HttpResponse(template.render(request))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
        