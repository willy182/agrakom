from django.conf.urls import url
from modules.cms.aboutus.views import AboutUsList

app_name = 'aboutus'
urlpatterns = [
    url(r'^$', AboutUsList.as_view(), name='aboutus'),

]