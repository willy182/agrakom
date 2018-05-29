from django.conf.urls import url
from modules.cms.whatsnew.views import Create, Edit, List, GetList, CreateDetail, EditDetail, ListDetail, GetListDetail,DeleteDetail,Delete

app_name = 'whatsnew'
urlpatterns = [
    url(r'^$', List.as_view(), name='whatsnew'),
    # awards
    url(r'^add/$', Create.as_view(), name='add-whatsnew'),
    url(r'^edit/$', Edit.as_view(), name='edit-whatsnew'),
    url(r'^get-list/$', GetList.as_view(), name='get-whatsnew'),
    url(r'^delete/$', Delete.as_view(), name='delete-whatsnew'),

    # detail
    url(r'^detail/$', ListDetail.as_view(), name='detail-whatsnew'),
    url(r'^detail/add/$', CreateDetail.as_view(), name='add-detil-whatsnew'),
    url(r'^detail/edit/$', EditDetail.as_view(), name='edit-detil-whatsnew'),
    url(r'^detail/get-list/$', GetListDetail.as_view(), name='get-detail-whatsnew'),
    url(r'^detail/delete/$', DeleteDetail.as_view(), name='delete-detail-whatsnew'),


]
