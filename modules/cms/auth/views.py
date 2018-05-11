from django.contrib.auth.forms import  AuthenticationForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import Group, Permission
import json
from django.contrib.auth import login, logout

from modules.cms.role.forms import GroupForm

class Login(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        cust_context = {}
        return super(Login, self).dispatch(request, cust_context, *args, **kwargs)

    def get(self, request, content, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'cms/auth/index.html', {'form': form})

    def post(self, request, content, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.user_cache)
            return HttpResponseRedirect('/cms-agrakom/')
        else:
            form = AuthenticationForm(data=request.POST)
            return render(request, 'cms/auth/index.html', {'form': form})


class Logout(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        cust_context = {}
        return super(Logout, self).dispatch(request, cust_context, *args, **kwargs)

    def get(self, request, content, *args, **kwargs):
        status = logout(request)
        return HttpResponseRedirect('/cms-agrakom/auth/')

