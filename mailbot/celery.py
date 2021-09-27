import os
from celery import Celery
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailbot.settings')

app = Celery('mailbot')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.update(
    result_expires=3600,
    enable_utc = True,
    timezone = 'UTC'
)

app.conf.beat_schedule = {
    "see-you-in-ten-seconds-task": {
        "task": 'mail.tasks.send_email',
        "schedule":timedelta(seconds=10)
    }
}

app.conf.beat_schedule = {
    "see-you-in-ten-seconds-task": {
        "task": 'mail.tasks.delete_email',
        "schedule":timedelta(hours=1)
    }
}