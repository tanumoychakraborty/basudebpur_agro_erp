'''
Created on 17-Nov-2018

@author: tanumoy
'''
from django import forms

class login_form(forms.Form):
    '''
    classdocs
    '''

    username = forms.CharField(min_length=1)
    password = forms.CharField(min_length=1)