import requests
from celery import shared_task
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import ipinfo

def get_ip_details(ip_address=None):
	ipinfo_token = getattr(settings, "IPINFO_TOKEN", None)
	ip_data = ipinfo.getHandler(ipinfo_token)
	ip_data = ip_data.getDetails(ip_address)
	return ip_data



@shared_task
def get_ip_info(user,ip):
	ip_info=get_ip_details(ip)

	channel_layer = get_channel_layer()

	group_name = f'user_{user}'
	async_to_sync(channel_layer.group_send)(
		group_name,
		{
			'type': 'send_ip_info',
			'ip_info': ip_info.__dict__
		}
	)

