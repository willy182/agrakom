from django.conf.urls import url
from modules.cms.user.views import Create, Edit, List, GetList,SetRole,Delete
app_name = 'user'
urlpatterns = [
    url(r'^$', List.as_view(), name='user'),
    # our client
    url(r'^add/$', Create.as_view(), name='add-user'),
    url(r'^edit/$', Edit.as_view(), name='edit-user'),
    url(r'^get-list/$', GetList.as_view(), name='get-user'),
    url(r'^set-role/$', SetRole.as_view(), name='set-role'),
    url(r'^delete/$', Delete.as_view(), name='delete-user'),

]
