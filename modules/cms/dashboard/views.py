from django.shortcuts import render
from django.views.generic import TemplateView

class Dashboard(TemplateView):
    # @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Dashboard, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return render(request, 'cms/dashboard/index.html', context={})
