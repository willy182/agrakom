"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

# from django.contrib import admin
from modules.frontend.views import HomeAgrakom

urlpatterns = [
    url(r'^$', HomeAgrakom.as_view(), name='home'),
    url(r'^cms-agrakom/', include('modules.cms.dashboard.urls')),
    url(r'^cms-agrakom/about-us/', include('modules.cms.aboutus.urls')),
    url(r'^cms-agrakom/awards/', include('modules.cms.awards.urls')),
    url(r'^cms-agrakom/event/', include('modules.cms.event.urls')),
    url(r'^cms-agrakom/ourservices/', include('modules.cms.ourservices.urls')),
    url(r'^cms-agrakom/ourclients/', include('modules.cms.ourclients.urls')),
    url(r'^cms-agrakom/user/', include('modules.cms.user.urls')),
    url(r'^cms-agrakom/role/', include('modules.cms.role.urls')),
    url(r'^cms-agrakom/auth/', include('modules.cms.auth.urls')),

]
