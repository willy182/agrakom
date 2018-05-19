import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from modules.cms.aboutus.forms import CreateAboutusForm, CreateSliderAboutUsForm
from modules.cms.aboutus.models import AboutUs, SliderAboutUs


class AboutUsList(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AboutUsList, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_about_us = AboutUs.objects.all().order_by("id")

        cust_context = {
            'all_about_us': all_about_us,
        }
        return render(request, 'cms/aboutus/index.html', context=cust_context)


class CreateAboutus(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAboutus, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateAboutusForm()
        perms = json.dumps([])
        return render(request, 'cms/aboutus/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateAboutusForm(data=request.POST)
        try:
            AboutUs.objects.get(title__iexact=request.POST.get('title'))
            form.errors.title = {'0': "Title Already Exists"}
            return render(request, 'cms/aboutus/add.html', {'form': form})

        except AboutUs.DoesNotExist:
            if form.is_valid():
                action = form.save(commit=False)
                # action.created_by = request.user
                action.save()
                return HttpResponseRedirect('/cms-agrakom/about-us/')
            else:
                form = CreateAboutusForm(data=request.POST)
                return render(request, 'cms/aboutus/add.html', {'form': form})


class EditAboutus(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditAboutus, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = CreateAboutusForm(instance=AboutUs.objects.get(id=int(id)))
        about_us = AboutUs.objects.get(id=int(id))
        perms = json.dumps([])
        return render(request, 'cms/aboutus/edit.html', {'form': form, 'id': id, 'about_us': about_us, 'perm': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateAboutusForm(data=request.POST, instance=AboutUs.objects.get(id=int(id)))

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/about-us/')
        else:

            return render(request, 'cms/aboutus/edit.html', {'form': form, 'id': id})


class GetListAboutUs(BaseDatatableView):
    order_columns = ['id', 'title', 'description', 'status', 'created_date', 'id']

    def get_initial_queryset(self):
        return AboutUs.objects.filter().order_by('id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        filter_by = self.request.GET.get(u'filter_by', None)

        if search:
            if filter_by == "title":
                qs = qs.filter(Q(title__icontains=search))
            elif filter_by == "description":
                qs = qs.filter(Q(description__icontains=search))
            elif filter_by == "status":
                qs = qs.filter(Q(status__icontains=search))
            else:
                qs = qs.filter(
                    Q(title__icontains=search) | Q(description__icontains=search) | Q(status__icontains=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        NumberingCounter = 1
        if qs:
            for item in qs:
                if item.status == True:
                    status = '<td>' \
                             '<p class="text-center">' \
                             '<span class="label label-success">Active</span>' \
                             '</p>' \
                             '</td>'
                else:
                    status = '<td>' \
                             '<p class="text-center">' \
                             '<span class="label label-danger">Not Active</span>' \
                             '</p>' \
                             '</td>'
                if len(item.description) > 25:
                    description = item.description[0:25] + ' ...'
                else:
                    description = item.description

                json_data.append([
                    NumberingCounter,
                    item.title,
                    description,
                    status,
                    item.created_datetime.strftime("%d/%m/%Y %H:%M"),
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/about-us/edit/?id=' +
                    str(item.id) + '">''<i class="fa fa-edit"></i>'
                                   '<span> Edit</span>'
                                   '<span class="pull-right-container">'
                                   '<i class="fa pull-left"></i>'
                                   '</span>'
                                   '</a>'
                    # '&nbsp|&nbsp'
                    # '<a style="widh:23px;" class="btn btn-danger btn-xs" href="/cms-agrakom/about-us/delete/?id=' +
                    # str(item.id) +'">''<i class="fa fa-trash  "></i>'
                    #                '<span> Delete</span>'
                    #                '<span class="pull-right-container">'
                    #                '<i class="fa pull-left"></i>'
                    #                '</span>'
                    #                '</a>'
                ])
                NumberingCounter += 1

        return json_data


class AboutUsSliderList(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AboutUsSliderList, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_about_us_slider = SliderAboutUs.objects.all().order_by("id")

        cust_context = {
            'all_about_us_slider': all_about_us_slider,
        }
        return render(request, 'cms/aboutus_slider/index.html', context=cust_context)


class CreateAboutusSlider(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAboutusSlider, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateSliderAboutUsForm()
        perms = json.dumps([])
        return render(request, 'cms/aboutus_slider/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateSliderAboutUsForm(request.POST, request.FILES)

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/about-us/slider/')
        else:
            form = CreateSliderAboutUsForm(request.POST, request.FILES)
            return render(request, 'cms/aboutus_slider/add.html', {'form': form})


class EditAboutusSlider(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditAboutusSlider, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = CreateSliderAboutUsForm(instance=SliderAboutUs.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False
        about_us = SliderAboutUs.objects.get(id=int(id))
        perms = json.dumps([])
        return render(request, 'cms/aboutus_slider/edit.html', {'form': form, 'id': id, 'about_us': about_us, 'perms': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateSliderAboutUsForm(data=request.POST, files=request.FILES, instance=SliderAboutUs.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False
        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/about-us/slider/')
        else:

            return render(request, 'cms/aboutus_slider/edit.html', {'form': form, 'id': id})


class GetListAboutUsSlider(BaseDatatableView):
    order_columns = ['id', 'imags', 'caption', 'title', 'about_us__title', 'created_date', 'status', 'id']

    def get_initial_queryset(self):
        return SliderAboutUs.objects.filter().order_by('id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        filter_by = self.request.GET.get(u'filter_by', None)

        if search:
            if filter_by == "about-us":
                qs = qs.filter(Q(about_us__title__icontains=search))
            elif filter_by == "caption":
                qs = qs.filter(Q(caption__icontains=search))
            elif filter_by == "status":
                qs = qs.filter(Q(status__icontains=search))
            else:
                qs = qs.filter(
                    Q(about_us__name__icontains=search) | Q(caption__icontains=search) | Q(status__icontains=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        NumberingCounter = 1
        if qs:
            for item in qs:
                if item.status == True:
                    status = '<td>' \
                             '<p class="text-center">' \
                             '<span class="label label-success">Active</span>' \
                             '</p>' \
                             '</td>'
                else:
                    status = '<td>' \
                             '<p class="text-center">' \
                             '<span class="label label-danger">Not Active</span>' \
                             '</p>' \
                             '</td>'
                if len(item.caption) > 25:
                    caption = item.caption[0:25] + ' ...'
                else:
                    caption = item.caption


                json_data.append([
                    NumberingCounter,
                    '<img style="height:25px;width:25px;text-align:center" src="/' + item.image.url + '" onerror="this.src=''\'/static/images/no-image.png''\';" class="user-image" alt="User Image">',
                    caption,
                    item.about_us.title,
                    item.created_datetime.strftime("%d/%m/%Y %H:%M"),
                    status,
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/about-us/slider/edit/?id=' +
                    str(item.id) + '">''<i class="fa fa-edit"></i>'
                                   '<span> Edit</span>'
                                   '<span class="pull-right-container">'
                                   '<i class="fa pull-left"></i>'
                                   '</span>'
                                   '</a>'
                    # '&nbsp|&nbsp'
                    # '<a style="widh:23px;" class="btn btn-danger btn-xs" href="/cms-agrakom/about-us/delete/?id=' +
                    # str(item.id) +'">''<i class="fa fa-trash  "></i>'
                    #                '<span> Delete</span>'
                    #                '<span class="pull-right-container">'
                    #                '<i class="fa pull-left"></i>'
                    #                '</span>'
                    #                '</a>'
                ])
                NumberingCounter += 1

        return json_data
