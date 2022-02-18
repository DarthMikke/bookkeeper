from django.test import TestCase
from bookkeeper.views import offset_month
from datetime import datetime
from bookkeeper.transactions import parse_transactions, _match_datetime


class TestMonthlyOffsets(TestCase):
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


class StatementImportTestCase(TestCase):
    def test_import(self):
        transactions = parse_transactions(
            "bookkeeper/statements_test/transaksjonsliste.xlsx",
            first=datetime(2017, 1, 1),
            last=datetime(2017, 1, 31)
        )
        with open("bookkeeper/statements_test/expected_transactions.csv") as fh:
            expected_transactions = [x.split(",") for x in fh.read().splitlines()]
            expected_transactions = [[x[0], x[1], float(x[2])] for x in expected_transactions]

        for i in range(len(expected_transactions)):
            for j in range(3):
                self.assertEqual(transactions[i][j], expected_transactions[i][j])
