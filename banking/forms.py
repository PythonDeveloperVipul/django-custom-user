from django import forms
from .models import Client_Transaction
class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class ClientTransactionForm(forms.ModelForm):
    amount=forms.FloatField()
    transaction_type=forms.CharField(max_length=50)

    class Meta:
        model=Client_Transaction
        exclude=['account','available_balance']