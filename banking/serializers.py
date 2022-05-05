from .models import Account,Client_Transaction
from rest_framework import serializers
from .models import Account


class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['bank_name','branch_name','branch_code','account_name','open_date','account_type','total_amount']
       

class Client_Transaction_Serializers(serializers.ModelSerializer):
    class Meta:
        model=Client_Transaction
        exclude=['account','available_balance']

