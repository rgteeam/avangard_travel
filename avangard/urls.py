"""avangard URL Configuration

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
from django.contrib import admin
from rest_framework import routers
from avangard.account.views import check_email
from avangard.museums.api import MuseumViewSet, ScheduleViewSet, CompanyViewSet
from avangard.orders.api import OrderViewSet
from avangard.tourtickets.api import TourticketViewSet
from avangard.proxycard.api import ProxycardViewSet
from avangard.chat.api import GetDialogsViewSet, MessageHistoryViewSet, MarkAsRead
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'museums', MuseumViewSet, 'museum')
router.register(r'companys', CompanyViewSet, 'company')
router.register(r'schedule', ScheduleViewSet, 'schedule')
router.register(r'orders', OrderViewSet, 'order')
router.register(r'tourtickets', TourticketViewSet, 'tourticket')
router.register(r'proxycard', ProxycardViewSet, 'proxycard')
router.register(r'chat_rooms', GetDialogsViewSet, 'chat_room')
router.register(r'messages', MessageHistoryViewSet, 'messages')


urlpatterns = [
    url(r'^api/rest-auth/', include('rest_auth.urls')),
    url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/rest-auth/check-email/', check_email),
    url(r'^api/chat/mark_as_read/', MarkAsRead.as_view(), name='mark_as_read'),

    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('avangard.account.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^export/', include('avangard.export.urls')),
    url(r'^tourtickets/', include('avangard.tourtickets.urls')),
    url(r'^proxycard/', include('avangard.proxycard.urls')),
    url(r'^settings/', include('avangard.setting.urls')),
    url(r'^orders/', include('avangard.orders.urls')),
    url(r'^chat/', include('avangard.chat.urls')),
    url(r'^', include('avangard.museums.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
