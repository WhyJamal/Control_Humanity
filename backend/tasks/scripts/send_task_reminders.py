import os
import django
import requests
import sys

from django.conf import settings
from django.contrib.auth import get_user_model

sys.path.append("C:/Users/user/Desktop/nebula projects/web_programs/control_humanity/config")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
API_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

def send_message(chat_id, text):
    if chat_id:
        requests.post(API_URL, data={
            'chat_id': chat_id,
            'text': text
        })

def run():
    users = User.objects.exclude(telegram_id=None)
    for user in users:
        send_message(user.telegram_id, "automatic launch completed!")

if __name__ == "__main__":
    run()
