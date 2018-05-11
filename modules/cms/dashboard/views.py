from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class Dashboard(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Dashboard, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return render(request, 'cms/dashboard/index.html', context={})
