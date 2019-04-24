'''
Created on 13-Nov-2018

@author: tanumoy
'''

from django.http.response import HttpResponse
from basudebpur_agro_erp.jinja_template import jinja_template
from basudebpur_agro_erp.view.template import template
import requests
from login.forms.login_form import login_form
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.views import defaults
from django.shortcuts import redirect
from basudebpur_agro_erp.URLS import ACCESS_RIGHT


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
        
            PARAMS = {'userName':username,
                      'password': password} 
                        
            user = authenticate(username=username, password=password)
            if user is None:
                r = requests.get(url = ACCESS_RIGHT, params = PARAMS) 
                
                if r.status_code is 200:
                    json_data = r.json()
                    _permissions = []
                                            
                    #data = json.loads(json_data)
                    user = User.objects.create_user(username, '', password)
                    for _group in Group.objects.filter(name=json_data['access']).all():
                        user.groups.add(_group)
                    
                    user.save()
                    user = authenticate(username=username, password=password)

                    
                else:
                    template = jinja_template.get_template('login/page-relogin.html')
                    return HttpResponse(template.render(request=request))
            
            if user.is_active:
                request.session.set_expiry(7200) #sets the exp. value of the session 
                login(request, user) #the user is now logged in
                request.user = user
#                 template = jinja_template.get_template('home.html')
#                 return HttpResponse(template.render(request=request))
                return redirect('home',permanent=True)
            else:
                return HttpResponse(defaults.page_not_found(request, Exception('message', 'Error while trying to login.. Please try again..'), template_name='500.html'))
            
        else:
            template = jinja_template.get_template('login/page-relogin.html')
            return HttpResponse(template.render(request=request))
            