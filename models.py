from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BankAccount(models.Model):
    name = models.CharField(max_length=200)
    number = models.BigIntegerField(null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    balance = models.BigIntegerField()
    # currency = models.CharField(max_length=3)

    def current_balance(self):
        return self.balance - sum([x.amount for x in self.receipt_set.all()])

    def __str__(self):
        return self.name


class SpendingAccount(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name


# class Category(models.Model):
#     ...


class Payee(models.Model):
    name = models.CharField(max_length=200)
    # owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # default_category = models.ForeignKey(
    #     Category, on_delete=models.SET_NULL, null=True, blank=True
    # )

    def __str__(self):
        return self.name


class Receipt(models.Model):
    from_account = models.ForeignKey(
        BankAccount, on_delete=models.SET_NULL, null=True, blank=True
    )
    to_account = models.ForeignKey(
        SpendingAccount, on_delete=models.SET_NULL, null=True, blank=True
    )
    # payee = models.ForeignKey(Payee, on_delete=models.CASCADE)
    # category = models.ForeignKey(
    #     Category, on_delete=models.SET_NULL, null=True, blank=True
    # )
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    # currency = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.amount} @ {self.date}"


class Transaction(models.Model):
    from_account = models.ForeignKey(
        BankAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions_from"
    )
    to_account = models.ForeignKey(
        BankAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions_to"
    )
    date = models.DateTimeField()
    amount = models.BigIntegerField()

