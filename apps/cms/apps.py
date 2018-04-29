from django.apps import AppConfig
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class CmsConfig(AppConfig):
    name = 'cms'

class memberList(TemplateView):
    # @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        return render(request, 'cms/layout.html')

class Logout_View(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        return super(Logout_View, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        status = logout(request)
        protocol = request.scheme
        host = request.META['HTTP_HOST']
        return redirect( str(protocol) + '://' + host + '/login/')

