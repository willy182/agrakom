from django.conf.urls import url
from modules.cms.dashboard.views import Dashboard


urlpatterns = [
    url(r'^$', Dashboard.as_view(), name='dashboard'),

]