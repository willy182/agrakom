import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from modules.cms.ourclients.forms import CreateOurClientsForm
from modules.cms.ourclients.models import Ourclient


class List(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(List, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_client = Ourclient.objects.all().order_by("id")

        cust_context = {
            'all_client': all_client,
        }
        return render(request, 'cms/ourclients/index.html', context=cust_context)


class Create(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Create, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateOurClientsForm()
        perms = json.dumps([])
        return render(request, 'cms/ourclients/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateOurClientsForm(request.POST, request.FILES)

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/ourclients/')
        else:
            form = CreateOurClientsForm(request.POST, request.FILES)
            return render(request, 'cms/ourclients/add.html', {'form': form})


class Edit(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Edit, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = CreateOurClientsForm(instance=Ourclient.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False

        our_clients = Ourclient.objects.get(id=int(id))
        perms = json.dumps([])
        return render(request, 'cms/ourclients/edit.html', {'form': form, 'id': id, 'our_clients': our_clients, 'perms': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateOurClientsForm(data=request.POST, files=request.FILES, instance=Ourclient.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/ourclients/')
        else:

            return render(request, 'cms/ourclients/edit.html', {'form': form, 'id': id})


class GetList(BaseDatatableView):
    order_columns = ['id', 'title', 'description', 'image', 'caption', 'status', 'created_date', 'id']

    def get_initial_queryset(self):
        return Ourclient.objects.filter().order_by('id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        filter_by = self.request.GET.get(u'filter_by', None)

        if search:
            if filter_by == "status":
                qs = qs.filter(Q(status__icontains=search))


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
                # if len(item.description) > 25:
                #     description = item.description[0:25] + ' ...'
                # else:
                #     description = item.description

                json_data.append([
                    NumberingCounter,
                    # item.name,
                    # description,
                    '<img style="height:25px;width:25px;text-align:center" src="/' + item.image.url + '" onerror="this.src=''\'/static/images/no-image.png''\';" class="user-image" alt="User Image">',
                    # item.caption,
                    status,
                    item.created_datetime.strftime("%d/%m/%Y %H:%M"),
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/ourclients/edit/?id=' +
                    str(item.id) + '">''<i class="fa fa-edit"></i>'
                                   '<span> Edit</span>'
                                   '<span class="pull-right-container">'
                                   '<i class="fa pull-left"></i>'
                                   '</span>'
                                   '</a>'

                ])
                NumberingCounter += 1

        return json_data
