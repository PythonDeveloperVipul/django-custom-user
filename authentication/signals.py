from email import message
from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from .utils import send_mail_reset_password
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    url = reverse('password_reset:reset-password-request')
    token = reset_password_token.key
    subject = "Reset your password",
    message = f"{url}?token={token}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = reset_password_token.user.email
    send_mail_reset_password(subject,
                             message, from_email, to_email)
