# MailBot

Simple beautiful telegram bot for sending emails also sending emails in the future. You can create your own TempEmail for one hour and read messages from there.

in this project i have used:
Django
Aiogram
Celery
Redis

## How to run
git clone https://github.com/leirons/MailBot.git

```
pip3 install -r requirements.txt
```

create .env file  and enter there

TOKEN

EMAIL_HOST

EMAIL_HOST_USER

EMAIL_HOST_PASSWORD

EMAIL_PORT

EMAIL_USE_TLS default is True

Then run redis server and tasks with two commands:

```
celery -A mailbot worker -l INFO --pool = solo

celery -A mailbot beat -l INFO 
```

and run tg bot with command 
```
python manage.py run_pooling
```
