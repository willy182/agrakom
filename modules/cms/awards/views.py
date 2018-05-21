import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from modules.cms.awards.forms import CreateAwardsForm, CreateAwardDetailForm
from modules.cms.awards.models import AwardsGalery, DetailGalery


class AwardsList(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AwardsList, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_awards = AwardsGalery.objects.filter().order_by("id")

        cust_context = {
            'all_awards': all_awards,
        }
        return render(request, 'cms/awards/index.html', context=cust_context)


class CreateAwards(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAwards, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateAwardsForm()
        perms = json.dumps([])
        return render(request, 'cms/awards/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateAwardsForm(request.POST, request.FILES)

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/awards/')
        else:
            form = CreateAwardsForm(request.POST, request.FILES)
            return render(request, 'cms/awards/add.html', {'form': form})


class EditAwards(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditAwards, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        form = None
        id = request.GET.get('id')
        form = CreateAwardsForm(instance=AwardsGalery.objects.get(id=int(id)))
        awards_galery = AwardsGalery.objects.get(id=int(id))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False
        perms = json.dumps([])
        return render(request, 'cms/awards/edit.html', {'form': form, 'id': id, 'about_us': awards_galery, 'perms': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateAwardsForm(data=request.POST, files=request.FILES, instance=AwardsGalery.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/awards/')
        else:

            return render(request, 'cms/awards/edit.html', {'form': form, 'id': id})


class GetListAwards(BaseDatatableView):
    order_columns = ['id', 'title', 'description', 'image', 'status', 'created_date', 'id']

    def get_initial_queryset(self):
        return AwardsGalery.objects.filter().order_by('id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        filter_by = self.request.GET.get(u'filter_by', None)

        if search:
            # if filter_by == "title":
            #     qs = qs.filter(Q(title__icontains=search))
            # elif filter_by == "description":
            #     qs = qs.filter(Q(description__icontains=search))
            if filter_by == "status":
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
                # if len(item.description) > 25:
                #     description = item.description[0:25] + ' ...'
                # else:
                #     description = item.description

                json_data.append([
                    NumberingCounter,
                    # item.title,
                    # description,
                    '<img style="height:25px;width:25px;text-align:center" src="/' + item.image.url + '" onerror="this.src=''\'/static/images/no-image.png''\';" class="user-image" alt="User Image">',
                    status,
                    item.created_datetime.strftime("%d/%m/%Y %H:%M"),
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/awards/edit/?id=' +
                    str(item.id) + '">''<i class="fa fa-edit"></i>'
                                   '<span> Edit</span>'
                                   '<span class="pull-right-container">'
                                   '<i class="fa pull-left"></i>'
                                   '</span>'
                                   '</a>'

                ])
                NumberingCounter += 1

        return json_data


class AwardsdetailList(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AwardsdetailList, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        all_detail_galery = DetailGalery.objects.all().order_by("id")

        cust_context = {
            'all_detail_galery': all_detail_galery,
        }
        return render(request, 'cms/awards_detail/index.html', context=cust_context)


class CreateDetailGalery(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateDetailGalery, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateAwardDetailForm()
        perms = json.dumps([])
        return render(request, 'cms/awards_detail/add.html', {'form': form, 'perms': perms})

    def post(self, request, *args, **kwargs):
        form = CreateAwardDetailForm(request.POST, request.FILES)

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/awards/detail/')
        else:
            form = CreateAwardDetailForm(request.POST, request.FILES)
            return render(request, 'cms/awards_detail/add.html', {'form': form})


class EditDetailGalery(TemplateView):
    @method_decorator(login_required(login_url='/cms-agrakom/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(EditDetailGalery, self).dispatch(request, *args, **kwargs)

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        form = CreateAwardDetailForm(instance=DetailGalery.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False
        about_us = DetailGalery.objects.get(id=int(id))
        perms = json.dumps([])
        return render(request, 'cms/awards_detail/edit.html', {'form': form, 'id': id, 'about_us': about_us, 'perms': perms})

    # @method_decorator(permission_required('awb.create_third_party_logistics', raise_exception=True))
    def post(self, request, *args, **kwargs):

        id = request.POST.get('id')
        form = CreateAwardDetailForm(data=request.POST, files=request.FILES, instance=DetailGalery.objects.get(id=int(id)))
        for k, v in form.base_fields.items():
            if k == 'image':
                v.required = False

        if form.is_valid():
            action = form.save(commit=False)
            # action.created_by = request.user
            action.save()
            return HttpResponseRedirect('/cms-agrakom/awards/detail/')
        else:

            return render(request, 'cms/awards_detail/edit.html', {'form': form, 'id': id})


class GetListDetailGalery(BaseDatatableView):
    order_columns = ['id', 'imags', 'caption', 'title', 'about_us__title', 'created_date', 'status', 'id']

    def get_initial_queryset(self):
        return DetailGalery.objects.filter().order_by('id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        filter_by = self.request.GET.get(u'filter_by', None)

        if search:
            if filter_by == "about-us":
                qs = qs.filter(Q(awards_galery__title__icontains=search))
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
                    item.awards_galery.title,
                    item.created_datetime.strftime("%d/%m/%Y %H:%M"),
                    status,
                    '<a style="widh:23px;" class="btn btn-warning btn-xs" href="/cms-agrakom/awards/detail/edit/?id=' +
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
