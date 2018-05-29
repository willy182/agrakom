from django.conf.urls import url
from modules.cms.aboutus.views import AboutUsList, CreateAboutus, GetListAboutUs, EditAboutus, AboutUsSliderList, GetListAboutUsSlider, CreateAboutusSlider, EditAboutusSlider, DeleteAboutus, \
    DeleteAboutusSlider

app_name = 'aboutus'
urlpatterns = [
    url(r'^$', AboutUsList.as_view(), name='aboutus'),
    # about us
    url(r'^add/$', CreateAboutus.as_view(), name='add-aboutus'),
    url(r'^edit/$', EditAboutus.as_view(), name='edit-aboutus'),
    url(r'^get-list/$', GetListAboutUs.as_view(), name='get-aboutus'),
    url(r'^delete/$', DeleteAboutus.as_view(), name='delete-aboutus'),
    # about us slider
    url(r'^slider/$', AboutUsSliderList.as_view(), name='aboutus-slider'),
    url(r'^slider/add/$', CreateAboutusSlider.as_view(), name='add-aboutus-slider'),
    url(r'^slider/edit/$', EditAboutusSlider.as_view(), name='edit-aboutus-slider'),
    url(r'^slider/get-list/$', GetListAboutUsSlider.as_view(), name='get-aboutus-slider'),
    url(r'^slider/delete/$', DeleteAboutusSlider.as_view(), name='delete-aboutus-slider'),


]
