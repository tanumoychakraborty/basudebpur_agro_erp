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
from django.shortcuts import redirect


class purchase_receipt_cancel_view(template):
    '''
    classdocs
    '''

    def get(self, request, transaction_number, challan_number):
        if hasAddPurchaseRecordAccess(request.user):
            receipt_details = json.loads(requests.get(RECEIPT_SEARCH+'challan_number='+challan_number).text)
            receipt_details['receipt_details'][0]['receipt_header_status'] = 'CANCEL'
            receipt_details['receipt_details'][0].pop('created_by')
            receipt_details['receipt_details'][0].pop('creation_date')
            receipt_details['receipt_details'][0]['last_updated_by'] = request.user.username
            if 'receipt_lines' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('receipt_lines')
            if 'receipt_date' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('receipt_date')
            if 'receipt_number' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('receipt_number')
            if 'challan_date' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('challan_date')
            if 'last_update_date' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('last_update_date')
            if 'bata' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('bata')
            if 'net_weight' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('net_weight')
            if 'average_weight' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('average_weight')
            if 'total_bags' in receipt_details['receipt_details'][0].keys():
                receipt_details['receipt_details'][0].pop('total_bags')
            jsondata = json.dumps(receipt_details['receipt_details'][0])
            r = requests.put(url = RECEIPT, json = jsondata) 
            if r.status_code is 200:
                to_json = {'message':'ok'}
                return redirect('/purchase/'+transaction_number)
            elif r.status_code == 422:
                to_json = json.loads(r.content)['errors']
                return HttpResponse(json.dumps(to_json), status = 422)
            else:
                template = jinja_template.get_template('internal_server_error.html')
                return HttpResponse(template.render(request))
  