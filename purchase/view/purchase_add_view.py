'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
from basudebpur_agro_erp.permission.purchase_permissions import hasAddPurchaseRecordAccess

class purchase_add_view(template):
    '''
    classdocs
    '''

    def get(self, request):
        if hasAddPurchaseRecordAccess(request.user):
            template = jinja_template.get_template('purchase/purchase-line-add.html')
        else:
            template = jinja_template.get_template('access_denied.html')
        return HttpResponse(template.render(request))