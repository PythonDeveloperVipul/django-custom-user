from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import AccountSerializers, Client_Transaction_Serializers
from .models import Account
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import RegisterSerializer
from users.models import User
# Create your views here.


class AccountApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializers

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            sid = transaction.savepoint()
            user_serializer = RegisterSerializer(data=request.data)
            serializer = self.get_serializer(data=request.data)
            if user_serializer.is_valid():
                transaction.savepoint_commit(sid)
                user_serializer.save()
                print(user_serializer.data['email'])
                user = User.objects.get(email=user_serializer.data['email'])
                if serializer.is_valid():
                    serializer.save(user=user, total_amount=0)
                    return Response({'user_information': user_serializer.data, 'bank_information': serializer.data})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            transaction.savepoint_rollback(sid)
            return Response({'msg': 'Account Already Available...'})


class Client_Transaction_View(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Client_Transaction_Serializers

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        serializer = self.get_serializer(data=request.data)
        account = Account.objects.get(user=self.request.user)
        if serializer.is_valid():
            available_balance = 0
            amount = float(self.request.data.get('amount'))
            transaction_type = self.request.data.get('transaction_type')
            client_total_amount = Account.objects.get(user=self.request.user)
            if (amount) > 0:
                if transaction_type == 'Deposite':
                    available_balance = (
                        client_total_amount.total_amount+amount)
                elif(transaction_type == 'Withdraw'):
                    if (client_total_amount.total_amount) >= amount:
                        available_balance = (
                            client_total_amount.total_amount-amount)
                    else:
                        return Response({'message': 'Insufficent Balance Your Account..'})
                transaction.savepoint_commit(sid)
                client_total_amount.total_amount = available_balance
                client_total_amount.save()
                serializer.save(account=account,
                                available_balance=available_balance)
                return Response({'message': f'Successfully {transaction_type} Money..', 'data': serializer.data, 'available_balance': available_balance})
            else:
                transaction.savepoint_rollback(sid)
                return Response({'message': 'You are Enter Invalid Money..'})
        else:
            transaction.savepoint_rollback(sid)
            return Response({'message': 'Invalid Data..', 'data': serializer.errors})


class BalanceInquiryApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializers

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)