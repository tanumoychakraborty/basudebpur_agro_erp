'''
Created on 15-Nov-2018

@author: tanumoy
'''
import jinja2
import os
from basudebpur_agro_erp import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse



class jinja_template(object):
    templateLoader = None
    templateEnv = None

    @staticmethod
    def get_template(TEMPLATE_FILE):
        if jinja_template.templateLoader is None:
            jinja_template.templateLoader = jinja2.FileSystemLoader(searchpath=os.path.join(settings.BASE_DIR, 'templates'))
        if jinja_template.templateEnv is None:
            jinja_template.templateEnv = jinja2.Environment(loader=jinja_template.templateLoader)
            jinja_template.templateEnv.globals.update({'static': staticfiles_storage.url, 'url': reverse})
        return jinja_template.templateEnv.get_template(TEMPLATE_FILE);