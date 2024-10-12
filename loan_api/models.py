from django.db import models
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField

# Create your models here.
class User(AbstractUser):
    is_borrower = models.BooleanField(default=False)
    is_lender = models.BooleanField(default=False)
    balance = MoneyField(max_digits=19, decimal_places=4, default_currency='IDR', default=0)

    def __str__(self):
        return self.username
    
class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('funded', 'Funded'),
        ('active', 'Active'),
        ('repaid', 'Repaid'),
        ('defaulted', 'Defaulted')
    ]

    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_amount = MoneyField(max_digits=19, decimal_places=4, default_currency='IDR')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.pk} -- {self.status}"
    
class Investment(models.Model):
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='investments')
    amount = MoneyField(max_digits=19, decimal_places=4, default_currency='IDR')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed')
    ], max_length=20)

    def __str__(self):
        return f"Investment by {self.lender} in Loan {self.loan}"
    
class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = MoneyField(max_digits=19, decimal_places=4, default_currency='IDR')
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=[
        ('due', 'Due'),
        ('paid', 'Paid'),
        ('late', 'Late')
    ], max_length=20)

    def __str__(self):
        return f"Repayment for Loan {self.loan.pk} -- {self.status}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('loan_disbursement', 'Loan Disbursement'),
        ('repayment', 'Repayment'),
        ('investment', 'Investment'),
        ('withdrawal', 'Withdrawal')
    ]

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = MoneyField(max_digits=19, decimal_places=4, default_currency='IDR')
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_type} -- {self.amount}"
    
class LoanRequest(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_requests')
    requested_amount = MoneyField(max_digits=19, decimal_places=4, default_currency='IDR')
    reason = models.TextField()
    status = models.CharField(choices=REQUEST_STATUS_CHOICES, max_length=20)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Loan request {self.pk} -- {self.status}"
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = MoneyField(max_digits=19, decimal_places=4, default_currency='IDR')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet for {self.user.username}"
    
class PaymentPlan(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payment_plans')
    installment_number = models.IntegerField()
    amount = MoneyField(max_digits=19, decimal_places=4, default_currency='IDR')
    due_date = models.DateField()
    status = models.CharField(choices=[
        ('due', 'Due'),
        ('paid', 'Paid'),
        ('late', 'Late')
    ], max_length=20)  