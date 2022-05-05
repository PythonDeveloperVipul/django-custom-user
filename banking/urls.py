from django.urls import path,include
from .views import AccountApiView,Client_Transaction_View,BalanceInquiryApi

urlpatterns = [
    path('account_create/',AccountApiView.as_view(),name='account_create'),
    path('client_transaction/',Client_Transaction_View.as_view(),name='client_transaction'),
    path('balanceshow/',BalanceInquiryApi.as_view(),name='balance_show'),
]