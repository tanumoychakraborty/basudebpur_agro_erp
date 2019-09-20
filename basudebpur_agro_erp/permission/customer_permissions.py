'''
Created on 27-Dec-2018

@author: tanumoy
'''

def hasAddCustomerAccess(user):
    for group in user.groups.all():
        for permission in group.permissions.all():
            if permission.codename == 'CUSTOMER_all' or permission.codename == 'CUSTOMER_create':
                return True
    return False           

def hasUpdateCustomerAccess(user):
    for group in user.groups.all():
        for permission in group.permissions.all():
            if permission.codename == 'CUSTOMER_all' or permission.codename == 'CUSTOMER_update':
                return True
    return False    