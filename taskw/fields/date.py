import datetime

import dateutil
from dateutil.parser import parse
import pytz

from taskw.utils import DATE_FORMAT

from .base import Field


class DateField(Field):
    def deserialize(self, value):
        if not value:
            return value
        value = parse(value)
        if not value.tzinfo:
            value = value.replace(tzinfo=pytz.utc)
        return value

    def serialize(self, value):
        if isinstance(value, datetime.datetime):
            if not value.tzinfo:
                #  Dates not having timezone information should be
                #  assumed to be in local time
                value = value.replace(tzinfo=dateutil.tz.tzlocal())
            #  All times should be converted to UTC before serializing
            value = value.astimezone(pytz.utc).strftime(DATE_FORMAT)
        elif isinstance(value, datetime.date):
            value = value.strftime(DATE_FORMAT)
        return value
