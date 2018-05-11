from django.conf.urls import url
from modules.cms.auth.views import Login, Logout

app_name = 'auth'
urlpatterns = [
    url(r'^$', Login.as_view(), name='role'),
    # our client
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),

]
