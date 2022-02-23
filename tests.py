from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from bookkeeper.views import offset_month
from bookkeeper.models import Profile, BankAccount, SpendingAccount, StatementImport, ImportedTransaction
from bookkeeper.transactions import parse_transactions, _match_datetime


class MonthlyOffsetsTestCase(TestCase):
    def tests(self):
        self.assertEqual(
            offset_month(datetime(2021, 1, 1), -1),
            datetime(2020, 12, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 1, 1), -2),
            datetime(2020, 11, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 1, 1), -3),
            datetime(2020, 10, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 1, 1), -4),
            datetime(2020, 9, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 1, 1), -5),
            datetime(2020, 8, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 12, 1), 1),
            datetime(2022, 1, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 12, 1), 2),
            datetime(2022, 2, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 12, 1), 3),
            datetime(2022, 3, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 12, 1), 4),
            datetime(2022, 4, 1)
        )
        self.assertEqual(
            offset_month(datetime(2021, 12, 1), 5),
            datetime(2022, 5, 1)
        )


class StatementParsingTestCase(TestCase):
    def test_import(self):
        transactions = parse_transactions(
            "bookkeeper/statements_test/transaksjonsliste.xlsx",
            first=datetime(2017, 1, 1),
            last=datetime(2017, 1, 31)
        )
        with open("bookkeeper/statements_test/expected_transactions.csv") as fh:
            expected_transactions = [x.split(",") for x in fh.read().splitlines()]
            expected_transactions = [[x[0], x[1], float(x[2])] for x in expected_transactions]

        self.assertEqual(len(expected_transactions), len(transactions))

        for i in range(len(expected_transactions)):
            # for j in range(3):
            #     self.assertEqual(transactions[i][j], expected_transactions[i][j])
            expected = expected_transactions[i]
            actual = transactions[i]
            self.assertEqual(
                expected,
                actual,
                f"Forventa {expected}, fekk {actual}"
            )

    def test_datetime_matching(self):
        self.assertEqual(
            _match_datetime("15.12 kl. 11.00", 2022),
            datetime(2022, 12, 15, 11, 0)
        )
        self.assertEqual(
            _match_datetime("05.02 kl. 01.10", 2022),
            datetime(2022, 2, 5, 1, 10)
        )


class StatementImportTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', 'test@ema.il', 'password')
        self.profile = Profile.objects.create(user=self.user)

        with open('bookkeeper/statements_test/expected_transactions.csv') as fh:
            self.expected_transactions = [x.split(",") for x in fh.read().splitlines()]

        self.account = BankAccount.objects.create(name="Test account", owner=self.profile, balance=0)
        self.statement = StatementImport.objects.create(
            account=self.account,
            upload='bookkeeper/statements_test/transaksjonsliste.xlsx',
            first_day=datetime(2016, 12, 1),
            last_day=datetime(2016, 12, 31)
        )

        for i in range(len(self.expected_transactions)):
            # Create payees here, and add them to the "expected" list.
            payee = self.expected_transactions[i][1]
            instance = SpendingAccount.objects.create(owner=self.profile, name=payee)
            self.expected_transactions[i].append(instance)


    def test_parsing(self):
        transactions = self.statement.handle_data()

        for i in range(len(self.expected_transactions)):
            expected = self.expected_transactions[i]
            actual = transactions[i]
            self.assertEqual(expected[0], actual.date, "Date")
            self.assertEqual(expected[1], actual.payee.name, "Payee")
            self.assertEqual(float(expected[2]), actual.amount, "Amount")
