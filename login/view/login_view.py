'''
Created on 13-Nov-2018

@author: tanumoy
'''

from django.http.response import HttpResponse
from basudebpur_agro_erp.jinja_template import jinja_template
from basudebpur_agro_erp.view.template import template


#from login.view.util import static
class login_view(template):
    '''
    classdocs
    '''


    def get(self, request):
        template = jinja_template.get_template('login/page-login.html')
        return HttpResponse(template.render(request))