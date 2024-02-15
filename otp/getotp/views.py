from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from kavenegar import KavenegarAPI
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from getotp.models import OtpRequest
from getotp.serializers import RequestOtpSerializer, RequestOtpResponseSerializer, VerifyOtpSerializer, \
    VerifyOtpResponseSerializer


class OncePerMinuteThrottle(UserRateThrottle):
    rate = '1/minute'


# Create your views here.
class RequestOtp(APIView):
    throttle_classes = [OncePerMinuteThrottle]

    def post(self, request):
        serializer = RequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            req = OtpRequest()
            req.phone = serializer.validated_data['phone']
            req.channel = serializer.validated_data['channel']
            req.generate_password()
            req.save()
            api = KavenegarAPI(settings.SMS_API_KEY)
            response = api.verify_lookup({
                'receptor': req.phone,
                'token': f'کد تایید شما{req.password}',
            })
            print(response)
            return Response(RequestOtpResponseSerializer(req).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            querry = OtpRequest.objects.filter(
                request_id=serializer.validated_data['request_id'],
                phone=serializer.validated_data['phone'],
                valid_until__gte=datetime.now()
            )
            if querry.exists():
                user = get_user_model()
                userq = user.objects.filter(username=serializer.validated_data['phone'])
                if userq.exists():
                    user = userq.first()
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(data=VerifyOtpResponseSerializer({'token': token, 'new_user': False}).data)
                else:
                    user = user.objects.create(username=serializer.validated_data['phone'])
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(data=VerifyOtpResponseSerializer({'token': token, 'new_user': True}).data)
            else:
                return Response(None, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
