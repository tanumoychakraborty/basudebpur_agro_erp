'''
Created on 27-Dec-2018

@author: tanumoy
'''

def hasAddSalesRecordAccess(user):
    for group in user.groups.all():
        for permission in group.permissions.all():
            if permission.codename == 'SALES_all' or permission.codename == 'SALES_create':
                return True
    return False           

def hasUpdateSalesRecordAccess(user):
    for group in user.groups.all():
        for permission in group.permissions.all():
            if permission.codename == 'SALES_all' or permission.codename == 'SALES_update':
                return True
    return False   
