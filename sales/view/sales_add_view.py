'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
from basudebpur_agro_erp.permission.sales_permissions import hasAddSalesRecordAccess
import json
from basudebpur_agro_erp.URLS import SALES_TRANSACTION, SALES_ITEM_LIST,\
    UNIT_OF_MEASURE, SALES_ORDER_TYPE, CUSTOMER_LIST
import requests
from django.shortcuts import redirect

class sales_add_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        if hasAddSalesRecordAccess(request.user):
            item_list = json.loads(requests.get(SALES_ITEM_LIST).text)
            uom = json.loads(requests.get(UNIT_OF_MEASURE).text)
#             po_line_statuses = requests.get(PURCHASE_ORDER_LINES_STATUS)
#             po_header_statuses = requests.get(PURCHASE_ORDER_HEADER_STATUS)
            so_type = json.loads(requests.get(SALES_ORDER_TYPE).text)
            customer_list = json.loads(requests.get(CUSTOMER_LIST).text)
            
            data= {'user' : request.user.username,
                   'so_type' : so_type['salesOrderType'],
                   'customer_list' : customer_list['customerLists'],
                   'item_list' : item_list['itemDetailsList'],
                   'uom' : uom['UnitOfMeasure']
                   }
            template = jinja_template.get_template('sales/sales-line-add.html')
            return HttpResponse(template.render(request, data=data))
        else:
            template = jinja_template.get_template('access_denied.html')
            return HttpResponse(template.render(request))
    
    def post(self, request):
        if hasAddSalesRecordAccess(request.user):
            data = json.loads(request.body)
            data['order_status'] = 'OPEN'
            data['created_by'] = request.user.username
            data['last_updated_by'] = request.user.username
            if data['transaction_date'] == '':
                data.pop('transaction_date')
            for line in data['sales_trx_lines']:
                line['created_by'] = request.user.username
                line['last_updated_by'] = request.user.username
                if line['booking_unit_price'] == '':
                    line.pop('booking_unit_price')
                if line['booking_quantity'] == '':
                    line.pop('booking_quantity')
            jsondata = json.dumps(data)
            
            r = requests.post(url = SALES_TRANSACTION, json = jsondata) 
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
        