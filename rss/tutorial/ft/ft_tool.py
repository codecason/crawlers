# =*= coding: utf-8 -*-
import os
import json
import datetime, time

class TimeFilter():
    
    def filter_date(self, days, collection):
        d = 0
        if days == 'week':
            d = -7
        elif days == 'three':
            d = -3
        elif days == 'ten':
            d = -10
        today = datetime.datetime.today()
        delta = datetime.timedelta(days=d)
        first = today + delta
        return first

    def get_time_sql(self, days):
        today = datetime.datetime.today()
        start = today + datetime.timedelta(days=-days)
        start = datetime.datetime(start.year, start.month, start.day, 0, 0)
        end = today
        end = datetime.datetime(end.year, end.month, end.day, 23, 59)
        between = {'$gte': start, '$lt': end}
        return between
    
    @staticmethod
    def get_today_str(style='date'):
        today = datetime.datetime.today()
        day = ''
        if style == 'date':
            day = today.strftime('%Y-%m-%d')
        elif style == 'time':
            # 2010-12-20 20:20:20.1233 => 2010-12-20 20:20:20
            day = day.__str__().split('.')[0]
        return day

    # @staticmethod
    # def get_datetime(datestr, pattern):
    #     return datetime.datetime.strptime(datestr, pattern)
