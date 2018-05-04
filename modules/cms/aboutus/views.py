from django.shortcuts import render
from django.views.generic import TemplateView

from modules.cms.aboutus.models import AboutUs


class AboutUsList(TemplateView):
    # @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AboutUsList, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_about_us = AboutUs.objects.all().order_by("id")

        # add custom context for template
        cust_context = {
            'all_about_us': all_about_us,
        }

        return render(request, 'cms/aboutus/index.html', context=cust_context)
