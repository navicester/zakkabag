from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.http import Http404

class StaffRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(StaffRequiredMixin, self).as_view(*args, **kwargs)
        return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404



class LoginRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(LoginRequiredMixin, self).as_view(*args, **kwargs)
        return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)



class PermissionRequiredMixin(object):

    # method #1
    @method_decorator(permission_required("products.add_product"))
    def dispatch(self, request, *args, **kwargs):
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)

    # method #2
    # def dispatch(self, request, *args, **kwargs):

    #     if request.user.has_perm("products.add_product"):
    #         return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
    #     else:
    #         # django.contrib.auth.decorators.py
    #         from django.contrib.auth.views import redirect_to_login
    #         from django.conf import settings
    #         from django.shortcuts import resolve_url

    #         path = request.get_full_path()
    #         resolved_login_url = resolve_url(settings.LOGIN_URL)
    #         redirect_field_name = 'next'
    #         return redirect_to_login(path, resolved_login_url, redirect_field_name)            