from django.conf.urls import url
from modules.cms.event.views import Create, Edit, List, GetList, CreateDetail, EditDetail, ListDetail, GetListDetail

app_name = 'event'
urlpatterns = [
    url(r'^$', List.as_view(), name='event'),
    # awards
    url(r'^add/$', Create.as_view(), name='add-event'),
    url(r'^edit/$', Edit.as_view(), name='edit-event'),
    url(r'^get-list/$', GetList.as_view(), name='get-event'),
    # detail
    url(r'^detail/$', ListDetail.as_view(), name='detail-event'),
    url(r'^detail/add/$', CreateDetail.as_view(), name='add-detil-event'),
    url(r'^detail/edit/$', EditDetail.as_view(), name='edit-detil-event'),
    url(r'^detail/get-list/$', GetListDetail.as_view(), name='get-detail-event'),

]
