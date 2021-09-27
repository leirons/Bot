import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailbot.settings')
django.setup()

from mail.handlers.bot import run_pooling

if __name__ == "__main__":
    run_pooling()