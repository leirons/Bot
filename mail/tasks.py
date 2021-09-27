from celery import shared_task
from .models import Email,TempEmail
from datetime import datetime
from django.core.mail import send_mail


@shared_task()
def send_email():
    emails = Email.get_all_emails()
    for i in emails:
        date = i.date
        d,m,y = date.split('-')
        today = datetime.now()
        if datetime(year=today.year,month=today.month,day=today.day) == datetime(year=int(y),month=int(m),day=int(d)):
            print('yes')
            send_mail(
                i.subject,
                i.message,
                'grecigor11@gmail.com',
                [i.mail],
                fail_silently=False,
            )
            Email.delete_email(id=i.id)


@shared_task()
def delete_email():
    temp_mails = TempEmail.get_all_temp_mail()
    for i in temp_mails:
        created_at = i.created_at
        if datetime.hour > created_at.hour:
            TempEmail.del_temp_mail(i.id)
