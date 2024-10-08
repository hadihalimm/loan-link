from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Loan, Investment, Repayment, Transaction, LoanRequest, Wallet, PaymentPlan

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_borrower', 'is_lender', 'balance']
        read_only_fields = ['balance']

class LoanSerializer(serializers.ModelSerializer):
    borrower = serializers.StringRelatedField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'borrower', 'loan_amount', 'interest_rate', 'duration', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']

class InvestmentSerializer(serializers.ModelSerializer):
    lender = serializers.StringRelatedField(read_only=True)
    loan = LoanSerializer(read_only=True)
    loan_id = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all(), write_only=True)

    class Meta:
        model = Investment
        fields = ['id', 'lender', 'loan', 'loan_id', 'amount', 'status', 'created_at']
        read_only_fields = ['lender', 'status', 'created_at']

class RepaymentSerializer(serializers.ModelSerializer):
    loan = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Repayment
        fields = ['id', 'loan', 'amount', 'due_date', 'paid_date', 'status']
        read_only_fields = ['loan', 'status']

class TransactionSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField(read_only=True)
    to_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'from_user', 'to_user', 'amount', 'transaction_type', 'created_at']
        read_only_fields = ['from_user', 'to_user', 'transaction_type', 'created_at']

class LoanRequestSerializer(serializers.ModelSerializer):
    borrower = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = LoanRequest
        fields = ['id', 'borrower', 'requested_amount', 'reason', 'status', 'created_at']
        read_only_fields = ['borrower', 'status', 'created_at']

class WalletSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'last_updated']
        read_only_fields = ['user', 'balance', 'last_updated']

class PaymentPlanSerializer(serializers.ModelSerializer):
    loan = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = PaymentPlan
        fields = ['id', 'loan', 'installment_number', 'amount', 'due_date', 'status']
        read_only_fields = ['loan', 'status']