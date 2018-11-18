'''
Created on 13-Nov-2018

@author: tanumoy
'''

from django.http.response import HttpResponse
from basudebpur_agro_erp.jinja_template import jinja_template
from basudebpur_agro_erp.view.template import template
import requests
import json
from login.forms.login_form import login_form


#from login.view.util import static
class login_view(template):
    '''
    classdocs
    '''


    def get(self, request):
        template = jinja_template.get_template('login/page-login.html')
        return HttpResponse(template.render(request))
    
    def post(self, request):
        form = login_form(request.POST)
        if form.is_valid():
            username = form.data['username']
            password = form.data['password']
        URL = "http://localhost:9000/api/access-right"
        PARAMS = {'userName':'ARITRATEWARY',
                  'password': '1234'} 
        r = requests.get(url = URL, params = PARAMS) 
        json_data = r.json() 
        data = json.loads(json_data)
        template = jinja_template.get_template('login/page-login.html')
        return HttpResponse(template.render(request))
        