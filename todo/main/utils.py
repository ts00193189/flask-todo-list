import datetime


class DateTimeConverter:
    @staticmethod
    def convert_date(form_date):
        date_pieces = form_date.split('-')
        date = datetime.date(int(date_pieces[0]), int(date_pieces[1]), int(date_pieces[2]))
        return date

    @staticmethod
    def convert_time(form_time):
        time_pieces = form_time.split(':')
        time = datetime.time(int(time_pieces[0]), int(time_pieces[1]))
        return time
