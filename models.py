from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone

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

    def number_of_receipts(self):
        return len(self.receipt_set.all())

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


def import_path(instance, filename):
    return 'statements/{0}/{1}/{2}_{3}'.format(
        datetime.now().date().isoformat(),
        instance.account.owner_id,
        datetime.now().time().isoformat(),
        filename
    )


class StatementImport(models.Model):
    """
    Model for storing and accessing imported bank statements.
    To protect privacy, bank statement files older than a threshold value
    should be removed every day (e.g. by a cron job).
    """
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    upload = models.FileField(upload_to=import_path)
    created_at = models.DateTimeField(default=datetime.now)
    first_day = models.DateField()
    last_day = models.DateField()
    processed = models.BooleanField(default=False)

    def should_delete(self) -> bool:
        return (self.created_at + timedelta(31)) < datetime.now(tz=timezone.utc)

    def __str__(self):
        return "Import to {0}".format(self.account.name)


class ImportedTransaction(models.Model):
    statement_import = models.ForeignKey(StatementImport, on_delete=models.CASCADE)
    payee = models.ForeignKey(SpendingAccount, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField()
    amount = models.FloatField()
