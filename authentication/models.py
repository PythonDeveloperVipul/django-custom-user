from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    url = reverse('password_reset:reset-password-request')
    token = reset_password_token.key
    email_plaintext_message = f"{url}?token={token}"

    send_mail(

        "Password Reset for Django-Custom-User",

        email_plaintext_message,

        settings.EMAIL_HOST_USER,

        [reset_password_token.user.email],

        fail_silently=False
    )
