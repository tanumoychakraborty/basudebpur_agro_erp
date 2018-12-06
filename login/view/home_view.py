'''
Created on 20-Nov-2018

@author: tanumoy
'''
from basudebpur_agro_erp.jinja_template import jinja_template
from django.http.response import HttpResponse
from basudebpur_agro_erp.view.template import template

class home_view(template):
    '''
    classdocs
    '''
    def get(self, request):
        template = jinja_template.get_template('home.html')
        return HttpResponse(template.render(request))