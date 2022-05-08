import datetime
from unittest import TestCase

from todo.main.utils import DateTimeConverter


class DateTimeConverterTestCase(TestCase):
    def test_convert_date_valid_str_return_date(self):
        date = '2022-01-01'
        convert_date = DateTimeConverter.convert_date(date)
        result = datetime.date(2022, 1, 1)
        self.assertEqual(convert_date, result)

    def test_convert_date_invalid_str_return_None(self):
        date = '2022/01/01'
        convert_date = DateTimeConverter.convert_date(date)
        self.assertIsNone(convert_date)

    def test_convert_date_None_return_None(self):
        date = None
        convert_date = DateTimeConverter.convert_date(date)
        self.assertIsNone(convert_date)

    def test_convert_time_valid_str_return_time(self):
        time = '01:11'
        convert_time = DateTimeConverter.convert_time(time)
        result = datetime.time(1, 11)
        self.assertEqual(convert_time, result)

    def test_convert_time_invalid_str_return_None(self):
        time = '01.11'
        convert_time = DateTimeConverter.convert_time(time)
        self.assertIsNone(convert_time)

    def test_convert_time_None_return_None(self):
        time = None
        convert_time = DateTimeConverter.convert_time(time)
        self.assertIsNone(convert_time)
