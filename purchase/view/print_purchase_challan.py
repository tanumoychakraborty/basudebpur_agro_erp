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
    PURCHASE_ORDER_HEADER_STATUS, RECEIPT_SEARCH
from basudebpur_agro_erp.permission.purchase_permissions import hasUpdatePurchaseRecordAccess
import json
from _io import BytesIO
from xhtml2pdf import pisa

class print_purchase_challan(template):
    '''
    classdocs
    '''


    def get(self, request, transaction_number, challan_number):
        item_list = json.loads(requests.get(ITEM_LIST).text)
        uom = json.loads(requests.get(UNIT_OF_MEASURE).text)
#        po_line_statuses = requests.get(PURCHASE_ORDER_LINES_STATUS)
        po_receipt_statuses = json.loads(requests.get(PURCHASE_ORDER_HEADER_STATUS).text)
        receipt_details = json.loads(requests.get(RECEIPT_SEARCH+'challan_number='+challan_number).text)
        if receipt_details['receipt_details'][0]['challan_date']:
            receipt_details['receipt_details'][0]['challan_date'] = receipt_details['receipt_details'][0]['challan_date'].split(' ')[0]
#         po_type = json.loads(requests.get(PURCHASE_ORDER_TYPE).text)
#         supplier_list = json.loads(requests.get(SUPPLIER_LIST).text)
#         
#         data= {'user' : request.user.username,
#                'po_type' : po_type['purchaseOrderType'],
#                'supplier_list' : supplier_list['supplierLists'],
#                'item_list' : item_list['itemDetailsList'],
#                'uom' : uom['UnitOfMeasure']
#                }
        data = {'transaction_number': transaction_number,
                'item_list': item_list['itemDetailsList'],
                'uom' : uom['UnitOfMeasure'],
                'po_receipt_statuses' : po_receipt_statuses['purchaseOrderHeaderStatus'],
                'details' : receipt_details['receipt_details'][0]}

        template = jinja_template.get_template('pdf-templates/purchase_challan.html')
        html = template.render(request, data=data)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), response)
        if not pdf.err:
            resp =  HttpResponse(response.getvalue(), content_type='application/pdf')
            resp['Content-Disposition'] = 'attachment; filename="PurchaseChallan.pdf"'
            return resp
        else:
            return HttpResponse("Error Rendering PDF", status=400)
            
        