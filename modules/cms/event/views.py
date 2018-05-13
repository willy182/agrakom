import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from modules.cms.event.forms import CreateEventForm, CreateEventDetailForm
from modules.cms.event.models import EventGalery, DetailEvent


class List(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(List, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_event = EventGalery.objects.all().order_by("id")

        cust_context = {
            'all_event': all_event,
        }
        return render(request, 'cms/event/index.html', context=cust_context)


class Create(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Create, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateEventForm()
        perms = json.dumps([])
        return render(request, 'cms/event/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateEventForm(request.POST, request.FILES)
        try:
            EventGalery.objects.get(title__iexact=request.POST.get('title'))
            form.errors.title = {'0': "Title Already Exists"}
            return render(request, 'cms/event/add.html', {'form': form})

        except EventGalery.DoesNotExist:
            if form.is_valid():
                action = form.save(commit=False)
                # action.created_by = request.user
                action.save()
                return HttpResponseRedirect('/cms-agrakom/event/')
            else:
                form = CreateEventForm(request.POST, request.FILES)
                return render(request, 'cms/event/add.html', {'form': form})


class Edit(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Edit, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = CreateEventForm(instance=EventGalery.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False

        event_galery = EventGalery.objects.get(id=int(id))
        perms = json.dumps([])
        return render(request, 'cms/event/edit.html', {'form': form, 'id': id, 'event_galery': event_galery, 'perms': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateEventForm(data=request.POST, files=request.FILES, instance=EventGalery.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/event/')
        else:

            return render(request, 'cms/event/edit.html', {'form': form, 'id': id})


class GetList(BaseDatatableView):
    order_columns = ['id', 'title', 'description', 'image', 'position', 'status', 'created_date', 'id']

    def get_initial_queryset(self):
        return EventGalery.objects.filter().order_by('id')

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
                    '<img style="height:25px;width:25px;text-align:center" src="/' + item.image.url + '" onerror="this.src=''\'/static/images/no-image.png''\';" class="user-image" alt="User Image">',
                    item.position,
                    status,
                    item.created_datetime.strftime("%d/%m/%Y %H:%M"),
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/event/edit/?id=' +
                    str(item.id) + '">''<i class="fa fa-edit"></i>'
                                   '<span> Edit</span>'
                                   '<span class="pull-right-container">'
                                   '<i class="fa pull-left"></i>'
                                   '</span>'
                                   '</a>'

                ])
                NumberingCounter += 1

        return json_data


class ListDetail(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ListDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_detail_event = DetailEvent.objects.all().order_by("id")

        cust_context = {
            'all_detail_event': all_detail_event,
        }
        return render(request, 'cms/event_detail/index.html', context=cust_context)


class CreateDetail(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateEventDetailForm()
        perms = json.dumps([])
        return render(request, 'cms/event_detail/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateEventDetailForm(request.POST, request.FILES)

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/event/detail/')
        else:
            form = CreateEventDetailForm(request.POST, request.FILES)
            return render(request, 'cms/event_detail/add.html', {'form': form})


class EditDetail(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditDetail, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = CreateEventDetailForm(instance=DetailEvent.objects.get(id=int(id)))
        event_detail = DetailEvent.objects.get(id=int(id))
        perms = json.dumps([])
        return render(request, 'cms/event_detail/edit.html', {'form': form, 'id': id, 'event_detail': event_detail, 'perms': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateEventDetailForm(data=request.POST, files=request.FILES, instance=DetailEvent.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/event/detail/')
        else:

            return render(request, 'cms/detail_detail/edit.html', {'form': form, 'id': id})


class GetListDetail(BaseDatatableView):
    order_columns = ['id', 'imags', 'caption', 'title', 'about_us__title', 'position', 'created_date', 'status', 'id']

    def get_initial_queryset(self):
        return DetailEvent.objects.filter().order_by('id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        filter_by = self.request.GET.get(u'filter_by', None)

        if search:
            if filter_by == "about-us":
                qs = qs.filter(Q(event_galery__title__icontains=search))
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

                if item.position:
                    position = item.position
                else:
                    position = '-'

                json_data.append([
                    NumberingCounter,
                    '<img style="height:25px;width:25px;text-align:center" src="/' + item.image.url + '" onerror="this.src=''\'/static/images/no-image.png''\';" class="user-image" alt="User Image">',
                    caption,
                    item.event_galery.title,
                    position,
                    item.created_datetime.strftime("%d/%m/%Y %H:%M"),
                    status,
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/event/detail/edit/?id=' +
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
