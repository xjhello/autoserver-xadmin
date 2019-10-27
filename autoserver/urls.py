"""autoserver URL Configuration

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
from django.contrib import admin
from django.conf.urls import url,include

import xadmin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/',include(xadmin.site.urls)),#添加新路由
    url(r'^api/', include('Api.urls')),
    # url(r'^info/main/$',getall include('Api.urls')),

    # url(r'^backend/', include('backend.urls')),
    # url(r'^info/cpuusage/$', _views.cpuusage, name='cpuusage')

   # url(r'^main/$', 'views.getall', name='main'),
   # url(r'^info/uptime/$', views.uptime, name='uptime'),
   # url(r'^info/memory/$', views.memusage, name='memusage'),
   # url(r'^info/cpuusage/$', views.cpuusage, name='cpuusage'),
   # url(r'^info/getdisk/$', views.getdisk, name='getdisk'),
   # url(r'^info/getusers/$', views.getusers, name='getusers'),
   # url(r'^info/getips/$', views.getips, name='getips'),
   # url(r'^info/gettraffic/$', 'usage.views.gettraffic', name='gettraffic'),
   # url(r'^info/proc/$', 'usage.views.getproc', name='getproc'),
   # url(r'^info/getdiskio/$', 'usage.views.getdiskio', name='getdiskio'),
   # url(r'^info/loadaverage/$', 'usage.views.loadaverage', name='loadaverage'),
   # url(r'^info/platform/([\w\-\.]+)/$', 'usage.views.platform', name='platform'),
   # url(r'^info/getcpus/([\w\-\.]+)/$', 'usage.views.getcpus', name='getcpus'),
   # url(r'^info/getnetstat/$', 'usage.views.getnetstat', name='getnetstat')

]


