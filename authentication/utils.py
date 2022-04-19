from django.core.mail import send_mail


def send_mail_reset_password(subject,
                             message, from_email, to_email):
    send_mail(

        subject,

        message,

        from_email,

        [to_email],

        fail_silently=False
    )
