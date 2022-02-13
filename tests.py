from django.test import TestCase
from .views import offset_month
from datetime import datetime


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
