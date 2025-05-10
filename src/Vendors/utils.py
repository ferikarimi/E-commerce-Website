from datetime import timedelta
from django.utils import timezone


def get_date_range(range_code):
    now = timezone.now()
    if range_code == '1d':
        from_date = now - timedelta(days=1)
    elif range_code == '3d':
        from_date = now - timedelta(days=3)
    elif range_code == '1w':
        from_date = now - timedelta(days=7)
    elif range_code == '1m':
        from_date = now - timedelta(days=30)
    elif range_code == '3m':
        from_date = now - timedelta(days=90)

    return from_date
