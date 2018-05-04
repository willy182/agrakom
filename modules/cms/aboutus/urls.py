from django.conf.urls import url
from modules.cms.aboutus.views import AboutUsList


urlpatterns = [
    url(r'^$', AboutUsList.as_view(), name='about-us'),

]