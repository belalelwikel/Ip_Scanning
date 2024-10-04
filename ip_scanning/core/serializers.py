# serializers.py
from rest_framework import serializers

class IpScanSerializer(serializers.Serializer):
    ips = serializers.ListField(
        child=serializers.IPAddressField(),
        allow_empty=False,
    )