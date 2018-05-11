from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.auth.models import User, Group


class List(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(List, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        cust_context = {}
        return render(request, 'cms/user/index.html', context=cust_context)


class Create(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Create, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'cms/user/add.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.is_superuser =True
            action.last_login = timezone.now()
            action.save()
            return HttpResponseRedirect('/cms-agrakom/user/')
        else:
            return render(request, 'cms/user/add.html', {'form': form})


class Edit(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Edit, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = UserCreationForm(instance=User.objects.get(id=int(id)))

        user = User.objects.get(id=int(id))
        return render(request, 'cms/user/edit.html', {'form': form, 'id': id, 'user': user})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = UserCreationForm(data=request.POST, instance=User.objects.get(id=int(id)))

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/user/')
        else:

            return render(request, 'cms/user/edit.html', {'form': form, 'id': id})


class GetList(BaseDatatableView):
    order_columns = ['id', 'username', 'last_login', '', 'status', 'id']

    def get_initial_queryset(self):
        return User.objects.filter().order_by('id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        filter_by = self.request.GET.get(u'filter_by', None)

        if search:
            if filter_by == "username":
                qs = qs.filter(Q(username__icontains=search))
            else:
                qs = qs.filter(
                    Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        NumberingCounter = 1
        if qs:
            for item in qs:
                if item.is_active == True:
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
                get_group_usr = item.groups.all()

                if get_group_usr:
                    marlin_role = get_group_usr[0].name
                else:
                    marlin_role = '-'

                if item.last_login:
                    last_log = item.last_login.strftime("%d/%m/%Y %H:%M")
                else:
                    last_log = ''
                json_data.append([
                    NumberingCounter,
                    item.username,
                    marlin_role,
                    last_log,
                    status,
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/user/edit/?id=' +
                    str(item.id) + '">''<i class="fa fa-edit"></i>'
                                   '<span> Edit</span>'
                                   '<span class="pull-right-container">'
                                   '<i class="fa pull-left"></i>'
                                   '</span>'
                                   '</a>&nbsp|&nbsp'
                                   '<a style="widh:23px;" class="btn btn-info btn-xs" href="/cms-agrakom/user/set-role/?id=' +
                    str(item.id) + '">''<i class="fa fa-edit"></i>'
                                   '<span> Set Role</span>'
                                   '<span class="pull-right-container">'
                                   '<i class="fa pull-left"></i>'
                                   '</span>'
                                   '</a>'

                ])
                NumberingCounter += 1

        return json_data


class SetRole(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(SetRole, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        user = User.objects.get(id=int(id))
        groups = Group.objects.filter()
        return render(request, 'cms/user/set_role.html', {'id': id, 'groups': groups, 'user': user})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        get_user = User.objects.get(id=int(request.POST.get('id')))
        group = request.POST.get('group')
        if group is None:
            return redirect('cms-agrakom/user/set-role/?user_id=' + str(get_user.id) + '&msg=Marlin role is required')
        elif group == '':
            get_user.groups.clear()
        else:
            # update group user
            get_user.groups.clear()
            get_group = Group.objects.get(id=int(group))
            get_user.groups.add(get_group)

        return redirect('/cms-agrakom/user/')