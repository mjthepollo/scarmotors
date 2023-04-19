from datetime import datetime

from core.utility import get_time
from django.test import TestCase


class CoreUtilityTest(TestCase):
    def test_get_time(self):
        morning = datetime(2019, 2, 15, 4, 58, 4,)
        night = datetime(2019, 2, 15, 20, 12, 4,)
        assert get_time(morning) == 'morning'
        assert get_time(night) == 'night'
