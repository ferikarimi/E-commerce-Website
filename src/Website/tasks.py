from celery import shared_tasks
import requests
from celery.backends.database import retry


@shared_tasks(retry=10)
def send_otp_code(otp_code):
    requests.get(f"http://127.0.0.1:8001/show_code/{otp_code}")