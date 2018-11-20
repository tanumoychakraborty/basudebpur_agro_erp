'''
Created on 13-Nov-2018

@author: tanumoy
'''
from django.views import View
from django.contrib.auth.models import Permission, Group

class template(View):
    '''
    classdocs
    '''
    __seed__ = False

    def __init__(self):
        '''
        Create Permission in Django auth
        '''
        if template.__seed__ is False:
            try:
                Permission.objects.filter(name='USER').first().name
            except AttributeError:
                Permission.objects.create(name='USER', content_type_id=6, codename='USER_all')
                Permission.objects.create(name='USER', content_type_id=6, codename='USER_view')
                Permission.objects.create(name='USER', content_type_id=6, codename='USER_update')
                Permission.objects.create(name='USER', content_type_id=6, codename='USER_create')
            try:
                Permission.objects.filter(name='SALES').first().name
            except AttributeError:
                Permission.objects.create(name='SALES', content_type_id=6, codename='SALES_all')
                Permission.objects.create(name='SALES', content_type_id=6, codename='SALES_view')
                Permission.objects.create(name='SALES', content_type_id=6, codename='SALES_update')
                Permission.objects.create(name='SALES', content_type_id=6, codename='SALES_create')
            try:
                Permission.objects.filter(name='PURCHASE').first().name
            except AttributeError:
                Permission.objects.create(name='PURCHASE', content_type_id=6, codename='PURCHASE_all')
                Permission.objects.create(name='PURCHASE', content_type_id=6, codename='PURCHASE_view')
                Permission.objects.create(name='PURCHASE', content_type_id=6, codename='PURCHASE_update')
                Permission.objects.create(name='PURCHASE', content_type_id=6, codename='PURCHASE_create')
                
            try:
                Group.objects.filter(name='MANAGEMENT_REP').first().name
            except AttributeError:
                _group = Group.objects.create(name='MANAGEMENT_REP')
                map(lambda x: _group.permissions.add(x), Permission.objects.filter(name='USER').all())
                map(lambda x: _group.permissions.add(x), Permission.objects.filter(name='SALES').all())
                map(lambda x: _group.permissions.add(x), Permission.objects.filter(name='PURCHASE').all())
                _group.save()
            template.__seed__ = True
            