from django.urls import path
from . import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('',views.home,name='home'),
    path('get_station_details',views.get_station_details,name='get_station_details'),
    path('home/divin/flood_monitor/static/<path:path>/', serve, {'document_root': settings.STATIC_ROOT}),
]