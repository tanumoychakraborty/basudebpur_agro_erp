'''
Created on 06-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.view.template import template
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

class logout_view(template):
    '''
    classdocs
    '''
    
    @never_cache
    def get(self, request):
        logout(request)
        request.user.is_active = False
#         template = jinja_template.get_template('login/page-login.html')
#         return HttpResponse(template.render(request))
        return redirect('login',permanent=True)