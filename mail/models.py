from django.db import models
from asgiref.sync import sync_to_async


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)

    is_banned = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id

    @classmethod
    @sync_to_async
    def get_user_or_created(cls, data):
        u, created = cls.objects.get_or_create(user_id=int(data))
        return u, created


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=255)

    mail = models.EmailField(max_length=255)

    message = models.CharField(max_length=500)
    date = models.CharField(max_length=255)

    @classmethod
    @sync_to_async
    def get_email_or_created(cls, data, u):
        e, created = cls.objects.get_or_create(
            user=u,
            subject=data['subject'],
            message=data['message'],
            date=data['date'],
            mail=data['email']
        )
        return e, created

    @classmethod
    def get_all_emails(cls):
        return cls.objects.all()

    @classmethod
    def delete_email(cls, id):
        cls.objects.filter(
            id=id
        ).delete()

    @classmethod
    @sync_to_async
    def get_email_of_user(cls, u):
        e = cls.objects.get(
            user_id=u,
        )
        return e


def __str__(self):
    return self.user


class TempEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    email = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now=True)

    @classmethod
    def del_temp_mail(cls, id):
        cls.objects.filter(
            id=id
        ).delete()

    @classmethod
    def get_all_temp_mail(cls):
        return cls.objects.all()

    @classmethod
    @sync_to_async
    def get_temp_mail(cls, user_id):
        e = cls.objects.get(
            user=user_id
        )
        return e

    @classmethod
    @sync_to_async
    def create_temp_mail(cls, u, email, domain=None):
        cls.objects.create(user_id=u, email=email, domain=domain)
