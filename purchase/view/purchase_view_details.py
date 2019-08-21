'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.URLS import PURCHASE_TRANSACTION, ITEM_LIST,\
    UNIT_OF_MEASURE, PURCHASE_ORDER_TYPE, SUPPLIER_LIST,\
    PURCHASE_ORDER_HEADER_STATUS
from basudebpur_agro_erp.permission.purchase_permissions import hasUpdatePurchaseRecordAccess
import json

class purchase_view_details(template):
    '''
    classdocs
    '''


    def get(self, request, transaction_number):
        r = requests.get(url = PURCHASE_TRANSACTION, params = {'transaction_number':transaction_number}) 
        if r.status_code is 200:
            json_data = r.json()
            
            if hasUpdatePurchaseRecordAccess(request.user):
                item_list = json.loads(requests.get(ITEM_LIST).text)
                uom = json.loads(requests.get(UNIT_OF_MEASURE).text)
                po_header_statuses = json.loads(requests.get(PURCHASE_ORDER_HEADER_STATUS).text)
                po_type = json.loads(requests.get(PURCHASE_ORDER_TYPE).text)
                supplier_list = json.loads(requests.get(SUPPLIER_LIST).text)
                if 'transaction_date' in json_data['purchase_trx_details'][0]:
                    #json_data['purchase_trx_details'][0]['transaction_date'] = json_data['purchase_trx_details'][0]['transaction_date'].replace('/', '-')
                    json_data['purchase_trx_details'][0]['transaction_date'] = json_data['purchase_trx_details'][0]['transaction_date'].split(' ')[0]
                if 'receipt_details' in json_data['purchase_trx_details'][0]:
                    for row in json_data['purchase_trx_details'][0]['receipt_details']:
                        if row['challan_date']:
                            row['challan_date'] = row['challan_date'].split(' ')[0]
                        if row['receipt_date']:
                            row['receipt_date'] = row['receipt_date'].split(' ')[0]
                        
                data= {'user' : request.user.username,
                       'po_type' : po_type['purchaseOrderType'],
                       'supplier_list' : supplier_list['supplierLists'],
                       'item_list' : item_list['itemDetailsList'],
                       'uom' : uom['UnitOfMeasure'],
                       'header_status' : po_header_statuses['purchaseOrderHeaderStatus'],
                       'details' : json_data['purchase_trx_details'][0]
                   }
                
                if json_data['purchase_trx_details'][0]['order_status'] == 'OPEN':
                    template = jinja_template.get_template('purchase/purchase-line-update.html')
                    
                    
                else:
                    template = jinja_template.get_template('purchase/purchase-line-view.html')
                    #data=json_data['purchase_trx_details'][0]
                    
                return HttpResponse(template.render(request, data=data))
            else:
                if 'transaction_date' in json_data['purchase_trx_details'][0]:
                    #json_data['purchase_trx_details'][0]['transaction_date'] = json_data['purchase_trx_details'][0]['transaction_date'].replace('/', '-')
                    json_data['purchase_trx_details'][0]['transaction_date'] = json_data['purchase_trx_details'][0]['transaction_date'].split(' ')[0]
                if 'receipt_details' in json_data['purchase_trx_details'][0]:
                    for row in json_data['purchase_trx_details'][0]['receipt_details']:
                        row['receipt_date'] = row['receipt_date'].split(' ')[0]
                        row['challan_date'] = row['challan_date'].split(' ')[0]
                template = jinja_template.get_template('purchase/purchase-line-view.html')
                return HttpResponse(template.render(request, data=json_data['purchase_trx_details'][0]))
        else:
            template = jinja_template.get_template('internal_server_error.html')
            return HttpResponse(template.render(request))
        