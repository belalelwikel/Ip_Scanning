from config.websocket import *

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/ip_scanner/', IpScanner.as_asgi()),
]

