from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.auth.models import Group, Permission
import json

from modules.cms.role.forms import GroupForm


class List(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(List, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        perms = json.dumps([])
        cust_context = {'perms':perms}
        return render(request, 'cms/role/index.html', context=cust_context)


class Create(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        cust_context = {}
        return super(Create, self).dispatch(request, cust_context, *args, **kwargs)

    def get(self, request, content, *args, **kwargs):
        form = GroupForm()
        perms = json.dumps([])
        return render(request, 'cms/role/add.html', {'form': form, 'perms': perms})

    def post(self, request, content, *args, **kwargs):
        form = GroupForm(request.POST)
        name = request.POST.get('name')
        perms = request.POST.getlist('permissions')

        if form.is_valid():

            new_group = Group.objects.create(name=name)
            list_permissions = perms
            for id_permissions in range(len(list_permissions)):
                get_permission = Permission.objects.get(id=int(list_permissions[id_permissions]))
                new_group.permissions.add(get_permission)

            return HttpResponseRedirect('/cms-agrakom/role/')
        else:
            return render(request, 'cms/role/add.html', {'form': form})


def list_to_str(value):
    """
    Convert value of list to integer
        :param value: the list
    """
    c = []
    for item in value:
        c.append(str(item))
    return c


def diff(first, second):
    """
    Get difference between two list
        :param first: first list
        :param second: second list
    """
    second = set(second)
    return [item for item in first if item not in second]


class Edit(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        cust_context = {}
        return super(Edit, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        group = Group.objects.get(id=int(id))
        form = GroupForm(instance=group)
        perms = json.dumps(list_to_str(list(group.permissions.values_list('id', flat=True))))
        return render(request, 'cms/role/add.html', {'form': form, 'perms': perms, 'id': id})

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        group = Group.objects.get(id=int(id))
        form = GroupForm(request.POST, instance=group)
        name = request.POST.get('name')
        perms = request.POST.getlist('permissions')

        if form.is_valid():
            old_permission = list_to_str(list(
                group.permissions.values_list('id', flat=True)))

            # handle old permission first
            permission_to_delete = diff(old_permission, perms)
            for p in permission_to_delete:
                permission = Permission.objects.get(id=p)
                group.permissions.remove(permission)

            # process the new one
            for id_permissions in range(len(perms)):
                get_permission = Permission.objects.get(
                    id=int(perms[id_permissions]))
                group.permissions.add(get_permission)

            group.save()

            return HttpResponseRedirect('/cms-agrakom/role/')
        else:
            return render(request, 'cms/role/add.html', {'form': form, 'perms': json.dumps(perms)})



class GetList(BaseDatatableView):
    order_columns = ['id', 'username', 'last_login', '', 'status', 'id']

    def get_initial_queryset(self):
        return Group.objects.filter().order_by('id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        filter_by = self.request.GET.get(u'filter_by', None)

        if search:
            if filter_by == "username":
                qs = qs.filter(Q(name__icontains=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        NumberingCounter = 1
        if qs:
            for item in qs:

                if self.request.user.username == 'adminagrakom':
                    edit = '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/role/edit/?id=' + str(item.id) + '"><i class="fa fa-edit"></i>'' \
                                                    ''<span> Edit</span>'' \
                                                    ''<span class="pull-right-container">'' \
                                                    ''<i class="fa pull-left"></i>'' \
                                                    ''</span>'' \
                                                    ''</a>'' \
                                                    ''&nbsp&nbsp'
                else:
                    if (self.request.user.groups.get().permissions.filter(codename='change_group').count() > 0):

                        edit= '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/role/edit/?id=' +str(item.id) + '"><i class="fa fa-edit"></i>'' \
                                ''<span> Edit</span>'' \
                                ''<span class="pull-right-container">'' \
                                ''<i class="fa pull-left"></i>'' \
                                ''</span>'' \
                                ''</a>'' \
                                ''&nbsp&nbsp'
                    else:
                        edit = ''

                if self.request.user.username == 'adminagrakom':
                    if item.user_set.all():
                        delete = '<a style="widh:23px;" class="btn btn-danger btn-xs" onclick="delete_info(\'' + 'data tidak bisa dihapus  karena masih terdapat user yg menggunakan role ini' + '\')" href="#">'' \
                                ''<i class="fa fa-trash  "></i>''<span> Delete</span>'' \
                                ''<span class="pull-right-container">'' \
                                ''<i class="fa pull-left"></i>'' \
                                ''</span>'' \
                                ''</a>'

                    else:
                        delete = '<a style="widh:23px;" class="btn btn-danger btn-xs" onclick="delete_confirm(\'' + '/cms-agrakom/role/delete/?id=' + str(
                            item.id) + '\')" href="#"><i class="fa fa-trash  "></i>'' \
                                ''<span> Delete</span>'' \
                                ''<span class="pull-right-container">'' \
                                ''<i class="fa pull-left"></i>'' \
                                ''</span>'' \
                                ''</a>'

                else:

                    if (self.request.user.groups.get().permissions.filter(codename='delete_group').count() > 0):

                        if item.user_set.all():
                            delete = '<a style="widh:23px;" class="btn btn-danger btn-xs" onclick="delete_info(\'' + 'data tidak bisa dihapus  karena masih terdapat user yg menggunakan role ini' + '\')" href="#">'' \
                                    ''<i class="fa fa-trash  "></i>''<span> Delete</span>'' \
                                    ''<span class="pull-right-container">'' \
                                    ''<i class="fa pull-left"></i>'' \
                                    ''</span>'' \
                                    ''</a>'

                        else:
                            delete = '<a style="widh:23px;" class="btn btn-danger btn-xs" onclick="delete_confirm(\''+'/cms-agrakom/role/delete/?id=' +str(item.id) +'\')" href="#"><i class="fa fa-trash  "></i>'' \
                                    ''<span> Delete</span>'' \
                                    ''<span class="pull-right-container">'' \
                                    ''<i class="fa pull-left"></i>'' \
                                    ''</span>'' \
                                    ''</a>'
                    else:
                        delete = ''

                json_data.append([
                    NumberingCounter,
                    item.name,
                    edit+delete

                ])
                NumberingCounter += 1

        return json_data

class Delete(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Delete, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        delete_data = Group.objects.get(id=int(id))
        all_permission_group  = delete_data.permissions.all()
        for row in all_permission_group:
            permission = Permission.objects.get(id=row.id)
            delete_data.permissions.remove(permission)
        delete_data.delete()
        return HttpResponseRedirect('/cms-agrakom/role/')