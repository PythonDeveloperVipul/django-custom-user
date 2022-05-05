from tabnanny import verbose
from django.db import models
from users.models import User
deposite_withdraw_amount_choice = (
    ('Deposite', 'Deposite'), ('Withdraw', 'Withdraw'))


class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=12)
    account_name = models.CharField(max_length=255)
    open_date = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255)
    total_amount = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.email}'


class Client_Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.CharField(
        max_length=10, choices=deposite_withdraw_amount_choice)
    available_balance=models.FloatField()

    class Meta:
        verbose_name_plural='client transaction'
