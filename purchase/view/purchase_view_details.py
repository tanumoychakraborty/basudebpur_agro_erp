'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
import requests
from basudebpur_agro_erp.URLS import PURCHASE_TRANSACTION
from django.views import defaults

class purchase_view_details(template):
    '''
    classdocs
    '''


    def get(self, request, transaction_number):
        r = requests.get(url = PURCHASE_TRANSACTION, params = {'transaction_number':transaction_number}) 
        if r.status_code is 200:
            json_data = r.json()
            line1 = {   "item_id" : "1",
                        "line_number": "1",
                        "item_description" : "Miniket Premium",
                        "booking_unit_price"  :  "100",
                        "booking_quantity"  :  "10",
                        "receipt_unit_price"  :  "100",
                        "receipt_quantity"  :  "10",
                        "discount" : "100",
                        "unit_of_measure"  :  "KG",
                        "line_status"  :  "ENTERED",
                        "created_by"  :  "1995",
                        "last_updated_by" : "1995"}
            line2 = {   "item_id" : "2",
                        "line_number": "2",
                        "item_description" : "Bashkati Regular",
                        "booking_unit_price"  :  "120",
                        "booking_quantity"  :  "10",
                        "receipt_unit_price"  :  "120",
                        "receipt_quantity"  :  "10",
                        "discount" : "100",
                        "unit_of_measure"  :  "KG",
                        "line_status"  :  "ENTERED",
                        "created_by"  :  "1995",
                        "last_updated_by" : "1995"}
            json_data['purchase_trx_details'][0]["purchase_trx_lines"]= [line1,line2]
            #template = jinja_template.get_template('purchase/purchase-line-view.html')
            template = jinja_template.get_template('purchase/purchase-line-update.html')
            return HttpResponse(template.render(request, data=json_data['purchase_trx_details'][0]))
        else:
            return HttpResponse(defaults.server_error(request))