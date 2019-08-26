'''
Created on 27-Jul-2019

@author: tanumoy
'''
import json
import random

from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.URLS import ITEM_LIST, UNIT_OF_MEASURE, \
    RECEIPT_LINE_STATUS, RECEIPT, RECEIPT_SEARCH
from basudebpur_agro_erp.permission.purchase_permissions import hasAddPurchaseRecordAccess
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template


class purchase_receipt_update_view(template):
    '''
    classdocs
    '''

    def get(self, request, transaction_number, challan_number):
        if hasAddPurchaseRecordAccess(request.user):
            item_list = json.loads(requests.get(ITEM_LIST).text)
            uom = json.loads(requests.get(UNIT_OF_MEASURE).text)
            po_receipt_statuses = json.loads(requests.get(RECEIPT_LINE_STATUS).text)
            receipt_details = json.loads(requests.get(RECEIPT_SEARCH+'challan_number='+challan_number).text)
            if receipt_details['receipt_details'][0]['challan_date']:
                receipt_details['receipt_details'][0]['challan_date'] = receipt_details['receipt_details'][0]['challan_date'].split(' ')[0]
            data = {'transaction_number': transaction_number,
                    'item_list': item_list['itemDetailsList'],
                    'uom' : uom['UnitOfMeasure'],
                    'po_receipt_statuses' : po_receipt_statuses['lookup_details'],
                    'details' : receipt_details['receipt_details'][0]}
            if receipt_details['receipt_details'][0]['receipt_header_status'] == 'OPEN':
                template = jinja_template.get_template('purchase/purchase-receipt-update.html')
                
            else:
                template = jinja_template.get_template('purchase/purchase-receipt-view-only.html')
                
            return HttpResponse(template.render(request, data=data))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
        
     
    def put(self, request, transaction_number, challan_number):
        if hasAddPurchaseRecordAccess(request.user):
            data = json.loads(request.body)
            #data['source_transaction_header_id'] = transaction_number
            #data['source_transaction_type'] = 'PURCHASE'            
            data['last_updated_by'] = request.user.username
            
            for line in data['receipt_lines']:
                line['last_updated_by'] = request.user.username
                if line['unit_price'] == '':
                    line.pop('unit_price')
                if line['quantity'] == '':
                    line.pop('quantity')
                if line['discount'] == '':
                    line.pop('discount')
                if 'receipt_line_id' in line.keys():
                    if line['receipt_line_id'] == '':
                        line.pop('receipt_line_id')
                
            jsondata = json.dumps(data)
            
            r = requests.put(url = RECEIPT, json = jsondata) 
            if r.status_code is 200:
                to_json = {'message':'ok'}
                return HttpResponse(json.dumps(to_json), status = 200)
            elif r.status_code == 422:
                to_json = json.loads(r.content)['errors']
                return HttpResponse(json.dumps(to_json), status = 422)
            else:
                template = jinja_template.get_template('internal_server_error.html')
                return HttpResponse(template.render(request))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))