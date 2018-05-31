from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from modules.cms.aboutus.models import AboutUs, SliderAboutUs
from modules.cms.awards.models import AwardsGalery
from modules.cms.event.models import EventGalery, DetailEvent
from modules.cms.ourclients.models import Ourclient
from modules.cms.ourservices.models import OurServiceDetail
from modules.cms.whatsnew.models import Whatsnew, DetailWhatsnew


class HomeAgrakom(TemplateView):
    def get(self, request, *args, **kwargs):
        dataSlider =  SliderAboutUs.objects.filter(status='True').order_by('-id')[:5]

        dataWhatsnew =  Whatsnew.objects.filter(status='True').order_by('-id')[:3]

        dataWhoWeAre =  OurServiceDetail.objects.filter(status='True').order_by('-id')[:4]

        dataAwards = AwardsGalery.objects.filter(status='True').order_by('-id')[:6]

        dataClients =  Ourclient.objects.filter(status='True').order_by('-id')[:5]

        dataEvents =  EventGalery.objects.filter(status='True').order_by('-id')[:6]

        dataAboutUs = AboutUs.objects.filter(status='True').order_by('-id')[:1]

        return render(request, 'frontend/index.html', {
            'sliders': dataSlider, 'whatsnew': dataWhatsnew,
            'whoweare': dataWhoWeAre, 'awards': dataAwards,
            'events': dataEvents, 'clients': dataClients,
            'aboutus': dataAboutUs[0]
        })

    def post(self, request, *args, **kwargs):
        emailFrom = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        send_mail(
            subject,
            message,
            emailFrom,
            ['mail_pr@agrakompr.com'],
            fail_silently=False,
        )

        return HttpResponseRedirect('/#contact')


class EventDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        detailEvent = DetailEvent.objects.filter(event_galery_id=int(kwargs['idevent']))

        dataAboutUs = AboutUs.objects.filter(status='True').order_by('-id')[:1]

        return render(request, 'frontend/detail-event.html', {'aboutus': dataAboutUs[0], 'detail': detailEvent})

class WhatsnewDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        detailWhatsnew = DetailWhatsnew.objects.filter(whatsnew=int(kwargs['idnew']))

        dataAboutUs = AboutUs.objects.filter(status='True').order_by('-id')[:1]

        return render(request, 'frontend/detail-event.html', {'aboutus': dataAboutUs[0], 'detail': detailWhatsnew})

class WhatsnewAjax(TemplateView):
    def get(self, request, *args, **kwargs):
        offset = int(kwargs['offset'])
        limit = int(kwargs['limit'])
        dataWhatsnew =  Whatsnew.objects.filter(status='True').order_by('-id')[offset:limit]

        data = ''
        if dataWhatsnew.count() > 0:
            for row in dataWhatsnew:
                data += '<li class="span4">' \
                            '<div class="thumbnail" style="background-color: #f1f1f1;">' \
                                '<img src="' + row.image.url + '" alt="ALT NAME">' \
                                '<h3 class="entry-title" style="margin-top:10px; margin-left: 10px; padding-bottom: 10px;">' \
                                    '<a href="/detail-whatsnew/' + str(row.id) + '/' + slugify(row.title) + '" class="exp_tt">' + row.title + '</a>' \
                                '</h3>' \
                            '</div>' \
                        '</li>'

        return HttpResponse(data)

class AwardAjax(TemplateView):
    def get(self, request, *args, **kwargs):
        offset = int(kwargs['offset'])
        limit = int(kwargs['limit'])
        dataAwards = AwardsGalery.objects.filter(status='True').order_by('-id')[offset:limit]

        data = ''
        if dataAwards.count() > 0:
            for row in dataAwards:
                data += '<li class="span4">' \
                            '<div class="thumbnail" style="background-color: #f1f1f1;">' \
                                '<img src="' + row.image.url + '" alt="">' \
                            '</div>' \
                        '</li>'

        return HttpResponse(data)

class ClientAjax(TemplateView):
    def get(self, request, *args, **kwargs):
        offset = int(kwargs['offset'])
        limit = int(kwargs['limit'])
        dataClient = Ourclient.objects.filter(status='True').order_by('-id')[offset:limit]

        data = ''
        if dataClient.count() > 0:
            for row in dataClient:
                data += '<div class="client">' \
                            '<img class="client-logo" src="' + row.image.url + '">' \
                        '</div>'

        return HttpResponse(data)

class HighlightAjax(TemplateView):
    def get(self, request, *args, **kwargs):
        offset = int(kwargs['offset'])
        limit = int(kwargs['limit'])
        dataHighlight = EventGalery.objects.filter(status='True').order_by('-id')[offset:limit]

        data = ''
        if dataHighlight.count() > 0:
            for row in dataHighlight:
                data += '<div class="portfolio-item">' \
                            '<div class="portfolio clearfix">' \
                                '<a href="/detail-event/' + str(row.id) + '/' + slugify(row.title) + '" class="portfolio-image">' \
                                    '<img src="' + row.image.url + '" alt="" />' \
                                    '<div class="portfolio-overlay">' \
                                        '<div class="thumb-info">' \
                                            '<h5 class="headingborder"><span>' + row.title + '</span></h5>' \
                                        '</div>' \
                                    '</div>' \
                                '</a>' \
                            '</div>' \
                        '</div>'

        return HttpResponse(data)
