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

class purchase_view_view(template):
    '''
    classdocs
    '''


    def get(self, request):
        r = requests.get(url = PURCHASE_TRANSACTION) 
        if r.status_code is 200:
            json_data = r.json()
            template = jinja_template.get_template('purchase/purchase-header-view.html')
            return HttpResponse(template.render(request, data=json_data['purchase_trx_details']))
        else:
            return HttpResponse(defaults.server_error(request))