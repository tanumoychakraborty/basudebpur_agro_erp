'''
Created on 27-Jul-2019

@author: tanumoy
'''
import json
import random

from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.external_urls import PURCHASE_ITEM_LIST, UNIT_OF_MEASURE, \
    RECEIPT_LINE_STATUS, RECEIPT, RECEIPT_SEARCH
from basudebpur_agro_erp.permission.purchase_permissions import hasAddPurchaseRecordAccess
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from basudebpur_agro_erp.util import clearDictionary, isFloat


class purchase_receipt_update_view(template):
    '''
    classdocs
    '''

    def get(self, request, transaction_number, challan_number):
        if hasAddPurchaseRecordAccess(request.user):
            item_list = json.loads(requests.get(PURCHASE_ITEM_LIST).text)
            uom = json.loads(requests.get(UNIT_OF_MEASURE).text)
            po_receipt_statuses = json.loads(requests.get(RECEIPT_LINE_STATUS).text)
            receipt_details = json.loads(requests.get(RECEIPT_SEARCH+'challan_number='+challan_number).text)
            if receipt_details['receipt_details'][0]['challan_date']:
                receipt_details['receipt_details'][0]['challan_date'] = receipt_details['receipt_details'][0]['challan_date'].split(' ')[0]
                
            if 'receipt_date' in receipt_details['receipt_details'][0].keys():
                if receipt_details['receipt_details'][0]['receipt_date']:
                    receipt_details['receipt_details'][0]['receipt_date'] = receipt_details['receipt_details'][0]['receipt_date'].split(' ')[0]
            
            receipt = clearDictionary(receipt_details['receipt_details'][0])
                
            data = {'transaction_number': transaction_number,
                    'item_list': item_list['itemDetailsList'],
                    'uom' : uom['UnitOfMeasure'],
                    'po_receipt_statuses' : po_receipt_statuses['lookup_details'],
                    'details' : receipt}
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
            if data['bata'] == '':
                data.pop('bata')
            if data['net_weight'] == '':
                data.pop('net_weight')
            total_bags = 0
            all_line_has_bags = False
            
            if 'receipt_lines' in data.keys():
                all_line_has_bags = True
                for line in data['receipt_lines']:
                    line['last_updated_by'] = request.user.username
                    if 'number_of_bags' in line.keys():
                        if line['number_of_bags'] != '' and isFloat(line['number_of_bags']):
                            total_bags += float(line['number_of_bags'])
                            all_line_has_bags = all_line_has_bags & True
                        else:
                            line.pop('number_of_bags')
                            all_line_has_bags = all_line_has_bags & False
                    
                    if line['unit_price'] == '':
                        line.pop('unit_price')
                    if line['item_id'] == '':
                        line.pop('item_id')
                    line['quantity'] = 0
                    if line['load_unload_area'] == '':
                        line.pop('load_unload_area')
                    if line['discount'] == '':
                        line.pop('discount')
                    if 'receipt_line_id' in line.keys():
                        if line['receipt_line_id'] == '':
                            line.pop('receipt_line_id')
                        
            if total_bags > 0 and 'bata' in data.keys() and 'net_weight' in data.keys() and all_line_has_bags:
                net_weight = float(data['net_weight'])
                weight = net_weight - float(data['bata'])
                average_weight = weight / total_bags
                for line in data['receipt_lines']:
                    line['quantity'] = average_weight * float(line['number_of_bags'])
                data['average_weight'] = average_weight
                data['total_bags'] = total_bags
            else:
                data['average_weight'] = 0
                data['total_bags'] = 0
                
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