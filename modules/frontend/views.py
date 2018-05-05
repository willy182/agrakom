from django.shortcuts import render
from django.views.generic import TemplateView

class HomeAgrakom(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'frontend/index.html', context={})
