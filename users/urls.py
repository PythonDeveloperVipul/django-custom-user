from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyObtainTokenPairView, RegisterView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='users_register'),
    path('password_reset/',
         include('django_rest_passwordreset.urls', namespace='forgot_password')),
]
