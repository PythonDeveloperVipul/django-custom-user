from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from .models import ResetPassword
from .serializers import RegisterSerializer,ChangePasswordSerializer
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
            except:
                reset_password = ResetPassword.objects.get(user=user)
                reset_password.token=self.unique_id
                reset_password.save()
            send_mail_reset_password(
                subject, reset_password.token, from_email, to_email)

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




class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)