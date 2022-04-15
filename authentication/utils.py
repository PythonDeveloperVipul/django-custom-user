from django.core.mail import send_mail


def send_mail_reset_password(default_from_email, email_plaintext_message, reset_password_token):
    send_mail(

        "Reset your password",

        email_plaintext_message,

        default_from_email,

        [reset_password_token.user.email],

        fail_silently=False
    )
