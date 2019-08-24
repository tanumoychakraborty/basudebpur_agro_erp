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
    PURCHASE_ORDER_LINES_STATUS, PURCHASE_ORDER_HEADER_STATUS
from django.views import defaults
from basudebpur_agro_erp.permission.purchase_permissions import hasUpdatePurchaseRecordAccess
import json
from _io import BytesIO
from xhtml2pdf import pisa

class print_sales_challan(template):
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
                po_line_statuses = json.loads(requests.get(PURCHASE_ORDER_LINES_STATUS).text)
                po_header_statuses = json.loads(requests.get(PURCHASE_ORDER_HEADER_STATUS).text)
                po_type = json.loads(requests.get(PURCHASE_ORDER_TYPE).text)
                supplier_list = json.loads(requests.get(SUPPLIER_LIST).text)
            
                data= {'user' : request.user.username,
                       'po_type' : po_type['purchaseOrderType'],
                       'supplier_list' : supplier_list['supplierLists'],
                       'item_list' : item_list['itemDetailsList'],
                       'uom' : uom['UnitOfMeasure'],
                       'header_status' : po_header_statuses['purchaseOrderHeaderStatus'],
                       'line_status' : po_line_statuses['purchaseOrderLineStatus'],
                       'details' : json_data['purchase_trx_details'][0]
                   }
                template = jinja_template.get_template('pdf-templates/sales-challan.html')
                html = template.render(request, data=data)
                response = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
                if not pdf.err:
                    resp =  HttpResponse(response.getvalue(), content_type='application/pdf')
                    resp['Content-Disposition'] = 'attachment; filename="SalesChallan.pdf"'
                    return resp
                else:
                    return HttpResponse("Error Rendering PDF", status=400)
            else:
                template = jinja_template.get_template('sales/sales-line-view.html')
                return HttpResponse(template.render(request, data=json_data['purchase_trx_details'][0]))
        else:
            template = jinja_template.get_template('internal_server_error.html')
            return HttpResponse(template.render(request))
        