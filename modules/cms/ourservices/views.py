import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from modules.cms.ourservices.forms import CreateServiceForm, CreateServiceDetailForm
from modules.cms.ourservices.models import OurServices, OurServiceDetail


class List(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(List, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_service = OurServices.objects.all().order_by("id")

        cust_context = {
            'all_service': all_service,
        }
        return render(request, 'cms/ourservices/index.html', context=cust_context)


class Create(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Create, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateServiceForm()
        perms = json.dumps([])
        return render(request, 'cms/ourservices/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateServiceForm(request.POST, request.FILES)
        try:
            OurServices.objects.get(title__iexact=request.POST.get('title'))
            form.errors.title = {'0': "Title Already Exists"}
            return render(request, 'cms/ourservices/add.html', {'form': form})

        except OurServices.DoesNotExist:
            if form.is_valid():
                action = form.save(commit=False)
                # action.created_by = request.user
                action.save()
                return HttpResponseRedirect('/cms-agrakom/ourservices/')
            else:
                form = CreateServiceForm(request.POST, request.FILES)
                return render(request, 'cms/ourservices/add.html', {'form': form})


class Edit(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Edit, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = CreateServiceForm(instance=OurServices.objects.get(id=int(id)))
        our_services = OurServices.objects.get(id=int(id))
        perms = json.dumps([])
        return render(request, 'cms/ourservices/edit.html', {'form': form, 'id': id, 'our_services': our_services, 'perms': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateServiceForm(request.POST, request.FILES, instance=OurServices.objects.get(id=int(id)))

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/ourservices/')
        else:

            return render(request, 'cms/ourservices/edit.html', {'form': form, 'id': id})


class GetList(BaseDatatableView):
    order_columns = ['id', 'title', 'description', 'image', 'status', 'created_date', 'id']

    def get_initial_queryset(self):
        return OurServices.objects.filter().order_by('id')

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
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/ourservices/edit/?id=' +
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
        all_detail_services = OurServiceDetail.objects.all().order_by("id")

        cust_context = {
            'all_detail_services': all_detail_services,
        }
        return render(request, 'cms/ourservices_detail/index.html', context=cust_context)


class CreateDetail(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateServiceDetailForm()
        perms = json.dumps([])
        return render(request, 'cms/ourservices_detail/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateServiceDetailForm(request.POST, request.FILES)

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/ourservices/detail/')
        else:
            form = CreateServiceDetailForm(request.POST, request.FILES)
            return render(request, 'cms/ourservices_detail/add.html', {'form': form})


class EditDetail(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditDetail, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = CreateServiceDetailForm(instance=OurServiceDetail.objects.get(id=int(id)))
        service_detail = OurServiceDetail.objects.get(id=int(id))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False
        perms = json.dumps([])
        return render(request, 'cms/ourservices_detail/edit.html', {'form': form, 'id': id, 'service_detail': service_detail, 'perms': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateServiceDetailForm(data=request.POST, files=request.FILES, instance=OurServiceDetail.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False
        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/ourservices/detail/')
        else:

            return render(request, 'cms/ourservices_detail/edit.html', {'form': form, 'id': id})


class GetListDetail(BaseDatatableView):
    order_columns = ['id', 'imags', 'caption', 'title', 'about_us__title', 'created_date', 'status', 'id']

    def get_initial_queryset(self):
        return OurServiceDetail.objects.filter().order_by('id')

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
                if item.description:
                    if len(item.description) > 25:
                        description = item.description[0:25] + ' ...'
                    else:
                        description = item.description
                else:

                    description = '-'

                json_data.append([
                    NumberingCounter,
                    item.title,
                    '<img style="height:25px;width:25px;text-align:center" src="/' + item.image.url + '" onerror="this.src=''\'/static/images/no-image.png''\';" class="user-image" alt="User Image">',
                    description,
                    item.created_datetime.strftime("%d/%m/%Y %H:%M"),
                    status,
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/ourservices/detail/edit/?id=' +
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
