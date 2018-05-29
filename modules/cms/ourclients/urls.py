from django.conf.urls import url
from modules.cms.ourclients.views import Create, Edit, List, GetList,Delete

app_name = 'ourclients'
urlpatterns = [
    url(r'^$', List.as_view(), name='clients'),
    # our client
    url(r'^add/$', Create.as_view(), name='add-clients'),
    url(r'^edit/$', Edit.as_view(), name='edit-clients'),
    url(r'^get-list/$', GetList.as_view(), name='get-clients'),
    url(r'^delete/$', Delete.as_view(), name='delete-clients'),

]
