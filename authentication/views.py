from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from .models import ResetPassword
from .serializers import RegisterSerializer
from .utils import send_mail_reset_password


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class Restpassword(APIView):
    def get(self, request):
        to_email = request.data.get('email', None)
        user = User.objects.get(email=to_email)
        self.unique_id = get_random_string(length=32)
        if user is not None:
            subject = 'Reset Your Password'
            from_email = settings.DEFAULT_FROM_EMAIL
            try:
                reset_password = ResetPassword(user=user, token=self.unique_id)
                reset_password.save()
                send_mail_reset_password(
                    subject, reset_password.token, from_email, to_email)
            except:
                reset_password = ResetPassword.objects.get(user=user)
            context = {'token': reset_password.token, 'email': user.email}
            return Response(context)

    def post(self, request):
        token = self.request.GET.get('token')
        try:
            confirmation_token = ResetPassword.objects.get(token=token)
            if confirmation_token is not None:
                user = User.objects.get(email=confirmation_token.user.email)
                user.set_password(self.request.GET.get('password'))
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'msg': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
