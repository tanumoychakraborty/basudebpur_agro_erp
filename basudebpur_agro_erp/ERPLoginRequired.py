'''
Created on 20-Nov-2018

@author: tanumoy
'''
from django.contrib.auth.mixins import LoginRequiredMixin

class ERPLoginRequired(LoginRequiredMixin):
    """Verify that the current user is authenticated."""
    redirect_field_name = 'next'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    