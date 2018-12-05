'''
Created on 06-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from django.contrib.auth import logout
from django.http.response import HttpResponse
from basudebpur_agro_erp.jinja_template import jinja_template

class logout_view(template):
    '''
    classdocs
    '''


    def get(self, request):
        logout(request)
        template = jinja_template.get_template('login/page-login.html')
        return HttpResponse(template.render(request))