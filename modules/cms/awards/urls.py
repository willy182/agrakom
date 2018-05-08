from django.conf.urls import url
from modules.cms.awards.views import CreateAwards, EditAwards, AwardsList, GetListAwards, AwardsdetailList, EditDetailGalery, CreateDetailGalery, GetListDetailGalery

app_name = 'awards'
urlpatterns = [
    url(r'^$', AwardsList.as_view(), name='awards'),
    # awards
    url(r'^add/$', CreateAwards.as_view(), name='add-awards'),
    url(r'^edit/$', EditAwards.as_view(), name='edit-awards'),
    url(r'^get-list/$', GetListAwards.as_view(), name='get-awards'),
    # detail
    url(r'^detail/$', AwardsdetailList.as_view(), name='detail-galery'),
    url(r'^detail/add/$', CreateDetailGalery.as_view(), name='add-detil-galery'),
    url(r'^detail/edit/$', EditDetailGalery.as_view(), name='edit-detil-galery'),
    url(r'^detail/get-list/$', GetListDetailGalery.as_view(), name='get-detail-galery'),

]
