from django.shortcuts import render
from django.views.generic import TemplateView

from modules.cms.aboutus.models import AboutUs
from modules.cms.event.models import EventGalery, DetailEvent
from modules.cms.whatsnew.models import Whatsnew, DetailWhatsnew


class HomeAgrakom(TemplateView):
    def get(self, request, *args, **kwargs):
        # dataSlider =  SliderAboutUs.objects.filter(status='True').order_by('-id')[:5]

        dataWhatsnew =  Whatsnew.objects.filter(status='True').order_by('-id')[:3]

        dataEvents =  EventGalery.objects.filter(status='True').order_by('-id')[:8]

        dataAboutUs = AboutUs.objects.filter(status='True').order_by('-id')[:1]

        return render(request, 'frontend/index.html', {'aboutus': dataAboutUs[0], 'whatsnew': dataWhatsnew, 'events': dataEvents})

class EventDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        detailEvent = DetailEvent.objects.filter(event_galery_id=int(kwargs['idevent']))

        dataAboutUs = AboutUs.objects.filter(status='True').order_by('-id')[:1]

        return render(request, 'frontend/detail-event.html', {'aboutus': dataAboutUs[0], 'detail': detailEvent})

class WhatsnewDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        detailWhatsnew = DetailWhatsnew.objects.filter(whatsnew=int(kwargs['idnew']))

        dataAboutUs = AboutUs.objects.filter(status='True').order_by('-id')[:1]

        return render(request, 'frontend/detail-event.html', {'aboutus': dataAboutUs[0], 'whatsnew': detailWhatsnew})
