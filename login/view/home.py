'''
Created on 20-Nov-2018

@author: tanumoy
'''
from django.contrib.auth.decorators import login_required
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
from basudebpur_agro_erp.view.template import template
from django.contrib.auth.mixins import LoginRequiredMixin
from basudebpur_agro_erp.ERPLoginRequired import ERPLoginRequired

class home(ERPLoginRequired, template):
    '''
    classdocs
    '''
    def get(self, request):
        template = jinja_template.get_template('home.html')
        return HttpResponse(template.render(request))