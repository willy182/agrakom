from django.conf.urls import url
from modules.cms.role.views import Create, List, GetList,Edit

app_name = 'role'
urlpatterns = [
    url(r'^$', List.as_view(), name='role'),
    # our client
    url(r'^add/$', Create.as_view(), name='add-role'),
    url(r'^edit/$', Edit.as_view(), name='edit-role'),
    url(r'^get-list/$', GetList.as_view(), name='get-role'),

]
