'''
Created on 20-Dec-2018

@author: tanumoy
'''

def hasAddPurchaseRecordAccess(user):
    for group in user.groups.all():
        for permission in group.permissions.all():
            if permission.codename == 'PURCHASE_all' or permission.codename == 'PURCHASE_create':
                return True
    return False           

def hasUpdatePurchaseRecordAccess(user):
    for group in user.groups.all():
        for permission in group.permissions.all():
            if permission.codename == 'PURCHASE_all' or permission.codename == 'PURCHASE_update':
                return True
    return False                