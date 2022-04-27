from django.db import models
from users.models import User


class ResetPassword(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=50,null=True,blank=True)