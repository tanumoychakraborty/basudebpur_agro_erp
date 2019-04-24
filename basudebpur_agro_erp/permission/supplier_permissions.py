'''
Created on 27-Dec-2018

@author: tanumoy
'''

def hasAddSupplierAccess(user):
    for group in user.groups.all():
        for permission in group.permissions.all():
            if permission.codename == 'SUPPLIER_all' or permission.codename == 'SUPPLIER_create':
                return True
    return False           

def hasUpdateSupplierAccess(user):
    for group in user.groups.all():
        for permission in group.permissions.all():
            if permission.codename == 'SUPPLIER_all' or permission.codename == 'SUPPLIER_update':
                return True
    return False    