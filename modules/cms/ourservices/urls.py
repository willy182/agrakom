from django.conf.urls import url
from modules.cms.ourservices.views import Create, Edit, List, GetList, CreateDetail, EditDetail, ListDetail, GetListDetail

app_name = 'ourservices'
urlpatterns = [
    url(r'^$', List.as_view(), name='event'),
    # awards
    url(r'^add/$', Create.as_view(), name='add-services'),
    url(r'^edit/$', Edit.as_view(), name='edit-services'),
    url(r'^get-list/$', GetList.as_view(), name='get-services'),
    # detail
    url(r'^detail/$', ListDetail.as_view(), name='detail-services'),
    url(r'^detail/add/$', CreateDetail.as_view(), name='add-detil-services'),
    url(r'^detail/edit/$', EditDetail.as_view(), name='edit-detil-services'),
    url(r'^detail/get-list/$', GetListDetail.as_view(), name='get-detail-services'),

]
