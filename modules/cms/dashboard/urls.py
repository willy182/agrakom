from django.conf.urls import url
from modules.cms.dashboard.views import Dashboard

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', Dashboard.as_view(), name='index'),

]