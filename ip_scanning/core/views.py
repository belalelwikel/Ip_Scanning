import re
from django.shortcuts import render
from rest_framework.generics import GenericAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

from celery.result import AsyncResult
from .serializers import IpScanSerializer

from .tasks import get_ip_info


class IpScanView(GenericAPIView):
    serializer_class = IpScanSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        ip_list = serializer.validated_data['ips']

        for ip in ip_list:
            get_ip_info.delay(user.username, ip) 

        return Response({'status': 'Processing IPs'}, status=status.HTTP_202_ACCEPTED)
