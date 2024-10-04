from django.urls import path
from .views import *

app_name = "core"
urlpatterns = [
    path("ip_scan/", IpScanView.as_view(), name="get_ip"),
   
]
